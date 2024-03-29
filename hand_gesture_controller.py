# hand_gesture_controller.py

import math
import pyautogui
import hand_tracker as HandTracker
from screeninfo import get_monitors
import screen_brightness_control as sbc
import time

class HandGestureController:
    def __init__(self):
        self.left_clicking = False
        self.right_clicking = False
        self.scrolling = False
        self.tab_shifting = False
        self.volume_up = False
        self.volume_down = False
        self.follow_cursor = False
        self.hold = False
        self.minimize = False
        self.on_screen_keyboard = False

        self.index_finger = None
        self.knuckle = None
        

    def dist(self, p1, p2):
        return (math.pow((p1.x - p2.x), 2) + math.pow((p1.y - p2.y), 2))

    def detect_gestures(self, mphands, hand_landmarks):
        scaling_factor = 1.5  # Scaling factor depends on the distance of hand from the camera
        
        self.index_finger = hand_landmarks.landmark[mphands.INDEX_FINGER_TIP]
        middle_finger = hand_landmarks.landmark[mphands.MIDDLE_FINGER_TIP]
        pinky_finger = hand_landmarks.landmark[mphands.PINKY_TIP]
        thumb = hand_landmarks.landmark[mphands.THUMB_TIP]
        wrist = hand_landmarks.landmark[mphands.WRIST]
        ring_finger = hand_landmarks.landmark[mphands.RING_FINGER_TIP]
        self.knuckle = hand_landmarks.landmark[mphands.MIDDLE_FINGER_MCP]

        dist_threshold = self.dist(self.index_finger, middle_finger)
        hand_length = math.pow((wrist.y - middle_finger.y), 2) + math.pow((wrist.x - middle_finger.x), 2)

        scroll_threshold = 0.1  # Threshold for index finger to trigger scroll up
        count = 0

        # Check if four fingers are raised
        if (self.index_finger.y < self.knuckle.y) and (middle_finger.y > self.knuckle.y) and (pinky_finger.y > self.knuckle.y) and (ring_finger.y > self.knuckle.y) and thumb.x < self.index_finger.x:
            self.left_clicking = True
        else:
            self.left_clicking = False
            self.hold = False

        # Check for fist gesture
        if (self.dist(self.index_finger, middle_finger)) < 0.08 * hand_length and (self.dist(middle_finger, ring_finger)) < 0.08 * hand_length and (self.dist(pinky_finger, ring_finger)) < 0.08 * hand_length and (self.dist(middle_finger, wrist)) < 0.08 * hand_length:
            print("right click")
            self.right_clicking = True
        else:
            self.right_clicking = False

        # Detect scroll gesture
        if abs(self.index_finger.y - self.knuckle.y) < scroll_threshold and abs(middle_finger.y - self.knuckle.y) < scroll_threshold and abs(pinky_finger.y - self.knuckle.y) < scroll_threshold and abs(ring_finger.y - self.knuckle.y) < scroll_threshold and (self.index_finger.y - self.knuckle.y)*(middle_finger.y - self.knuckle.y)*(pinky_finger.y - self.knuckle.y)*(ring_finger.y - self.knuckle.y) > 0 and (pinky_finger.x -self.index_finger.x) < 10 and self.minimize == False:
            self.scrolling = True
        else:
            self.scrolling = False
            
        #Detect volume-up gesture
        if (self.dist(self.index_finger, thumb)) > 0.08 * hand_length and (middle_finger.y < self.knuckle.y) and (self.index_finger.y < self.knuckle.y) and (ring_finger.y < self.knuckle.y) and (pinky_finger.y > self.knuckle.y):
            self.volume_up = True
        else:
            self.volume_up = False
            
        # #Detect volume-down gesture
        if (middle_finger.y < self.knuckle.y) and (ring_finger.y < self.knuckle.y) and (pinky_finger.y < self.knuckle.y) and (self.index_finger.y > self.knuckle.y):
            self.volume_down = True
        else:
            self.volume_down = False

        # Detect minimize gesture
        if (self.dist(self.index_finger, thumb)) < 0.08 * hand_length and (self.dist(middle_finger, thumb)) < 0.08 * hand_length and (self.dist(pinky_finger, thumb)) < 0.08 * hand_length and (self.dist(ring_finger, thumb)) < 0.08 * hand_length:
            self.minimize = True
        else:
            self.minimize = False

        # Detect on-screen keyboard gesture
        if (self.dist(self.index_finger, thumb)) < 0.08 * hand_length and (middle_finger.y < self.knuckle.y) and (self.index_finger.y > self.knuckle.y) and (ring_finger.y < self.knuckle.y) and (pinky_finger.y < self.knuckle.y):
            self.on_screen_keyboard = True
            print("onscreen keyboard")
        else:
            self.on_screen_keyboard = False
        
        # Detect tab shifting gesture using both palms
        if abs(self.knuckle.x - wrist.x) > hand_length * 0.02 and abs(self.knuckle.y - wrist.y) < hand_length * 0.5:
            self.tab_shifting = True
        else:
            self.tab_shifting = False

        if dist_threshold < hand_length * 0.02 and (self.index_finger.y < self.knuckle.y) and (middle_finger.y < self.knuckle.y) and (ring_finger.y > self.knuckle.y) and (pinky_finger.y > self.knuckle.y):
            self.follow_cursor = True
        else:
            self.follow_cursor = False

    
    def perform_actions(self):
        pyautogui.FAILSAFE = False
        monitor = get_monitors()[0]
        screen_width, screen_height = monitor.width, monitor.height

        # if self.hold:
        #     pyautogui.mouseDown()
        #     x, y = int(self.index_finger.x *screen_width*1.3 - 100), int(self.index_finger.y *screen_height*1.4 - 150)
        #     pyautogui.moveTo(x, y, 0.05)
        # else:
        #     pyautogui.mouseUp()

        # Perform the click action
        if self.left_clicking:
            pyautogui.click()

        # Perform the right-click action
        elif self.right_clicking:
            pyautogui.rightClick()

        # Perform the scroll action
        elif self.scrolling:
            scroll = -3200*(self.index_finger.y - self.knuckle.y)
            pyautogui.scroll(int(scroll))  # Scroll up/down based on the distance of index finger from the knuckle
            
        # Perform the volume-up action
        elif self.volume_up:
            pyautogui.press("volumeup")
        
        # # Perform the volume-down action
        elif self.volume_down:
            pyautogui.press("volumedown")  

        elif self.minimize:
            pyautogui.hotkey('win', 'm')
        elif self.on_screen_keyboard:
            pyautogui.keyDown('win')
            pyautogui.keyDown('ctrl')
            pyautogui.keyDown('o')
            pyautogui.keyUp('win')
            pyautogui.keyUp('ctrl')
            pyautogui.keyUp('o')

        
        # # Perform the brightness-up action
        # elif self.brightness_up:
        #     #increase brightness by 10%
        #     sbc.set_brightness('+10')
            
        # # Perform the brightness-down action    
        # elif self.brightness_down:
        #     #decrease brightness by 10%
        #     sbc.set_brightness('-10')      
         
             
            
        # Perform tab shifting action
        elif self.tab_shifting:
            pyautogui.keyDown('alt')
            pyautogui.press('tab')
            pyautogui.keyUp('alt')

        # Follow Cursor:
        if self.follow_cursor:
            x, y = int(self.index_finger.x *screen_width*1.3 - 100), int(self.index_finger.y *screen_height*2 - 300)
            pyautogui.moveTo(x, y, duration=0.08)