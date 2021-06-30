import numpy as np
import cv2

# Reading Image
img = cv2.imread('images\lena.jpg')


# Viewing Image
cv2.imshow('Image', img)


# closing window on click
cv2.waitKey(0)
