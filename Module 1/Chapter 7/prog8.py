import picamera
import picamera.array
import time
import cv2

with picamera.PiCamera() as camera:
	rawCap=picamera.array.PiRGBArray(camera)
	camera.start_preview()
	time.sleep(3)
	camera.capture(rawCap,format="bgr")
	image=rawCap.array
cv2.imshow("Test",image)
cv2.waitKey(0)
cv2.destroyAllWindows()