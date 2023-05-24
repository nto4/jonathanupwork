import cv2
import numpy as np

img = cv2.imread('h.jpeg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret,thresh = cv2.threshold(gray,50,255,0)
contours,hierarchy = cv2.findContours(thresh, 1, 2)
print("Number of contours detected:", len(contours))

big_contour = sorted(contours, key=cv2.contourArea)
print(len(big_contour))
big_contour= big_contour[-2]




contours = []
contours.append(big_contour)
for cnt in contours:
   x1,y1 = cnt[0][0]
   approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
   if len(approx) == 4:
    x, y, w, h = cv2.boundingRect(cnt)
    # cv2.putText(img, 'Rectangle', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    img = cv2.drawContours(img, [cnt], -1, (0,0,0), 15)
    roi = img[y:y+h, x:x+w]
    cv2.imwrite('i.jpg', roi)
    # img = cv2.imread('samp_balanced_extracted.jpg')
    # margin_mm = 2  # Adjust this value according to your needs
    # dpi = 300  # Assuming the image has a resolution of 300 DPI
    # margin_px = int(margin_mm * dpi / 25.4)
    # height, width = img.shape[:2]
    # cropped_image = img[margin_px:height - margin_px, margin_px:width - margin_px]
    # cv2.imwrite('output_image.jpg', cropped_image)
    cv2.imshow("Shapes", roi)
    cv2.waitKey(0)
    cv2.destroyAllWindows()