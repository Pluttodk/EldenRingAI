"""
This will be the main file containing the structure of the program

The program will work the following way:


1: Read the web cam

2: Detect facial features

3: Map features to key movements

4: Map features into elden ring moves:

5: Run the program and HAVE FUN!!!
"""

# Lets get the basic of the facial recognition up and running!

import cv2, numpy as np
import pydirectinput
from pywinauto import keyboard

def draw_introduction(frame):
    """
    We fill the area with various colors to show how the game works

    """
    height, width = frame.shape[:2]

    lx,ly = 0,0
    mx,my = int(width*0.33), int(height*0.5)
    mid_x, mid_y = int(width*0.66), int(height*0.5)

    #Left
    cv2.rectangle(frame, (0,0), (mx,height), (0,255,0), thickness=2)

    # Top
    cv2.rectangle(frame, (mx,0), (mid_x,mid_y), (255,0,0), thickness=2)

    # Bottom
    cv2.rectangle(frame, (mx,my), (mid_x, height), (255,255,255), thickness=2)

    # Right
    cv2.rectangle(frame, (mid_x,0), (width,height), (0,0,255), thickness=2)


    return True



def elden_ring_moves(feature, frame, current_pressed):
    """
    Elden ring has the following moves:

    Moving [W,A,S,D]
        - Eyebrows?
            [Left raised eyebrow => A, Right raised eyebrow => D, Both raised => W, both lowered => S]
        - Proof of concept we make it based on face location?
            Top center (W)
            Left (A)
            Bottom center (S)
            Right (D)
    Sprint [ALT]
        - TODO
    Jump [F]
        - TODO
    Dodge [SPACE]
        - TODO
    Simple attack [LMB]
        - Smile with closed mouth
    Strong attack [SHIFT + LMB]
        - Smile with open mouth
    Guard [RMB]
        - Squeeze mouth together?
    Skill [SHIFT+RMB]
        - Squeeze mouth together openly?
    So a total of 11 different features that we need to map:
    """
    (x,y,w,h) = feature

    cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), thickness=2)

    # which direction to move
    height, width = list(frame.shape)[:2]
    xc, yc = x+(w//2), y+(h//2)
    if xc < 0.33 * width: 
        # We are left pos
        print("MOVE LEFT")
        should_press = "left"
    elif xc > 0.66*width:
        # We are right pos
        print("MOVE RIGHT")
        should_press = "right"
    elif yc >= 0.5 * height:
        # We move back
        print("MOVE BACKWARDS")
        should_press = "down"
    else:
        # We move forward
        print("MOVE FORWARD")
        should_press = "up"
    if current_pressed != should_press:
        pydirectinput.keyUp(current_pressed)
        pydirectinput.keyDown(should_press)

    return should_press


video_capture = cv2.VideoCapture(1)
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

should_start_game = False
current_press = "down"
while True:
    ret, frame = video_capture.read()
    if ret:
        frame = cv2.flip(frame, 1)
        if should_start_game:
            # Make image gray scale
            gray_face = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect face
            faces = faceCascade.detectMultiScale(gray_face, scaleFactor=1.1, minNeighbors=9)

            # Draw rectangle on face
            if len(faces):
                # We take only first face
                features = faces[0]
                current_press = elden_ring_moves(features, frame, current_press)
        else:
            draw_introduction(frame)

        # Show image
        cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('s'):
        if should_start_game:
            break
        # Press s to start the game
        should_start_game = True



video_capture.release()
cv2.destroyAllWindows()

