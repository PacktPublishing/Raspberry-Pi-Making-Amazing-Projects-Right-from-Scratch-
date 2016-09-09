import picamera
import grovepi
from time import sleep

camera = picamera.PiCamera()
counter = 0
led = 3
buzzer = 5
ultrasonic = 7

while True:
    try:
        if grovepi.ultrasonicRead(ultrasonic) < 100:
	    print 'Intruder Detected'
            grovepi.analogWrite(buzzer,100)
            grovepi.digitalWrite(led_status,1)
            sleep(.5)
            grovepi.analogWrite(buzzer,0)
	    grovepi.digitalWrite(led_status,0)
            camera.capture('image' + counter + '.jpg')
            print 'Image Captured'
	    sleep(2)
    except IOError:
        print "Error"
