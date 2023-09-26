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
        ring_finger = hand_landmarks.landmark[mphands.RING_FINGER_TIP]
        knuckle = hand_landmarks.landmark[mphands.MIDDLE_FINGER_MCP]

        dist_threshold = math.pow((index_finger.y - middle_finger.y), 2) + math.pow((index_finger.x - middle_finger.x), 2)
        hand_length = math.pow((wrist.y - middle_finger.y), 2) + math.pow((wrist.x - middle_finger.x), 2)

        scroll_threshold = 0.075  # Threshold for index finger to trigger scroll up
        scroll_down_threshold = 0.2  # Threshold for pinky finger to trigger scroll down

        volume_up_threshold = 0.2  # Threshold for index finger to trigger volume up
        volume_down_threshold = 0.2  # Threshold for pinky finger to trigger volume down

        monitor = get_monitors()[0]
        screen_width, screen_height = monitor.width, monitor.height
        
        # Check if all four fingers are detected
        # if (index_finger.y < knuckle.y) and (middle_finger.y > knuckle.y) and (pinky_finger.y > knuckle.y) and (ring_finger.y > knuckle.y) and thumb.x < index_finger.x:
        #     left_clicking = True
        #     follow_cursor = True
        # else:
        #     left_clicking = False

        # Detect scroll-up gesture
        if abs(index_finger.y - knuckle.y) < scroll_threshold and abs(middle_finger.y - knuckle.y) < scroll_threshold and abs(pinky_finger.y - knuckle.y) < scroll_threshold and abs(ring_finger.y - knuckle.y) < scroll_threshold:
            scrolling = True
        else:
            scrolling = False
            
        #Detect volume-up gesture
        if (middle_finger.y < knuckle.y) and (index_finger.y < knuckle.y) and (ring_finger.y < knuckle.y) and (pinky_finger.y > knuckle.y):
            volume_up = True
        else:
            volume_up = False
            
        # #Detect volume-down gesture
        if (middle_finger.y < knuckle.y) and (ring_finger.y < knuckle.y) and (pinky_finger.y < knuckle.y) and (index_finger.y > knuckle.y):
            volume_down = True
        else:
            volume_down = False
        # # Detect tab shifting gesture using both palms
        # if abs(knuckle.x - wrist.x) > 0.1 and abs(knuckle.y - wrist.y) < 0.1:
        #     tab_shifting = True
        # else:
        #     tab_shifting = False

        # if dist_threshold < hand_length * 0.02 and (index_finger.y < knuckle.y) and (middle_finger.y < knuckle.y) and (ring_finger.y > knuckle.y) and (pinky_finger.y > knuckle.y):
        #     follow_cursor = True
        # else:
        #     follow_cursor = False

        # Perform the click action
        # if left_clicking:
        #     pyautogui.click()

        # Perform the scroll-up action
        if scrolling:
            scroll = 4000*(index_finger.y - knuckle.y)
            pyautogui.scroll(int(scroll))  # Scroll up by 500 "clicks"
            print(int(scroll))
        # Perform the scroll-down action
        # elif scrolling_down:
        #     pyautogui.scroll(-500)  # Scroll down by 500 "clicks"
            
            # Perform the volume-up action
        # elif volume_up:
        #     pyautogui.press("volumeup")
        
        # # Perform the volume-down action
        # elif volume_down:
        #     pyautogui.press("volumedown")  
            
        # # Perform tab shifting action
        # elif tab_shifting:
        #     pyautogui.keyDown('ctrl')
        #     pyautogui.press('tab')
        #     pyautogui.keyUp('ctrl')

        # # Follow Cursor:
        # if follow_cursor:
        #     x, y = int(index_finger.x *screen_width*1.2 - 100), int(index_finger.y *screen_height*1.2 - 100)
        #     pyautogui.moveTo(x, y)
    
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