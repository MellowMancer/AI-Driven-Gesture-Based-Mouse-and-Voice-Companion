import cv2
import mediapipe as mp
import pyautogui
import math
from screeninfo import get_monitors

mp_drawing = mp.solutions.drawing_utils
mphands = mp.solutions.hands
pyautogui.FAILSAFE = False

monitor = get_monitors()[0]
screen_width, screen_height = monitor.width, monitor.height

cap = cv2.VideoCapture(0)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
hands = mphands.Hands()

# Initialize variables to track hand gestures
clicking = False
scrolling_up = False
scrolling_down = False
tab_shifting = False  # Initialize a variable to track tab shifting gesture
volume_up = False
volume_down = False
# Set thresholds for the finger positions
scroll_up_threshold = 0.2  # Threshold for index finger to trigger scroll up
scroll_down_threshold = 0.2  # Threshold for pinky finger to trigger scroll down

volume_up_threshold = 0.2  # Threshold for index finger to trigger volume up
volume_down_threshold = 0.2  # Threshold for pinky finger to trigger volume down

while True:
    data, image = cap.read()
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height, width, _ = image.shape

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks, mphands.HAND_CONNECTIONS)
            index_finger = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
            middle_finger = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP]
            pinky_finger = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.PINKY_TIP]
            thumb = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]
            wrist = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.WRIST]
            palm = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_MCP]
            ring_finger = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.RING_FINGER_TIP]

            dist_threshold = math.pow((index_finger.y - middle_finger.y), 2) + math.pow((index_finger.x - middle_finger.x), 2)
            dist_pinky_finger = math.pow((pinky_finger.y - middle_finger.y), 2) + math.pow((pinky_finger.x - middle_finger.x), 2)
            hand_length = math.pow((wrist.y - middle_finger.y), 2) + math.pow((wrist.x - middle_finger.x), 2)

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
            if abs(palm.x - wrist.x) > 0.1 and abs(palm.y - wrist.y) > 0.1:
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
                x, y = int(index_finger.x * screen_width), int(index_finger.y * screen_height)
                pyautogui.moveTo(x, y)

    cv2.imshow('Handtracker', image)
    cv2.waitKey(1)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
