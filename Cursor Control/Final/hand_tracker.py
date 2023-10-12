# hand_tracker.py

import cv2
import mediapipe as mp
# from main import data, image, results
# from screeninfo import get_monitorsqq

class HandTracker:
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands(static_image_mode = False, max_num_hands = 1, min_detection_confidence = 0.6)

        self.cap = cv2.VideoCapture(0)

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