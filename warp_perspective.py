import cv2
import numpy as np


img = cv2.imread("images\deck_cards.jpg")


# four corner points
width, height = 250, 400
pts1 = np.float32([[240, 44], [140, 279], [357, 118], [267, 355]])
pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
matrix = cv2.getPerspectiveTransform(pts1, pts2)

imgOutput = cv2.warpPerspective(img, matrix, (width, height))


cv2.imshow("Cards", img)
cv2.imshow("Warped Cards", imgOutput)

cv2.waitKey(0)
