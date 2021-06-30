import cv2
import numpy as np

img = np.zeros((512, 512, 3), np.uint8)
print(img.shape)  # height, width, channel


# img[:] = (255, 255, 0)

# create Lines -- width, height
cv2.line(img, (0, 0), (img.shape[1], img.shape[0]), (0, 255, 0), 3)

# create a rectngle
cv2.rectangle(img, (250, 10), (430, 90), (0, 0, 255), 2)  # cv2.FILED

# create a circle
cv2.circle(img, (300, 50), 30, (255, 255, 0), 5)
cv2.circle(img, (300, 50), 5, (0, 255, 255), 5)
cv2.circle(img, (380, 50), 30, (255, 255, 0), 5)
cv2.circle(img, (380, 50), 5, (0, 255, 255), 5)


# putting text on images
cv2.putText(img, "OpenCV tutorial", (220, 120), cv2.FONT_HERSHEY_COMPLEX,
            1, (0, 150, 150), 4)


cv2.imshow('Image', img)

cv2.waitKey(0)
