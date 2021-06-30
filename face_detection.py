# Face Detection using HAARCASCADES
import cv2
import numpy as np
import os

# downloading the default haarcascademodel xml files in cv2 directory
cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))
haar_model = os.path.join(cv2_base_dir, 'data/haarcascade_frontalface_default.xml')
faceCascade = cv2.CascadeClassifier(haar_model)
# faceCascade = cv2.CascadeClassfier("")
path = "images\DSCN5285.JPG"
img = cv2.imread(path)
rows, cols, channels = img.shape
print(rows, cols, channels)
aspRatio = int(cols/float(rows))
print(aspRatio)
IMG_HEIGHT = 720
imgResize = cv2.resize(img, (IMG_HEIGHT, IMG_HEIGHT * aspRatio))
imgGray = cv2.cvtColor(imgResize, cv2.COLOR_BGR2GRAY)

# detecting Faces using HAAR CASCADE
faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)

# bounding Boxes
for num, (x, y, w, h) in enumerate(faces):
    cv2.rectangle(imgResize, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv2.putText(imgResize, "Face: "+str(num+1), (x-10, y-10), cv2.FONT_ITALIC,
                0.5, (0, 0, 255), 2)

cv2.imshow('Image', imgResize)
cv2.waitKey(0)
