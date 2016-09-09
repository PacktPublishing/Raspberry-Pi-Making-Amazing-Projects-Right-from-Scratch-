import picamera
import time

with picamera.PiCamera() as cam:
	cam.resolution=(1024,768)
	cam.start_preview()
	time.sleep(5)
	cam.capture('/home/pi/book/output/still.jpg')
