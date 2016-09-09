import picamera
import time

with picamera.PiCamera() as cam:
	cam.resolution=(640,480)
	cam.start_preview()
	time.sleep(3)
	for count, imagefile in enumerate(cam.capture_continuous('/home/pi/book/output/image{counter:02d}.jpg')):
		print 'Capturing and saving ' + imagefile
		time.sleep(1)
		if count == 10:
			break
