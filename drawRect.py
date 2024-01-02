import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2
from Rectangle import Rectangle
import math
import cv2 as cv

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

IMAGE_WIDTH = 1280
IMAGE_HEIGHT = 720

shapes = []

def rescale(x, y):
    disp_width = 540 - 80
    disp_height = 320 - 0

    x -= 80
    new_x = 1920 - x * 2000 / disp_width
    new_y = y * 1100 / disp_height
    return new_x, new_y

def hand_viz(image, hand_landmarks):

    # Visualizing landmarks
    mp_drawing.draw_landmarks(
        image,
        hand_landmarks,
        mp_hands.HAND_CONNECTIONS,
        mp_drawing_styles.get_default_hand_landmarks_style(),
        mp_drawing_styles.get_default_hand_connections_style())
    
    return image

def render(image):
    for shape in shapes:
        cv.rectangle(image,shape.top_left,shape.bot_right,(0,255,0),3)
    
    return image

# RENDER ALL SHAPES IN A RENDER FUNCTION
# FOR ALL RECTANGLES, CHECK WHETHER ON_SEG
#       IF ON SEG, REDO LOCK HAND 
#       AFTER LOCK, MOVE COORDS OF REC BASED ON PREV LOC

# HAVE TO FIGURE OUT A WAY TO UNLOCK HAND FROM A RECTANGLE
# AND HAVE THE RECTANGLE STAY IN ITS NEW LOCATION.

cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

prev_x = 0
prev_y = 0
rec_top_left = []
rec_top_right = []

two_hand_closed = False
one_hand_closed = False

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv.cvtColor(image, cv.COLOR_RGB2BGR)

    landmarks = []
    if results.multi_hand_landmarks:

        # Visualizing Hand Landmarks
        for hand_landmarks in results.multi_hand_landmarks:
        
            # Thumb pointer
            t_x = hand_landmarks.landmark[4].x * IMAGE_WIDTH
            t_y = hand_landmarks.landmark[4].y * IMAGE_HEIGHT

            # Index pointer
            p_x = hand_landmarks.landmark[8].x * IMAGE_WIDTH
            p_y = hand_landmarks.landmark[8].y * IMAGE_HEIGHT

            # Store prev so we can move a chosen shape
            prev_x = int((t_x + p_x) / 2)
            prev_y = int((t_y + p_y) / 2)

            #cv.circle(image,(int(p_x),int(p_y)), 40, (0,0,255), -1)

            landmarks.append([int(t_x), int(t_y)])
            landmarks.append([int(p_x), int(p_y)])

            image = hand_viz(image, hand_landmarks)
    
    if len(landmarks) == 4:
        if math.dist(landmarks[0], landmarks[1]) < 60 and math.dist(landmarks[2], landmarks[3]) < 60:
            l_midx = int((landmarks[0][0] + landmarks[1][0]) / 2)
            l_midy = int((landmarks[0][1] + landmarks[1][1]) / 2)
            r_midx = int((landmarks[2][0] + landmarks[3][0]) / 2)
            r_midy = int((landmarks[2][1] + landmarks[3][1]) / 2)
            cv.rectangle(image,(l_midx, l_midy),(r_midx, r_midy),(0,255,0),3)

            two_hand_closed = True

            rec_top_left = [l_midx, l_midy]
            rec_top_right = [r_midx, r_midy]
    elif two_hand_closed:
        two_hand_closed = False
        rect = Rectangle(rec_top_left, rec_top_right, 3)
        shapes.append(rect)

    image = render(image)

    # Flip the image horizontally for a selfie-view display.
    cv.imshow('MediaPipe Hands', cv.flip(image, 1))
    if cv.waitKey(5) & 0xFF == 27:
      break
cap.release()
    
