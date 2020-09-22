# import the necessary packages
from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils
import math
 


def draw_angle(image, angle, center):
    height, width = image.shape[0:2]
    # Ellipse parameters
    radius = 50
    axes = (radius, radius)
    angle_1 = 0
    startAngle = angle
    endAngle = 0
    thickness = 2
    cv2.ellipse(image, center, axes, angle_1, startAngle, endAngle, (255, 0, 255), thickness)

filename = '/Users/grashin/video_detection/siemens/example_8.png'

frame = cv2.imread(filename)
(H, W) = frame.shape[:2]

frame = imutils.resize(frame, width = 600)

gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 0)
 
 
edged = cv2.Canny(gray, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)

cv2.imshow("Canny", edged)
cv2.waitKey(0)

# middle black
# blackLower = (103, 245, -28)
# blackUpper = (123, 265, 52)

# blackLower = (8, 154, -12)
# blackUpper = (28, 174, 68)

# # ideal black   [102 245 -29] [122 265  51]


# gray = cv2.GaussianBlur(frame, (7, 7), 0)
# gray = cv2.cvtColor(gray, cv2.COLOR_BGR2HSV)

# edged = cv2.inRange(gray, blackLower, blackUpper)
# edged = cv2.erode(edged, None, iterations=2)
# edged = cv2.dilate(edged, None, iterations=2)


cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

output = frame.copy()


# if cnts:
#     c = max(cnts, key = cv2.contourArea)


# M = cv2.moments(c)
# if M["m00"]:
#     center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
#     cv2.circle(output, center, 5, (0, 0, 255), -1)
#     cv2.line(output, (center[0], 0), (center[0], H),(255,0,0), 2)
#     cv2.line(output, (0, center[1]), (W, center[1]),(255,0,0), 2)
for c in cnts:
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(output,[box],0,(0,0,255),2)

# rows,cols = output.shape[:2]
# [vx,vy,x,y] = cv2.fitLine(c, cv2.DIST_L2,0,0.01,0.01)
# lefty = int((-x*vy/vx) + y)
# righty = int(((cols-x)*vy/vx)+y)
# cv2.line(output,(cols-1,righty),(0,lefty),(0,255,0),2)


# k = 0


# if righty-lefty != 0:
#     angle = int(math.atan((cols-1)/(righty-lefty))*180/math.pi)
#     if k == 0:
#         angle_start = angle
#         k+=1
# text_1 = "Angle deviation: {}".format(angle-angle_start)
# # print(angle, angle_start, text_1)
# cv2.putText(output, text_1, (10, 25),  cv2.FONT_HERSHEY_SIMPLEX, 0.7,
# (240, 0, 159), 2)
# text_2 = "Angle: {}".format(angle+90)
# cv2.putText(output, text_2, (10, 50),  cv2.FONT_HERSHEY_SIMPLEX, 0.7,
# (240, 0, 159), 2)

# draw_angle(output, -angle-90, center)
 
cv2.imshow("Image", output)
cv2.waitKey(0)
