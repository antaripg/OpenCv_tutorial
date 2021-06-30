# Document scanner

import cv2
import numpy as np
import time
from datetime import datetime
import os


# Create a directory to save scanned images
def createDirectory():
    imgDir = 'scanned_images'
    dirPath = os.path.dirname(os.path.realpath(__file__))
    try:
        os.mkdir(os.path.join(dirPath, imgDir))
    except OSError as e:
        print(e)

# Reorded the contour points


def reorder(myPoints):
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), np.int32)
    add = myPoints.sum(axis=1)
    # print("add", add)
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    # print("NewPoints", myPointsNew)
    return myPointsNew

# Warp Perspective


def getWarp(img, biggest, widthImg, heightImg):
    try:
        biggest = reorder(biggest)
        # print(biggest.shape)
        pts1 = np.float32(biggest)
        pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg],
                           [widthImg, heightImg]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        imgOutput = cv2.warpPerspective(img, matrix,
                                        (widthImg, heightImg))

        return imgOutput
    except ValueError as e:
        pass

# Edge Detection Pre-processing


def preProcessing(img):
    kernel = np.ones((5, 5))
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, 200, 200)  # Edge Detection
    imgDilate = cv2.dilate(imgCanny, kernel, iterations=2)  # Dilation
    # imgDilate = cv2.dilate(imgCanny, kernel, iteration=2)  # Dilation
    imgThresh = cv2.erode(imgDilate, kernel, iterations=1)
    return imgThresh

# Getting Contours


def getContours(img, imgContour, contourArea):

    biggest = np.array([])
    maxArea = 0
    contours, hirearchy = cv2.findContours(img, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > contourArea:
            # cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            if area > maxArea and len(approx) == 4:
                biggest = approx
                maxArea = area
                # x, y, w, h = cv2.boundingRect(biggest)
                # cv2.rectangle(imgContour, (x, y), (x+w, y+h), (255, 0, 0), 3)
    cv2.drawContours(imgContour, biggest, -1, (255, 0, 0), 20)

    return biggest


def main():
    createDirectory()
    widthImg, heightImg = 640, 480
    brightness = 100
    defaultMsg = "Checking for Scannable Object \n Please Wait"
    cap = cv2.VideoCapture(0)
    cap.set(3, widthImg)
    cap.set(4, heightImg)
    cap.set(10, brightness)

    while(1):
        _, frame = cap.read()
        area = 1000
        img = cv2.resize(frame, (widthImg, heightImg))
        imgContour = img.copy()
        defaultImg = img.copy()
        defaultImg = cv2.putText(defaultImg, defaultMsg,
                                 (60, heightImg//2),
                                 cv2.FONT_HERSHEY_COMPLEX, 1,
                                 (255, 255, 255), 2)
        # cv2.imshow('Image', img)
        imgThresh = preProcessing(img)
        biggest = getContours(imgThresh, imgContour, area)
        cv2.imshow('ImageThresh', imgContour)
        try:
            imgWarped = getWarp(img, biggest, widthImg, heightImg)
            cv2.imshow('Result', imgWarped)
        except Exception as e:
            cv2.imshow('Result', defaultImg)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            try:
                time.sleep(1)
                timeNow = datetime.now()
                timeNow_str = timeNow.strftime("%d-%m_%Y_%H_%M_%S")
                savePath = 'scanned_images/Scanned_image_{}.jpg'.format(timeNow_str)
                cv2.imwrite(savePath, imgWarped)
                break
            except Exception as e:
                break
    cap.release()
    cv2.destroyAllWindows()

# calling the main class


if __name__ == "__main__":
    main()
