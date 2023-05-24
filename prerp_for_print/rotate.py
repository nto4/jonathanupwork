import cv2
import numpy as np
import math

# unrotation to portrait mode

# read input
img = cv2.imread('j.jpg')
hh, ww = img.shape[:2]

# compute center
cx = ww // 2
cy = hh // 2

# rotated input in range -90 to 90 inclusive
# assume scanned so always in that range
# do unrotation by using the longest edge of rectangle to find the direction 
# and unrotate so that it aligns with the vertical (Y) axis upwards
for rotation in range(-90,100,10):

    # rotate image
    matrix = cv2.getRotationMatrix2D((cx,cy), rotation, 1.0)
    img_rotated = cv2.warpAffine(img, matrix, (ww, hh), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    # convert to gray
    gray = cv2.cvtColor(img_rotated, cv2.COLOR_BGR2GRAY)

    # threshold (must be convex, so use morphology to close up if needed)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]

    # find all non-zero pixel coordinates
    # swap x and y for conversion from numpy y,x to opencv x,y ordering via transpose
    coords = np.column_stack(np.where(thresh.transpose() > 0))

    # get minAreaRect and its vertices
    rotrect = cv2.minAreaRect(coords)
    pts = cv2.boxPoints(rotrect)
    #print(pts)
    
    list = []
    # compute edge lengths and directions (in range -90 to 90) and put into list
    polygon = img_rotated.copy()
    for i in range(0,4):
        i1 = i
        i2 = i+1 if i!=3 else 0
        pt1 = pts[i1]
        pt2 = pts[i2]
        pt1x = pt1[0]
        pt2x = pt2[0]
        pt1y = pt1[1]
        pt2y = pt2[1]
        length = math.sqrt( (pt2x-pt1x)*(pt2x-pt1x) + (pt2y-pt1y)*(pt2y-pt1y) )
        direction = (180/math.pi)*math.atan2( (pt2y-pt1y), (pt2x-pt1x) )
        list.append([length, direction, pt1])
        
        # optional: draw lines around box points on input (rotated)
        # points start at left most point (and top most to break ties)
        # and go clockwise around rectangle
        # first point is blue and second point is green to show direction
        x1 = int(pt1x)
        y1 = int(pt1y)
        x2 = int(pt2x)
        y2 = int(pt2y)
        if i == 0:
            cv2.circle(polygon,(x1,y1),7,(255,0,0),-1)
            cv2.circle(polygon,(x2,y2),5,(0,255,0),-1)
            cv2.line(polygon, (x1,y1), (x2,y2), (0,0,255), 2)
        else:
            cv2.line(polygon, (x1,y1), (x2,y2), (0,0,255), 2)
                
    # sort list on length with largest first
    def takeFirst(elem):
        return elem[0]
    list.sort(key=takeFirst, reverse=True)
    
    # get direction of largest length and correct to -90 to 90 range
    item = list[0]
    dir = item[1]
    if dir < -90:
        dir = dir + 180
    if dir > 90:
        dir = dir - 180
                
    # correct to portrait mode
    # if dir is negative or zero, then add 90; otherwise subtract 90
    # dir = 0 occurs for both 0 and 90, so both cannot be determined -- pick one
    if dir <= 0:
        unrotate = dir + 90
    else:
        unrotate = dir - 90
        
    print("initial rotation=", rotation, "edge direction=", dir, "unrotation angle=", unrotate)
    
    # unrotate image
    M = cv2.getRotationMatrix2D((cx, cy), unrotate, 1.0)
    img_unrotated = cv2.warpAffine(img_rotated, M, (ww, hh), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    #cv2.imshow('img_rotated', img_rotated)
    cv2.imshow('polygon', polygon)
    cv2.imshow('img_unrotated', img_unrotated)
    cv2.waitKey()

    # optional save output
    #cv2.imwrite("vertical_rect_{0}.png".format(rotation), img_unrotated)

# Results:

# initial rotation= -90 edge direction= 0.0 unrotation angle= 90.0
# initial rotation= -80 edge direction= -10.024489033132815 unrotation angle= 79.97551096686719
# initial rotation= -70 edge direction= -19.922231300954746 unrotation angle= 70.07776869904525
# initial rotation= -60 edge direction= -30.000354626107335 unrotation angle= 59.99964537389266
# initial rotation= -50 edge direction= -39.98688344835102 unrotation angle= 50.01311655164898
# initial rotation= -40 edge direction= -50.00064126059898 unrotation angle= 39.99935873940102
# initial rotation= -30 edge direction= -60.00891266459192 unrotation angle= 29.991087335408082
# initial rotation= -20 edge direction= -70.07776869904525 unrotation angle= 19.92223130095475
# initial rotation= -10 edge direction= -79.97551600323786 unrotation angle= 10.024483996762143
# initial rotation= 0 edge direction= 90.0 unrotation angle= 0.0
# initial rotation= 10 edge direction= 79.97550927006476 unrotation angle= -10.024490729935238
# initial rotation= 20 edge direction= 70.07776869904525 unrotation angle= -19.92223130095475
# initial rotation= 30 edge direction= 59.99507091100694 unrotation angle= -30.00492908899306
# initial rotation= 40 edge direction= 50.013119348261796 unrotation angle= -39.986880651738204
# initial rotation= 50 edge direction= 39.99936207636015 unrotation angle= -50.00063792363985
# initial rotation= 60 edge direction= 29.991085160541278 unrotation angle= -60.008914839458726
# initial rotation= 70 edge direction= 19.922231300954746 unrotation angle= -70.07776869904525
# initial rotation= 80 edge direction= 10.02448431018454 unrotation angle= -79.97551568981547
# initial rotation= 90 edge direction= 0.0 unrotation angle= 90.0