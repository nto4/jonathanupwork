# h
import cv2
import imutils
import numpy as np

image_name = "3.jpeg"


image = cv2.imread(image_name)
# image = imutils.resize(image, height = 800)
blur = cv2.pyrMeanShiftFiltering(image, 11, 21)
gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.015 * peri, True)
    if len(approx) == 4:
        x,y,w,h = cv2.boundingRect(approx)
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,0),25)


cv2.imwrite('h.jpeg', image)


# i
img = cv2.imread('h.jpeg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret,thresh = cv2.threshold(gray,50,255,0)
contours,hierarchy = cv2.findContours(thresh, 1, 2)

big_contour = sorted(contours, key=cv2.contourArea)
big_contour= big_contour[-2]




contours = []
contours.append(big_contour)
for cnt in contours:
   x1,y1 = cnt[0][0]
   approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
   if len(approx) == 4:
    x, y, w, h = cv2.boundingRect(cnt)
    # cv2.putText(img, 'Rectangle', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    img = cv2.drawContours(img, [cnt], -1, (0,0,0), 25)

    roi = img[y:y+h, x:x+w]
    cv2.imwrite('i.jpg', roi)

# cv2.waitKey()


if True:

    from PIL import Image, ImageChops

    im = Image.open('i.jpg')

    def trim(im):
        # bg = Image.new(im.mode, im.size, im.getpixel((10,10)))
        # bg = Image.new(im.mode, im.size, (255, 255, 255))
        bg = Image.new(im.mode, im.size, (0, 0, 0))
        diff = ImageChops.difference(im, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
            return im.crop(bbox)


    trim(im).save("j.jpg")