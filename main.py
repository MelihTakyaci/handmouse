import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

# Get screen resolution
screen_width, screen_height = pyautogui.size()

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
prev_click_time = 0

# Define ROI size based on screen aspect ratio
roi_h = int(480 * 0.8)  # 80% of camera height
roi_w = int(roi_h * (screen_width / screen_height))  # match screen aspect ratio

# ROI interaction settings
zoom_step = 10
move_step = 10

# Smoothing parameters for mouse movement
smooth_x, smooth_y = 0, 0
smoothing_factor = 3

# Gesture control variables
gesture_mode = False
gesture_start_x = 0
gesture_triggered = False
gesture_cooldown = 1

# Right click cooldown
prev_right_click_time = 0

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)  # Mirror image for intuitive control
    h, w, _ = img.shape
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Dynamically center the ROI each frame
    roi_x = int((w - roi_w) // 2)
    roi_y = 1

    roi = img_rgb[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]
    results = hands.process(roi)

    # Draw the ROI box on screen
    cv2.rectangle(img, (roi_x, roi_y), (roi_x + roi_w, roi_y + roi_h), (0, 0, 255), 2)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w], hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = hand_landmarks.landmark

            # Extract key landmark coordinates
            index_x = int(landmarks[8].x * roi_w) + roi_x
            index_y = int(landmarks[8].y * roi_h) + roi_y
            thumb_x = int(landmarks[4].x * roi_w) + roi_x
            thumb_y = int(landmarks[4].y * roi_h) + roi_y

            thumb_knuckle_x = int(landmarks[2].x * roi_w) + roi_x
            thumb_knuckle_y = int(landmarks[2].y * roi_h) + roi_y
            index_knuckle_x = int(landmarks[5].x * roi_w) + roi_x
            index_knuckle_y = int(landmarks[5].y * roi_h) + roi_y

            middle_x = int(landmarks[12].x * roi_w) + roi_x
            middle_y = int(landmarks[12].y * roi_h) + roi_y

            # Visualize tracked points
            cv2.circle(img, (index_x, index_y), 10, (0, 255, 255), cv2.FILLED)
            cv2.circle(img, (thumb_x, thumb_y), 10, (255, 255, 0), cv2.FILLED)
            cv2.circle(img, (middle_x, middle_y), 10, (0, 0, 255), cv2.FILLED)
            cv2.line(img, (index_x, index_y), (thumb_x, thumb_y), (0, 255, 0), 2)

            # Define a padded area inside ROI to ensure control without reaching edges
            pad_x = int(roi_w * 0.1)
            pad_y = int(roi_h * 0.3)

            min_x = roi_x + pad_x
            max_x = roi_x + roi_w - pad_x
            min_y = roi_y + pad_y
            max_y = roi_y + roi_h - pad_y

            middle_x_clamped = np.clip(middle_x, min_x, max_x)
            middle_y_clamped = np.clip(middle_y, min_y, max_y)

            # Map the clamped coordinates to screen space
            screen_x = np.interp(middle_x_clamped, [min_x, max_x], [0, screen_width])
            screen_y = np.interp(middle_y_clamped, [min_y, max_y], [0, screen_height])
            print(f"Mouse move to: ({screen_x:.0f}, {screen_y:.0f})")

            # Smooth the mouse movement
            smooth_x += (screen_x - smooth_x) / smoothing_factor
            smooth_y += (screen_y - smooth_y) / smoothing_factor
            pyautogui.moveTo(int(smooth_x), int(smooth_y))

            # Left click gesture: thumb and index finger tip proximity
            distance = np.hypot(thumb_x - index_x, thumb_y - index_y)
            dynamic_threshold = roi_w * 0.05
            if distance < dynamic_threshold:
                now = time.time()
                if now - prev_click_time > 1:
                    pyautogui.click()
                    prev_click_time = now
                    cv2.putText(img, 'Click!', (middle_x, middle_y - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Right click gesture: thumb and index knuckle proximity
            right_click_distance = np.hypot(index_knuckle_x - thumb_x, index_knuckle_y - thumb_y)
            if right_click_distance < dynamic_threshold:
                now = time.time()
                if now - prev_right_click_time > 1:
                    pyautogui.rightClick()
                    prev_right_click_time = now
                    cv2.putText(img, 'Right Click!', (index_knuckle_x, index_knuckle_y - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

            # Gesture-based desktop switching (MacOS): thumb and thumb knuckle proximity, then lateral movement
            thumb_ring_distance = np.hypot(thumb_x - thumb_knuckle_x, thumb_y - thumb_knuckle_y)
            hand_center_x = int(landmarks[9].x * roi_w) + roi_x

            if not gesture_mode and thumb_ring_distance < dynamic_threshold:
                gesture_mode = True
                gesture_start_x = hand_center_x
                gesture_triggered = False
                gesture_start_time = time.time()

            if gesture_mode:
                dx = hand_center_x - gesture_start_x
                if not gesture_triggered and abs(dx) > 40:
                    if dx > 0:
                        pyautogui.hotkey('ctrl', 'right')
                        print("→ Desktop")
                    else:
                        pyautogui.hotkey('ctrl', 'left')
                        print("← Desktop")
                    gesture_triggered = True

                if time.time() - gesture_start_time > gesture_cooldown:
                    gesture_mode = False

    cv2.imshow("HandMouse - ROI Enabled", img)

    # Keyboard controls for adjusting ROI manually
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('i'):
        roi_w = max(100, roi_w - zoom_step)
        roi_h = max(100, roi_h - zoom_step)
    elif key == ord('o'):
        roi_w = min(w - roi_x, roi_w + zoom_step)
        roi_h = min(h - roi_y, roi_h + zoom_step)
    elif key == ord('w'):
        roi_y = max(0, roi_y - move_step)
    elif key == ord('s'):
        roi_y = min(h - roi_h, roi_y + move_step)
    elif key == ord('a'):
        roi_x = max(0, roi_x - move_step)
    elif key == ord('d'):
        roi_x = min(w - roi_w, roi_x + move_step)

cap.release()
cv2.destroyAllWindows()
