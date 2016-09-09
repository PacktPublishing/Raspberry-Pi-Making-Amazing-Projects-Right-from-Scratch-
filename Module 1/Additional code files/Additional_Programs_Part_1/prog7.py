# Program for highlighting the green objects in the view with green border
# requires webcam to be attached to the Pi

import numpy as np
import cv2

cam = cv2.VideoCapture(0)

while ( True ):
	ret, frame = cam.read()

	hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

	range_upper = np.array([140,255,255])
	range_lower = np.array([100,50,50])

	image_mask=cv2.inRange(hsv,range_lower,range_upper)

	output=cv2.bitwise_and(frame,frame,mask=image_mask)

	contours, hierarchy = cv2.findContours(image_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours( frame, contours, -1, (0,255,0), 2 )

	cv2.imshow('Original',frame)
#	cv2.imshow('Image Mask',image_mask)
#	cv2.imshow('Output',output)

	if cv2.waitKey(1) == 27:
		break

cv2.destroyAllWindows()
cam.release()
