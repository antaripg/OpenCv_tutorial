import numpy as np
import cv2


# Reading Video
cap = cv2.VideoCapture('images\output.avi')


# VIewing Video
while True:
    sucess, img = cap.read()
    cv2.imshow('Video', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
