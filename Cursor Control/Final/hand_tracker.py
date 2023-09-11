# hand_tracker.py

import cv2
import mediapipe as mp
from screeninfo import get_monitors

class HandTracker:
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands()

        self.cap = cv2.VideoCapture(0)
        self.monitor = get_monitors()[0]
        self.screen_width, self.screen_height = self.monitor.width, self.monitor.height

    def read_frame(self):
        return self.cap.read()

    def process_frame(self, image):
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        results = self.hands.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return results, image

    def draw_landmarks(self, image, hand_landmarks):
        self.mp_drawing.draw_landmarks(image, hand_landmarks, self.mphands.HAND_CONNECTIONS)

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()