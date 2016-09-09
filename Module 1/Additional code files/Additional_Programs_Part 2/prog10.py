import numpy as np
import cv2

cam = cv2.VideoCapture(0)

# Green and Blue Object Tracker

while ( True ):
	ret, frame = cam.read()

	hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

	blue=cv2.inRange(hsv,np.array([100,50,50]),np.array([140,255,255]))
	green=cv2.inRange(hsv,np.array([40,50,50]),np.array([80,255,255]))	

	image_mask=cv2.add(blue,green)

	output=cv2.bitwise_and(frame,frame,mask=image_mask)

	cv2.imshow('Original',frame)
#	cv2.imshow('Image Mask',image_mask)
	cv2.imshow('Output',output)

	if cv2.waitKey(1) == 27:
		break

cv2.destroyAllWindows()
cam.release()
