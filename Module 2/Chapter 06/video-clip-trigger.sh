#!/bin/bash

#set up port expander 
sudo i2cset –y 1 0x20 0x00 0xFF

# loop forever
while true
do
	# read the GPA inputs
	GPA=$(sudo i2cget –y 1 0x20 0x12)

	# detect the zone on input 0
	if [ $GPA == "0x01" ]
	then
		#circuit normally closed so zone is OK
		#short delay
		sleep 0.5
	else
		#zone is activated so take a 20 sec video clip
		
		#filename will be based on current timestamp
		sDate=’date +%d%m%y’
		sTime=’date +%T’
		echo “Zone 1 Activate at $sDate $sTime”

		#take video clip
		raspivid –o $sDate$sTime.h264 –t 20000
		
		#convert to MP4
		MP4Box -fps 30 -add $sDate$sTime.h264 $sDate$sTime.mp4
	fi
done
