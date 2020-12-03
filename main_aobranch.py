#Based on tutorial https://www.pyimagesearch.com/2015/09/21/opencv-track-object-movement/
# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
from Regionify import Regionify
from play import play
import threading


def detect_objects(img, pts, num_objs = 1, color = 'green'):
    blurred = cv2.GaussianBlur(img, (11, 11), 0)
    #todo change back to HSV??
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2RGB)
    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    if (color == 'green'):
        upper_hsv = greenUpper
        lower_hsv = greenLower
    if (color == 'red'):
        upper_hsv = redUpper
        lower_hsv = redLower
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        for obj in range(num_objs):
            c = max(cnts, key=cv2.contourArea)

            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            # only proceed if the radius meets a minimum size
            if radius > 10:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(img, (int(x), int(y)), int(radius),
                           (0, 255, 255), 2)
                cv2.circle(img, center, 5, (0, 0, 255), -1)
                pts.appendleft(center)

    return pts

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=32,
    help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space
#TODO I am not convinced that these bounds are correct for HSV bc,
#TODO they look much more appropriate for RGB
greenLower = (29, 86, 6)
greenUpper = (90, 255, 255)

redLower = (86, 6, 29)
redUpper = (255, 64, 255)


# initialize the list of tracked points, the frame counter,
# and the coordinate deltas
pts1 = deque(maxlen=args["buffer"])
pts2 = deque(maxlen=args["buffer"])
pts_list = []
pts_list.append(pts1)
pts_list.append(pts2)
counter = 0
(dX, dY) = (0, 0)
direction = ""
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    vs = VideoStream(src=0).start()
# otherwise, grab a reference to the video file
else:
    vs = cv2.VideoCapture(args["video"])
# allow the camera or video file to warm up
time.sleep(2.0)

global playing
playing = False
num_objs = int(input("Enter how many balls you are using: "))
frame = vs.read()
rows, cols, channels = frame.shape
regions, references = Regionify(frame, instrument="xylophone")
# keep looping
while True:
    # grab the current frame
    frame = vs.read()
    # handle the frame from VideoCapture or VideoStream
    frame = frame[1] if args.get("video", False) else frame
    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if frame is None:
        break
    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=600)

    pts_list[0] = detect_objects(frame, pts_list[0], num_objs)
    if (num_objs >1):
        pts_list[1] = detect_objects(frame, pts_list[1], num_objs, 'red')
        #pts for the SECOND ball

    #TODO place the below code into a loop (for p in range(2)) and repeat this for both balls
    # loop over the set of tracked points
    for p in range(num_objs):
        pts = pts_list[p]
        for i in np.arange(1, len(pts)):
            # if either of the tracked points are None, ignore
            # them
            if pts[i - 1] is None or pts[i] is None:
                continue
            # check to see if enough points have been accumulated in
            # the buffer
            if counter >= 10 and i == 1 and len(pts) > 10:
                # compute the difference between the x and y
                # coordinates and re-initialize the direction
                # text variables
                dX = pts[-10][0] - pts[i][0]
                dY = pts[-10][1] - pts[i][1]
                (dirX, dirY) = ("", "")
                #TODO change this?
                direction = "Test"

                velocity = np.array([dX, dY])
                point = pts[i]
                if playing == False:
                    t = threading.Thread(target=play, args=(point, velocity, regions, references, playing))
                    t.start()
                    # play(point, velocity, regions, references, playing)

            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
            cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
        # show the movement deltas and the direction of movement on
        # the frame
        cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    0.65, (0, 0, 255), 3)
        if p == 0:
            cv2.putText(frame, "green - dx: {}, dy: {}".format(dX, dY),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.35, (0, 0, 255), 1)
        else:
            cv2.putText(frame, "red - dx: {}, dy: {}".format(dX, dY),
                        (frame.shape[1] - 150, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.35, (0, 0, 255), 1)

    # show the frame to our screen and increment the frame counter
    #this next line let's you see what a frame in HSV looks like. debugging purposes only:
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    counter += 1
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
    vs.stop()
# otherwise, release the camera
else:
    vs.release()
# close all windows
cv2.destroyAllWindows()