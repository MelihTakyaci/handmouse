import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, max_num_hands=1, detection_confidence=0.5, tracking_confidence=0.5):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_num_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils

    def process(self, image):
        """
        İşlenen görüntüde el tespiti yapar ve sonuçları döndürür.
        Giriş olarak RGB formatında veya BGR olup dönüşüm yapılır.
        """
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)
        return results

    def draw_landmarks(self, image, hand_landmarks):
        """
        Belirtilen görüntü üzerinde el işaret noktalarını ve bağlantılarını çizer.
        """
        self.mp_draw.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)