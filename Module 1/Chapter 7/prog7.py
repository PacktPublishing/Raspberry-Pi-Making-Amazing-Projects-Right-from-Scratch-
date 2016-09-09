import cv2
cam = cv2.VideoCapture(0)
output  = cv2.VideoWriter('VideoStream.avi',
cv2.cv.CV_FOURCC(*'WMV2'),40.0,(640,480))

while (cam.isOpened()):
	ret, frame = cam.read()
	if ret == True:
		output.write(frame)
		cv2.imshow('VideoStream', frame )
		if cv2.waitKey(1) == 27 :
			break
	else:
		break

cam.release()
output.release()
cv2.destroyAllWindows()
