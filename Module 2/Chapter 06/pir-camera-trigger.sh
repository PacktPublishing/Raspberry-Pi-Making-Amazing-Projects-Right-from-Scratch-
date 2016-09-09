#!/bin/bash

#set up the High Load GPIO pin
sudo echo 17 > /sys/class/gpio/export
sudo echo out > /sys/class/gpio/gpio17/direction

#set up port expander Port A for inputs
sudo i2cset –y 1 0x20 0x00 0xFF

#clear the output by default to switch light off
sudo echo 0 > /sys/class/gpio/gpio17/value


# loop forever
while true
do
	# read the sensor state
	SWITCH=$(sudo i2cget –y 1 0x20 0x12)

	#PIR is normally closed so pin is held high
	if [ $SWITCH != "0x01" ]
	then
		#PIR was triggered – pin taken low

		#switch on lamp driver
		sudo echo 1 > /sys/class/gpio/gpio17/value
		sleep 0.5
		
		#take a still image
		sudo raspistill –o –image.jpg –h 768 –w 1024 –q 25
		
		#email the image
		mpack –s “Security Alert Photo” test.jpg me@mydomain.com

		#switch off the lamp driver
		sudo echo 0 > /sys/class/gpio/gpio17/value

	fi
	#short delay
	sleep 0.5
done
