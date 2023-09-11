# hand_gesture_controller.py

import math
import pyautogui
import hand_tracker as HandTracker
from screeninfo import get_monitors

class HandGestureController:
    def __init__(self):
        self.clicking = False
        self.scrolling_up = False
        self.scrolling_down = False
        self.tab_shifting = False
        self.volume_up = False
        self.volume_down = False

    def detect_gestures(self, mphands, hand_landmarks):
        scaling_factor = 1.5  # Scaling factor depends on the distance of hand from the camera
        

        index_finger = hand_landmarks.landmark[mphands.INDEX_FINGER_TIP]
        middle_finger = hand_landmarks.landmark[mphands.MIDDLE_FINGER_TIP]
        pinky_finger = hand_landmarks.landmark[mphands.PINKY_TIP]
        thumb = hand_landmarks.landmark[mphands.THUMB_TIP]
        wrist = hand_landmarks.landmark[mphands.WRIST]
        palm = hand_landmarks.landmark[mphands.MIDDLE_FINGER_MCP]
        ring_finger = hand_landmarks.landmark[mphands.RING_FINGER_TIP]

        dist_threshold = math.pow((index_finger.y - middle_finger.y), 2) + math.pow((index_finger.x - middle_finger.x), 2)
        hand_length = math.pow((wrist.y - middle_finger.y), 2) + math.pow((wrist.x - middle_finger.x), 2)

        scroll_up_threshold = 0.2  # Threshold for index finger to trigger scroll up
        scroll_down_threshold = 0.2  # Threshold for pinky finger to trigger scroll down

        volume_up_threshold = 0.2  # Threshold for index finger to trigger volume up
        volume_down_threshold = 0.2  # Threshold for pinky finger to trigger volume down

        monitor = get_monitors()[0]
        screen_width, screen_height = monitor.width, monitor.height
        
        # Check if all four fingers are detected
        if thumb.y < index_finger.y and thumb.y < middle_finger.y:
            clicking = True
        else:
            clicking = False

        # Detect scroll-up gesture
        if index_finger.y < middle_finger.y - scroll_up_threshold:
            scrolling_up = True
        else:
            scrolling_up = False

        # Detect scroll-down gesture
        if pinky_finger.y < middle_finger.y - scroll_down_threshold:
            scrolling_down = True
        else:
            scrolling_down = False
            
        #Detect volume-up gesture
        if (middle_finger.y < pinky_finger.y - volume_up_threshold) and (index_finger.y < pinky_finger.y - volume_up_threshold) and (ring_finger.y < pinky_finger.y - volume_up_threshold) :
            volume_up = True
        else:
            volume_up = False
            
        # #Detect volume-down gesture
        if (middle_finger.y < index_finger.y - volume_down_threshold) and (ring_finger.y < index_finger.y - volume_down_threshold) and (pinky_finger.y < index_finger.y - volume_down_threshold):
            volume_down = True
        else:
            volume_down = False
        # Detect tab shifting gesture using both palms
        if abs(palm.x - wrist.x) > 0.1 and abs(palm.y - wrist.y) < 0.1:
            tab_shifting = True
        else:
            tab_shifting = False

        # Perform the click action
        if clicking:
            pyautogui.click()

        # Perform the scroll-up action
        if scrolling_up:
            pyautogui.scroll(500)  # Scroll up by 500 "clicks"

        # Perform the scroll-down action
        if scrolling_down:
            pyautogui.scroll(-500)  # Scroll down by 500 "clicks"
            
            # Perform the volume-up action
        if volume_up:
            pyautogui.press("volumeup")
        
        # Perform the volume-down action
        if volume_down:
            pyautogui.press("volumedown")  
            
        # Perform tab shifting action
        if tab_shifting:
            pyautogui.keyDown('ctrl')
            pyautogui.press('tab')
            pyautogui.keyUp('ctrl')

        # Follow Cursor:
        elif dist_threshold < hand_length * 0.02:
            x, y = int(index_finger.x *screen_width), int(index_finger.y *screen_height)
            pyautogui.moveTo(x, y)
    
    def perform_actions(self):
        if self.clicking:
            pyautogui.click()

        if self.scrolling_up:
            pyautogui.scroll(500)

        if self.scrolling_down:
            pyautogui.scroll(-500)

        if self.volume_up:
            pyautogui.press("volumeup")

        if self.volume_down:
            pyautogui.press("volumedown")

        if self.tab_shifting:
            pyautogui.keyDown('ctrl')
            pyautogui.press('tab')
            # pyautogui.keyUp('ctrl')