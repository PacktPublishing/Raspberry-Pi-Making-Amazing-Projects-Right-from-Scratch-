#!/bin/bash
sudo echo 27 > /sys/class/gpio/export
sudo echo in > /sys/class/gpio/gpio27/direction
# loop forever
while true
do
	# read the switch state
	SWITCH=$(sudo cat /sys/class/gpio/gpio27/value)

	if [ $SWITCH = "1" ]
	then
		#switch not pushed so wait for a second
		sleep 1
	else
		#switch was pushed
		echo "You've pushed my button"
	fi
done
