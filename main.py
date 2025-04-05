import cv2
import numpy as np
import pyautogui

from hand_tracker import HandTracker
from mouse_controller import MouseController
from roi_manager import ROIManager
from gesture_controller import GestureController

def main():
    # Sabit kamera boyutları
    frame_w, frame_h = 640, 480

    screen_width, screen_height = pyautogui.size()

    cap = cv2.VideoCapture(1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_w)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_h)

    # Modülleri başlat
    hand_tracker = HandTracker(max_num_hands=1)
    mouse_controller = MouseController(smoothing_factor=3)
    roi_manager = ROIManager(screen_width, screen_height, cam_width=frame_w, cam_height=frame_h, scale=0.8)
    gesture_controller = GestureController(cooldown=1, trigger_threshold=40)

    # Ayarlar penceresi ve slider ile ilgili değişkenler
    settings_window_open = False
    slider_active = False
    slider_min = 1
    slider_max = 10
    slider_value = mouse_controller.smoothing_factor  # başlangıç değeri: 3

    # Ayarlar ikonunun koordinatları (sabit: sağ üst köşe)
    settings_icon_top_left = (frame_w - 50, 10)
    settings_icon_bottom_right = (frame_w - 10, 50)

    window_name = "HandMouse - ROI Enabled"
    cv2.namedWindow(window_name)

    def on_mouse(event, x, y, flags, param):
        nonlocal settings_window_open, slider_active, slider_value, frame_w, frame_h
        # Pop-up pencere koordinatlarını hesapla
        popup_w, popup_h = 300, 300
        popup_x = (frame_w - popup_w) // 2
        popup_y = (frame_h - popup_h) // 2
        # Kapatma butonu (sağ üst köşe, 30x30)
        close_button_w, close_button_h = 30, 30
        close_button_x = popup_x + popup_w - close_button_w
        close_button_y = popup_y
        # Slider koordinatları
        track_x = popup_x + 50
        track_y = popup_y + 150
        track_width = 200
        track_height = 10

        if event == cv2.EVENT_LBUTTONDOWN:
            if not settings_window_open:
                # Ayarlar ikonuna tıklanırsa
                if settings_icon_top_left[0] <= x <= settings_icon_bottom_right[0] and \
                   settings_icon_top_left[1] <= y <= settings_icon_bottom_right[1]:
                    print("Ayarlar açılıyor...")
                    settings_window_open = True
            else:
                # Ayarlar penceresi açıksa: önce kapatma butonuna bak
                if close_button_x <= x <= close_button_x + close_button_w and \
                   close_button_y <= y <= close_button_y + close_button_h:
                    print("Ayarlar kapatılıyor...")
                    settings_window_open = False
                # Slider track alanına tıklanırsa
                elif track_x <= x <= track_x + track_width and track_y <= y <= track_y + track_height:
                    slider_active = True
                    ratio = (x - track_x) / track_width
                    slider_value = int(slider_min + ratio * (slider_max - slider_min))
                    slider_value = max(slider_min, min(slider_value, slider_max))
                    mouse_controller.smoothing_factor = slider_value
        elif event == cv2.EVENT_MOUSEMOVE:
            if slider_active:
                # Slider aktifken, değeri güncelle
                if x < track_x:
                    x = track_x
                elif x > track_x + track_width:
                    x = track_x + track_width
                ratio = (x - track_x) / track_width
                slider_value = int(slider_min + ratio * (slider_max - slider_min))
                mouse_controller.smoothing_factor = slider_value
        elif event == cv2.EVENT_LBUTTONUP:
            slider_active = False

    cv2.setMouseCallback(window_name, on_mouse)

    def draw_settings_popup(img):
        nonlocal slider_value, frame_w, frame_h
        popup_w, popup_h = 300, 300
        popup_x = (frame_w - popup_w) // 2
        popup_y = (frame_h - popup_h) // 2

        # Pop-up arka planı ve kenarlık
        cv2.rectangle(img, (popup_x, popup_y), (popup_x + popup_w, popup_y + popup_h), (50, 50, 50), -1)
        cv2.rectangle(img, (popup_x, popup_y), (popup_x + popup_w, popup_y + popup_h), (200, 200, 200), 2)
        # Kapatma butonu
        close_button_w, close_button_h = 30, 30
        close_button_x = popup_x + popup_w - close_button_w
        close_button_y = popup_y
        cv2.rectangle(img, (close_button_x, close_button_y), (close_button_x + close_button_w, close_button_y + close_button_h), (0, 0, 255), -1)
        cv2.putText(img, 'X', (close_button_x + 8, close_button_y + 22), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        # Başlık metni
        cv2.putText(img, 'Ayarlar', (popup_x + 20, popup_y + 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Slider etiket ve track çizimi
        cv2.putText(img, f"Smoothing: {slider_value}", (popup_x + 50, popup_y + 130),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        track_x = popup_x + 50
        track_y = popup_y + 150
        track_width = 200
        track_height = 10
        cv2.rectangle(img, (track_x, track_y), (track_x + track_width, track_y + track_height), (100, 100, 100), -1)
        # Slider knob hesaplama ve çizimi
        ratio = (slider_value - slider_min) / (slider_max - slider_min)
        knob_x = track_x + int(ratio * track_width)
        knob_y = track_y + track_height // 2
        cv2.circle(img, (knob_x, knob_y), 10, (0, 255, 0), -1)

    while True:
        success, img = cap.read()
        if not success:
            break

        img = cv2.flip(img, 1)
        frame_h, frame_w, _ = img.shape

        # Ayarlar ikonunu çiz
        cv2.rectangle(img, settings_icon_top_left, settings_icon_bottom_right, (200, 200, 200), -1)
        cv2.putText(img, '...', (settings_icon_top_left[0] + 10, settings_icon_top_left[1] + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 50), 2)

        # ROI ve el tespiti
        roi = img[roi_manager.roi_y:roi_manager.roi_y + roi_manager.roi_h, roi_manager.roi_x:roi_manager.roi_x + roi_manager.roi_w]
        roi_rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
        results = hand_tracker.process(roi_rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                hand_tracker.draw_landmarks(roi, hand_landmarks)
                landmarks = hand_landmarks.landmark

                index_x = int(landmarks[8].x * roi_manager.roi_w) + roi_manager.roi_x
                index_y = int(landmarks[8].y * roi_manager.roi_h) + roi_manager.roi_y
                thumb_x = int(landmarks[4].x * roi_manager.roi_w) + roi_manager.roi_x
                thumb_y = int(landmarks[4].y * roi_manager.roi_h) + roi_manager.roi_y

                thumb_knuckle_x = int(landmarks[2].x * roi_manager.roi_w) + roi_manager.roi_x
                thumb_knuckle_y = int(landmarks[2].y * roi_manager.roi_h) + roi_manager.roi_y
                index_knuckle_x = int(landmarks[5].x * roi_manager.roi_w) + roi_manager.roi_x
                index_knuckle_y = int(landmarks[5].y * roi_manager.roi_h) + roi_manager.roi_y

                middle_x = int(landmarks[12].x * roi_manager.roi_w) + roi_manager.roi_x
                middle_y = int(landmarks[12].y * roi_manager.roi_h) + roi_manager.roi_y

                cv2.circle(img, (index_x, index_y), 10, (0, 255, 255), cv2.FILLED)
                cv2.circle(img, (thumb_x, thumb_y), 10, (255, 255, 0), cv2.FILLED)
                cv2.circle(img, (middle_x, middle_y), 10, (0, 0, 255), cv2.FILLED)
                cv2.line(img, (index_x, index_y), (thumb_x, thumb_y), (0, 255, 0), 2)

                pad_x = int(roi_manager.roi_w * 0.1)
                pad_y = int(roi_manager.roi_h * 0.3)
                min_x = roi_manager.roi_x + pad_x
                max_x = roi_manager.roi_x + roi_manager.roi_w - pad_x
                min_y = roi_manager.roi_y + pad_y
                max_y = roi_manager.roi_y + roi_manager.roi_h - pad_y

                middle_x_clamped = np.clip(middle_x, min_x, max_x)
                middle_y_clamped = np.clip(middle_y, min_y, max_y)

                screen_x = np.interp(middle_x_clamped, [min_x, max_x], [0, screen_width])
                screen_y = np.interp(middle_y_clamped, [min_y, max_y], [0, screen_height])
                print(f"Mouse move to: ({screen_x:.0f}, {screen_y:.0f})")
                mouse_controller.move_mouse(screen_x, screen_y)

                distance = np.hypot(thumb_x - index_x, thumb_y - index_y)
                dynamic_threshold = roi_manager.roi_w * 0.05
                if distance < dynamic_threshold:
                    mouse_controller.left_click()
                    cv2.putText(img, 'Click!', (middle_x, middle_y - 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                right_click_distance = np.hypot(index_knuckle_x - thumb_x, index_knuckle_y - thumb_y)
                if right_click_distance < dynamic_threshold:
                    mouse_controller.right_click()
                    cv2.putText(img, 'Right Click!', (index_knuckle_x, index_knuckle_y - 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

                thumb_ring_distance = np.hypot(thumb_x - thumb_knuckle_x, thumb_y - thumb_knuckle_y)
                hand_center_x = int(landmarks[9].x * roi_manager.roi_w) + roi_manager.roi_x
                if not gesture_controller.gesture_mode and thumb_ring_distance < dynamic_threshold:
                    gesture_controller.start_gesture(hand_center_x)
                if gesture_controller.gesture_mode:
                    gesture_controller.process_gesture(hand_center_x)

        cv2.rectangle(img, (roi_manager.roi_x, roi_manager.roi_y), 
                      (roi_manager.roi_x + roi_manager.roi_w, roi_manager.roi_y + roi_manager.roi_h), (0, 0, 255), 2)

        if settings_window_open:
            draw_settings_popup(img)

        cv2.imshow(window_name, img)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        roi_manager.update_roi(frame_w, frame_h, key)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()