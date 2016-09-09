#!/bin/bash
sudo i2cset –y 1 0x20 0x00 0xFF

# loop forever
while true
do
	# read the sensor state
	SWITCH=$(sudo i2cget –y 1 0x20 0x12)

	if [ $SWITCH == "0x01" ]
	then
		#contact closed so wait for a second
		echo "The door is closed!"
		sleep 1
	else
		#contact was opened
		echo "The door is open!"
	fi
done
