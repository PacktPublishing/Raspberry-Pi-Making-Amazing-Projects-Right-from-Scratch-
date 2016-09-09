import numpy as np
import cv2

# Tracking blue objects

cam = cv2.VideoCapture(0)

while ( True ):
	ret, frame = cam.read()

	hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

	range_upper = np.array([140,255,255])
	range_lower = np.array([100,50,50])

	image_mask=cv2.inRange(hsv,range_lower,range_upper)

	output=cv2.bitwise_and(frame,frame,mask=image_mask)

	cv2.imshow('Original',frame)
#	cv2.imshow('Image Mask',image_mask)
	cv2.imshow('Output',output)

	if cv2.waitKey(1) == 27:
		break

cv2.destroyAllWindows()
cam.release()
