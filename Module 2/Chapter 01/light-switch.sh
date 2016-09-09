#!/bin/bash

#set up the LED GPIO pin
sudo echo 17 > /sys/class/gpio/export
sudo echo out > /sys/class/gpio/gpio17/direction

#set up the switch GPIO pin
sudo echo 27 > /sys/class/gpio/export
sudo echo in > /sys/class/gpio/gpio27/direction

# loop forever
while true
do
	# read the switch state
	SWITCH=$(sudo cat /sys/class/gpio/gpio27/value)

	#0=Pushed 1=Not Pushed
	if [ $SWITCH = "1" ]
	then
		#switch not pushed so turn off LED pin
		sudo echo 0 > /sys/class/gpio/gpio17/value
	else
		#switch was pushed so turn on LED pin
		sudo echo 1 > /sys/class/gpio/gpio17/value
	fi
	#short delay
	sleep 0.5
done
