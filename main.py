import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

# Ekran boyutu
screen_width, screen_height = pyautogui.size()

# MediaPipe eller
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Kamera
cap = cv2.VideoCapture(1)
prev_click_time = 0

# ROI ayarları
roi_x, roi_y, roi_w, roi_h = 100, 100, 600, 600
zoom_step = 20
move_step = 20

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    h, w, _ = img.shape
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # ROI'yi her karede merkeze yerleştir
    roi_x = (w - roi_w) // 2
    roi_y = (h - roi_h) // 2

    roi = img_rgb[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]
    results = hands.process(roi)

    # ROI çiz
    cv2.rectangle(img, (roi_x, roi_y), (roi_x + roi_w, roi_y + roi_h), (0, 0, 255), 2)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w], hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = hand_landmarks.landmark

            # TODO make better optimization for mouse movement
            # ROI içi koordinatları tüm ekrana çevir
            x1 = int(landmarks[8].x * roi_w) + roi_x
            y1 = int(landmarks[8].y * roi_h) + roi_y
            x2 = int(landmarks[4].x * roi_w) + roi_x
            y2 = int(landmarks[4].y * roi_h) + roi_y

            # Çizim
            cv2.circle(img, (x1, y1), 10, (0, 255, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 255, 0), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Ekran koordinatlarına dönüştürme
            screen_x = np.interp(x1, [roi_x, roi_x + roi_w], [0, screen_width])
            screen_y = np.interp(y1, [roi_y, roi_y + roi_h], [0, screen_height])
            print(f"Mouse move to: ({screen_x:.0f}, {screen_y:.0f})")

            pyautogui.moveTo(int(screen_x), int(screen_y))

            # Tıklama kontrolü
            distance = np.hypot(x2 - x1, y2 - y1)
            if distance < 40:
                now = time.time()
                if now - prev_click_time > 1:
                    pyautogui.click()
                    prev_click_time = now
                    cv2.putText(img, 'Click!', (x1, y1 - 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("HandMouse - ROI Destekli", img)

    # Klavye kontrol
    key = cv2.waitKey(1)

    if key == ord('q'):
        break
    elif key == ord('i'):  # Zoom in
        roi_w = max(100, roi_w - zoom_step)
        roi_h = max(100, roi_h - zoom_step)
    elif key == ord('o'):  # Zoom out
        roi_w = min(w - roi_x, roi_w + zoom_step)
        roi_h = min(h - roi_y, roi_h + zoom_step)
    elif key == ord('w'):  # Up arrow
        roi_y = max(0, roi_y - move_step)
    elif key == ord('s'):  # Down arrow
        roi_y = min(h - roi_h, roi_y + move_step)
    elif key == ord('a'):  # Left arrow
        roi_x = max(0, roi_x - move_step)
    elif key == ord('d'):  # Right arrow
        roi_x = min(w - roi_w, roi_x + move_step)

cap.release()
cv2.destroyAllWindows()