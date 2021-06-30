# creating a virtual paint
import cv2
import numpy as np

frameWidth = 1024
frameHeight = 720
brightness = 100
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, brightness)
# Points
myPoints = []  # [x, y, ColorId]
# list of Colors
myColors_dict = {'Blue': ([98, 135, 147, 226, 200, 255], (255, 0, 0))}
# 'Orange': [0, 39, 131, 245, 155, 255]}
# 'Blue': [98, 135, 147, 226, 200, 255]}
# draw on Canvas
myColorValues = [[255, 0, 0]]


def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10,
                   myColorValues[point[2]], cv2.FILLED)

# defining a method for finding colors


def findColor(img, myColors_dict):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for key in myColors_dict:
        lower = np.array(myColors_dict[key][0][:3])
        upper = np.array(myColors_dict[key][0][3:])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = getContours(mask)
        if x != 0 and y != 0:
            newPoints.append([x, y, count])
        count += 1
        cv2.circle(imgResult, (x, y), 10, myColors_dict[key][1], cv2.FILLED)
        # cv2.imshow(key, mask)
    return newPoints
# Conotour Function


def getContours(img):
    x, w, y = 0, 0, 0
    contours, hirearchy = cv2.findContours(img, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 10:
            # cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2, y


while True:
    _, frame = cap.read()
    imgResult = frame.copy()
    newPoints = findColor(frame, myColors_dict)
    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)
    if myPoints != 0:
        drawOnCanvas(myPoints, myColorValues)

    cv2.imshow('frame', imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # find the colors

# releasing the capture
cap.release()

cv2.destroyAllWindows()
