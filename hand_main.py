# hand-main.py

import cv2
from hand_tracker import HandTracker
from hand_gesture_controller import HandGestureController

def call_for_gesture(terminate_queue):
    hand_tracker = HandTracker()
    hand_gesture_controller = HandGestureController()

    while True:
        data, image = hand_tracker.read_frame()
        results, image = hand_tracker.process_frame(image)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                hand_tracker.draw_landmarks(image, hand_landmarks)
                hand_gesture_controller.detect_gestures(hand_tracker.mphands.HandLandmark, hand_landmarks)

        hand_gesture_controller.perform_actions()

        cv2.imshow('Waver', image)
        cv2.waitKey(100)

        if cv2.waitKey(100) & 0xFF == ord('q') or not terminate_queue.empty():
            message = terminate_queue.get()
            if message == "terminate":
                break

    hand_tracker.release()

# if __name__ == "__mq