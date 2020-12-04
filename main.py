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
from play import playSound
import threading
from multiprocessing import Process, Queue



def detect_objects(img, pts):
	blurred = cv2.GaussianBlur(img, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)
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
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
# initialize the list of tracked points, the frame counter,
# and the coordinate deltas
pts = deque(maxlen=args["buffer"])
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
frame = vs.read()
rows, cols, channels = frame.shape
regions, references = Regionify(frame, instrument="xylophone")
# regions = imutils.resize(regions, width = 600)
# regions_3D = regions.reshape(regions.shape[0],regions.shape[1],1)
# regions_3D = np.concatenate((regions_3D,regions_3D,regions_3D),axis = 2)

# task_queues = []
# region_queues = {}
locks = []
for i in range(1, len(np.unique(regions))):
	locks.append(threading.Lock())

def worker(region, *args):
	locks[region-1].acquire()
	playSound(*args)
	locks[region-1].release()

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
	pts = detect_objects(frame, pts)

	# loop over the set of tracked points
	for i in np.arange(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue
		# check to see if enough points have been accumulated in
		# the buffer
		if counter >= 10 and i == 1 and pts[-10] is not None:
			# compute the difference between the x and y
			# coordinates and re-initialize the direction
			# text variables
			dX = pts[-10][0] - pts[i][0]
			dY = pts[-10][1] - pts[i][1]
			(dirX, dirY) = ("", "")
			direction= "Test"

			velocities = [np.array([dX, dY])]
			points = [pts[i]]
			region = regions[points[0]]

			if not locks[region-1].locked():
				t = threading.Thread(target=worker, args=(region, points, velocities, regions, references, playing))
				t.start()
				#play(point, velocity, regions, references, playing)

		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
	# show the movement deltas and the direction of movement on
	# the frame
	cv2.putText(frame, "dx: {}, dy: {}".format(dX, dY),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
		0.35, (0, 0, 255), 1)
	#color the regions so the user knows which areas are the instruments
	#extract only those areas in img that is a instrument region
	# extraction = (regions_3D >= 1)*frame
	# frame = frame - extraction
    # #Alpha add the regions and extraction and reform the image
	# foreground = 0.8 * extraction
	# foreground = foreground.astype(np.uint8)
	# background = 10.0 * regions_3D
	# background = background.astype(np.uint8)
	# combined = cv2.add(foreground, background)
	# frame = frame+combined

	# show the frame to our screen and increment the frame counter
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