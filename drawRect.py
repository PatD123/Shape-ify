import mediapipe as mp
import math
import cv2 as cv
import numpy as np

from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2
from Rectangle import Rectangle
from Line import Line

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

IMAGE_WIDTH = 1280
IMAGE_HEIGHT = 720

shapes = []
screen_shapes = []

prev_x = 0
prev_y = 0
top_left = []
top_right = []

two_hand_closed = False
one_hand_closed = False

hand_locked = -1

shape_choice = 1

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

def midpt(p1, p2):
    midx = int((p1[0] + p2[0]) / 2)
    midy = int((p1[1] + p2[1]) / 2)
    return midx, midy

def display_shape(image, shape):
    if shape.type == "Rectangle":
        cv.rectangle(image,shape.top_left,shape.bot_right,shape.color,shape.line_width)
    elif shape.type == "Line":
        cv.line(image, shape.p1, shape.p2, shape.color, shape.line_width)

def display_screen_names(image):
    for shape in screen_shapes:
        cv.putText(image, shape.name, (IMAGE_WIDTH - shape.bot_right[0] + 20, shape.top_left[1] + 30), cv.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

def render(image, landmarks):
    global hand_locked
    dis_x = 0
    dis_y = 0
    midx = -1
    midy = -1
    if landmarks:
        midx, midy = midpt(landmarks[0], landmarks[1])
        dis_x = midx - prev_x
        dis_y = midy - prev_y
    
    for i in range(len(shapes)):
        shape = shapes[i]
        if one_hand_closed and shape.on_segment([midx, midy]) or hand_locked == i:
            hand_locked = i
            shape.move(dis_x, dis_y)

        display_shape(image, shape)

    for screen_shape in screen_shapes:
        if landmarks:
            if screen_shape.in_rectangle(landmarks[1]):
                shapes.clear()
        display_shape(image, screen_shape)
    
    return image
    
if __name__ == "__main__":
    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

    # Create the permanent screen shapes
    del_button = Rectangle([1150, 0], [1280, 50], (255, 0, 0), 3, "Delete")
    screen_shapes.append(del_button)

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

                    #cv.circle(image,(int(p_x),int(p_y)), 40, (0,0,255), -1)

                    landmarks.append([int(t_x), int(t_y)])
                    landmarks.append([int(p_x), int(p_y)])

                    image = hand_viz(image, hand_landmarks)
            
            # Creating a rectangle with two hands, 4 landmarks
            if len(landmarks) == 4:
                if math.dist(landmarks[0], landmarks[1]) < 50 and math.dist(landmarks[2], landmarks[3]) < 50:
                    l_midx, l_midy = midpt(landmarks[0], landmarks[1])
                    r_midx, r_midy = midpt(landmarks[2], landmarks[3])
                    
                    if shape_choice == 0:
                        cv.rectangle(image,(l_midx, l_midy),(r_midx, r_midy),(0,255,0),3)
                    else:
                        cv.line(image,(l_midx, l_midy),(r_midx, r_midy),(0,255,0),3)

                    two_hand_closed = True

                    top_left = [l_midx, l_midy]
                    top_right = [r_midx, r_midy]
                elif two_hand_closed:
                    two_hand_closed = False
                    shape = None
                    if shape_choice == 0:
                        shape = Rectangle(top_left, top_right, (0, 255, 0), 3)
                    else:
                        shape = Line(top_left, top_right, (0, 255, 0), 3)
                    shapes.append(shape)

            # Dragging a rectangle with one hand, 2 landmarks
            if len(landmarks) == 2:
                if math.dist(landmarks[0], landmarks[1]) < 80:
                    if not one_hand_closed:
                        prev_x, prev_y = midpt(landmarks[0], landmarks[1])
                        one_hand_closed = True
                else:
                    one_hand_closed = False
                    hand_locked = -1
            else:
                one_hand_closed = False
                hand_locked = -1

            image = render(image, landmarks)
            image = cv.flip(image, 1)

            display_screen_names(image)

            if landmarks:
                prev_x, prev_y = midpt(landmarks[0], landmarks[1])

            # Flip the image horizontally for a selfie-view display.
            cv.imshow('MediaPipe Hands', image)
            if cv.waitKey(5) & 0xFF == 27:
                break

    cap.release()