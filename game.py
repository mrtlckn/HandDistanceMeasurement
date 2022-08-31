import cv2
from cvzone.HandTrackingModule import HandDetector
import math
import numpy as np
import cvzone
#Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280) #width
cap.set(4, 720) #height

# 1-Find or declare the hand detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# 2.2 Find Function basically relate x and y
# x is the raw distance y is the value in cm
x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
#PolynomialFunction for calibration (raw distance(pixel) and cm)
# we need to plot this graph for find relationship
# we already drawed, this is a quadratic function
coff = np.polyfit(x, y, 2)  # y = Ax^2 + Bx + C

# 3- Game Variables
cx, cy = 250,250
color = (255,0,255)

#Loop
while True:
    success, img = cap.read()
    #hands, img = detector.findHands(img)
    hands = detector.findHands(img, draw=False) #hand points will not draw
    # 2- Measurement
    if hands:
        #hands[0] #first element means first hand, we have just one hand
        lmList = hands[0]['lmList'] #lmList give us the list of all the points
        x, y, w, h = hands[0]['bbox']
        #print(lmList)
        # What exactly we need which point number? check it media pipe website
        # 5 and 17 points!
        x1,y1 = lmList[5]
        x2, y2 = lmList[17]

        #2.1 - diagonal distance
        distance = int(math.sqrt((y2-y1)**2 + (x2-x1)**2))
        #2.2 - calibration (distance to cm)
        A, B, C = coff
        distanceCM = A * distance**2 + B * distance + C
        #final print!
        #print(abs(distanceCM), distance)

        # 3.3- Logic
        if distanceCM < 40:
            if x < cx < x+w and y < cy < y+h:
                color = (0,255,0)
        else:
                color = (255,0,255)

        cv2.rectangle(img, (x,y), (x+w , y+h), (255,0,255),3)
        cvzone.putTextRect(img, f'{int(distanceCM)} cm', (x+5, y-10))

    #3.1- Draw Button
    cv2.circle(img, (cx, cy), 30, color, cv2.FILLED)
    cv2.circle(img, (cx, cy), 10, (255,255,255), cv2.FILLED)
    cv2.circle(img, (cx, cy), 20, (255, 255, 255), 2)
    cv2.circle(img, (cx, cy), 30, (50, 50, 50), 2)

    #3.2- Game HUD
    cvzone.putTextRect(img,'Time : 30', (1000, 75), scale=3, offset=20)
    cvzone.putTextRect(img, 'Score : 4', (60, 75), scale=3, offset=20)


    cv2.imshow('Image', img)
    cv2.waitKey(1)