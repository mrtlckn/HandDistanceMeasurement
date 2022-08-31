import cv2
from cvzone.HandTrackingModule import HandDetector
import math

#Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280) #width
cap.set(4, 720) #height

# 1-Find or declare the hand detector
detector = HandDetector(detectionCon=0.8, maxHands=1)


#Loop
while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)

    # 2- Measurement
    if hands:
        #hands[0] #first element means first hand, we have just one hand
        lmList = hands[0]['lmList'] #lmList give us the list of all the points
        #print(lmList)
        # What exactly we need which point number? check it media pipe website
        # 5 and 17 points!
        x1,y1 = lmList[5]
        x2, y2 = lmList[17]

        #2.1 - diagnoal distance
        distance = int(math.sqrt((y2-y1)**2 + (x2-x1)**2))
        #2.2 - calibration (distance to cm)
        #
        print(abs(x2-x1), distance)

    cv2.imshow('Image', img)
    cv2.waitKey(1)