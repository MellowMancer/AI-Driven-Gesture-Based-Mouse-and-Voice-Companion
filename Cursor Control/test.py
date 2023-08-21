import cv2
import mediapipe as mp
import pyautogui
import math
from screeninfo import get_monitors

mp_drawing=mp.solutions.drawing_utils
mp_drawing_styles=mp.solutions.drawing_styles
mphands=mp.solutions.hands
pyautogui.FAILSAFE = False

monitor = get_monitors()[0]
screen_width, screen_height = monitor.width, monitor.height

cap=cv2.VideoCapture(0)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# cap.set(3, frame_width)
# cap.set(4, frame_height)
hands=mphands.Hands()

while True:
    data,image=cap.read()
    image=cv2.cvtColor(cv2.flip(image,1),cv2.COLOR_BGR2RGB)
    results=hands.process(image)
    image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    height, width, _ = image.shape

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,mphands.HAND_CONNECTIONS)
            index_finger = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
            middle_finger = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP]
            thumb = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]
            wrist = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.WRIST]
            palm = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_MCP]

            dist_threshold = math.pow((index_finger.y - middle_finger.y), 2) + math.pow((index_finger.x - middle_finger.x), 2)
            dist_middle_finger = math.pow((palm.y - middle_finger.y), 2) + math.pow((palm.x - middle_finger.x), 2)
            dist_index_finger = math.pow((palm.y - index_finger.y), 2) + math.pow((palm.x - index_finger.x), 2)
            click_threshold = math.pow((thumb.y - index_finger.y), 2) + math.pow((thumb.x - index_finger.x), 2)
            hand_length = math.pow((wrist.y - middle_finger.y), 2) + math.pow((wrist.x - middle_finger.x), 2)
            
            
            index_finger.x -= 0.5
            index_finger.y -= 0.5
            
            # if abs(index_finger.x) > frame_width/2-50:
            #     index_finger.x = (frame_width/2-50)*abs(index_finger.x)/index_finger.x

            # if abs(index_finger.y) > frame_height/2-50:    
            #     index_finger.y = (frame_height/2-50)*abs(index_finger.y)/index_finger.y

            index_finger.x = (1.5-abs(index_finger.x)/2)*index_finger.x
            index_finger.y = (1.5-abs(index_finger.y))*index_finger.y
            # print(index_finger.x, index_finger.y)
            index_finger.x += 0.5
            index_finger.y += 0.5
            # if index_finger.y < 100:
            #     index_finger.y = 0
            # elif index_finger.y >= 100 and index_finger.y < frame_height-100:
            #     index_finger.y = (index_finger.y-100)*frame_height
            # else:
            #     index_finger.y = frame_height-100

            # if index_finger.x < 100:
            #     index_finger.x = 0
            # elif index_finger.x >= 100 and index_finger.x < frame_width-100:
            #     index_finger.x = index_finger.x - 100
            # else:
            #     index_finger.x = frame_width-100
            
            #Click:
            if click_threshold < hand_length*0.06 and dist_threshold < hand_length*0.02:
                pyautogui.click()
            
            #Follow Cursor:
            elif dist_threshold < hand_length*0.02:
                x, y = int(index_finger.x * screen_width), int(index_finger.y * screen_height)
                pyautogui.moveTo(x, y)

            



    cv2.imshow('Handtracker',image)
    cv2.waitKey(1)    
    
    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break