import time
import pyautogui

class GestureController:
    def __init__(self, cooldown=1, trigger_threshold=40):
        self.gesture_mode = False
        self.gesture_start_x = 0
        self.gesture_triggered = False
        self.gesture_start_time = 0
        self.gesture_cooldown = cooldown
        self.trigger_threshold = trigger_threshold

    def start_gesture(self, start_x):
        """
        Jest modu başlatılır ve başlangıç x koordinatı kaydedilir.
        """
        self.gesture_mode = True
        self.gesture_start_x = start_x
        self.gesture_triggered = False
        self.gesture_start_time = time.time()

    def process_gesture(self, current_x):
        """
        Jest modundaki el hareketine göre masaüstü geçişini tetikler.
        """
        if self.gesture_mode:
            dx = current_x - self.gesture_start_x
            if not self.gesture_triggered and abs(dx) > self.trigger_threshold:
                direction = 'right' if dx > 0 else 'left'
                if direction == 'right':
                    pyautogui.hotkey('ctrl', 'right')
                else:
                    pyautogui.hotkey('ctrl', 'left')
                self.gesture_triggered = True
            if time.time() - self.gesture_start_time > self.gesture_cooldown:
                self.gesture_mode = False