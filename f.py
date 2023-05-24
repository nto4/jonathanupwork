import cv2
import numpy as np
import imutils

cv2.namedWindow('image', cv2.WINDOW_NORMAL)

img = cv2.imread('1.jpeg')
ratio = img.shape[0] / 300.0
img = imutils.resize(img, height = 800)
blur = cv2.GaussianBlur(img,(7,7),0)
gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
mask = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
canny = cv2.Canny(mask, 30, 200)
(cnts, _) = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    if len(approx) == 4:
        cv2.drawContours(img, [approx], -1, (0, 0, 255), 1)


cv2.imshow('result', img)
cv2.waitKey(0)
cv2.destroyAllWindows()