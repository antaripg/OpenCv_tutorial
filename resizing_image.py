import cv2


# reading image
img = cv2.imread('images\Dog0.jpg')
print(img.shape)
# resizing and image --> width, height, channel
imgResize = cv2.resize(img, (300, 200))

# image cropping --> height,width, channel
imgCropped = img[:250, 100:300]

cv2.imshow('dog', img)
cv2.imshow('dog_resized', imgResize)
cv2.imshow('dog_cropped', imgCropped)


cv2.waitKey(0)
