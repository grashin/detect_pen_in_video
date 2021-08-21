import numpy as np
import time
import cv2
import os
import math
import util

import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--video", type=str, required=True, help="path to input video")
ap.add_argument("-o", "--output", type=str, required=False, help="path to output video")
args = vars(ap.parse_args())

input_video = args["video"]

output_video = args["output"] if args["output"] else 'output/output_video.avi'


args = vars(ap.parse_args())

vs = cv2.VideoCapture(input_video)
writer = None
(H, W) = (None, None)

prop = cv2.CAP_PROP_FRAME_COUNT
total = int(vs.get(prop))

start = time.time()

yellowLower = (-4, 179, 198)
yellowUpper = (16, 225, 295)

while True:
    (grabbed, frame) = vs.read()
    if not grabbed:
        break

    if W is None or H is None:
        (H, W) = frame.shape[:2] 

    frame = cv2.resize(frame, width=600)


    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # gray = cv2.GaussianBlur(gray, (5, 5), 0)
     

    # edged = cv2.Canny(gray, 50, 100)
    # edged = cv2.dilate(edged, None, iterations=1)
    # edged = cv2.erode(edged, None, iterations=1)

    gray = cv2.GaussianBlur(frame, (7, 7), 0)
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2HSV)

    edged = cv2.inRange(gray, yellowLower, yellowUpper)
    edged = cv2.erode(edged, None, iterations=2)
    edged = cv2.dilate(edged, None, iterations=2)

    # if k ==0:
    #     cv2.imshow("Canny", edged)
    #     cv2.waitKey(0)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    output = frame.copy()

    if cnts:
        c = max(cnts, key = cv2.contourArea)

        cv2.imshow('gdfg', edged)
        cv2.waitKey(0)
        M = cv2.moments(c)
        if M["m00"]:
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            cv2.circle(output, center, 5, (0, 0, 255), -1)
            cv2.line(output, (center[0], 0), (center[0], H),(255,0,0), 2)
            cv2.line(output, (0, center[1]), (W, center[1]),(255,0,0), 2)

        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(output,[box],0,(0,0,255),2)

        rows,cols = output.shape[:2]
        [vx,vy,x,y] = cv2.fitLine(c, cv2.DIST_L2,0,0.01,0.01)
        lefty = int((-x*vy/vx) + y)
        righty = int(((cols-x)*vy/vx)+y)
        cv2.line(output,(cols-1,righty),(0,lefty),(0,255,0),2)


        if righty-lefty != 0:
            angle = int(math.atan((cols-1)/(righty-lefty))*180/math.pi)
            if k == 0:
                angle_start = angle
                k+=1
        else: angle = 0
        text_1 = "Angle deviation: {}".format(angle-angle_start)
        # print(angle, angle_start, text_1)
        cv2.putText(output, text_1, (10, 25),  cv2.FONT_HERSHEY_SIMPLEX, 0.7,
        (255, 0, 255), 2)
        text_2 = "Angle: {}".format(angle+90)
        cv2.putText(output, text_2, (10, 50),  cv2.FONT_HERSHEY_SIMPLEX, 0.7,
        (255, 0, 255), 2)
        
        util.draw_angle(output, -angle-90, center)

    if writer is None:
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        writer = cv2.VideoWriter(output_video, fourcc, 15,
            (frame.shape[1], frame.shape[0]), True)

    writer.write(output)

end = time.time()
print(end-start)
writer.release()
vs.release()

