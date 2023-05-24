import cv2
import numpy as np
import imutils

cv2.namedWindow('image', cv2.WINDOW_NORMAL)

img = cv2.imread('h.jpeg')
ratio = img.shape[0] / 300.0
img = imutils.resize(img, height = 800)

# convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# threshold
thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)[1]

# apply close morphology
kernel = np.ones((111,111), np.uint8)
morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

# invert so rectangle is white
morph = 255 - morph

# get largest contour and draw on copy of input
result = img.copy()
contours = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]
big_contour = max(contours, key=cv2.contourArea)
cv2.drawContours(result, [big_contour], 0, (255,255,255), 1)

# write result to disk
cv2.imwrite("black_rectangle_outline_thresh.png", thresh)
cv2.imwrite("black_rectangle_outline_morph.png", morph)
cv2.imwrite("black_rectangle_outline_result.png", result)

# display results
cv2.imshow("THRESH", thresh)
cv2.imshow("MORPH", morph)
cv2.imshow("RESULT", result)
cv2.waitKey(0)
cv2.destroyAllWindows()