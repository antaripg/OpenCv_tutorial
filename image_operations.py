# Operating on Images
import cv2
import numpy as np

img = cv2.imread("images\lena.jpg")

# dilation kernel
kernel = np.ones((5, 5), np.uint8)
# gray scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Blur
# Gaussian Blur
blur = cv2.GaussianBlur(gray, (7, 7), 0)

# Canny EdgeDetector
canny = cv2.Canny(img, 200, 150)

# Dilation
dilate = cv2.dilate(canny, kernel, iterations=1)

# Erosion
eroded = cv2.erode(dilate, kernel, iterations=1)

# cv2.imshow('img', img)
cv2.imshow('gray', gray)
cv2.imshow('blur', blur)
cv2.imshow('Canny', canny)
cv2.imshow('Dilated Image', dilate)
cv2.imshow('Eroded Image', eroded)

cv2.waitKey(0)
