import cv2
import numpy as np

img = cv2.imread('samp_balanced.jpg')
img2 = cv2.imread('samp_balanced.jpg')
#cv2.sobel e bak 
img = cv2.medianBlur(img,55)
cv2.imwrite('op_med.jpg', img)
kernel = np.ones((20,20),np.uint8)
img = cv2.erode(img,kernel,iterations = 1)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(gray, 0, 80)
contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

max_area = 0
max_contour = None

for cnt in contours:
    area = cv2.contourArea(cnt)
    x, y, w, h = cv2.boundingRect(cnt)
    
    if area > max_area:
        max_area = area
        max_contour = cnt

if max_contour is not None:
    x, y, w, h = cv2.boundingRect(max_contour)
    # cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)
    roi = img2[y:y+h, x:x+w]
    cv2.imwrite('op_ex.jpg', roi)
# cv2.imwrite('samp_balanced_extracted.jpg', img)
