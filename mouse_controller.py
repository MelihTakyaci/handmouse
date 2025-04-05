import pyautogui
import time

class MouseController:
    def __init__(self, smoothing_factor=3, click_cooldown=1, right_click_cooldown=1):
        self.smooth_x = 0
        self.smooth_y = 0
        self.smoothing_factor = smoothing_factor
        self.prev_click_time = 0
        self.prev_right_click_time = 0
        self.click_cooldown = click_cooldown
        self.right_click_cooldown = right_click_cooldown

    def move_mouse(self, target_x, target_y):
        """
        Hedef koordinatlara doğru fare hareketini yumuşatarak uygular.
        """
        self.smooth_x += (target_x - self.smooth_x) / self.smoothing_factor
        self.smooth_y += (target_y - self.smooth_y) / self.smoothing_factor
        pyautogui.moveTo(int(self.smooth_x), int(self.smooth_y))

    def left_click(self):
        """
        Sol tıklamayı tetikler, tıklamalar arası süre kontrolü yapar.
        """
        now = time.time()
        if now - self.prev_click_time > self.click_cooldown:
            pyautogui.click()
            self.prev_click_time = now

    def right_click(self):
        """
        Sağ tıklamayı tetikler, tıklamalar arası süre kontrolü yapar.
        """
        now = time.time()
        if now - self.prev_right_click_time > self.right_click_cooldown:
            pyautogui.rightClick()
            self.prev_right_click_time = now

    def switch_desktop(self, direction):
        """
        Masaüstleri arasında geçiş için hotkey kullanır.
        direction: 'left' veya 'right'
        """
        if direction == 'left':
            pyautogui.hotkey('ctrl', 'left')
        elif direction == 'right':
            pyautogui.hotkey('ctrl', 'right')