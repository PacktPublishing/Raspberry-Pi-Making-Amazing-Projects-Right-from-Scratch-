#!/bin/bash
#/etc/pi-alarm/alarm-control.sh

ALM_BELL_DURATION=600	#duration in seconds the alarm bell should sound for
ALM_EXIT_DELAY=30		#entry/exit zone delay in seconds
ALM_KEY_ARMED=0 		#status of the arm/disarm key switch
ALM_SYS_ARMED=0			#armed status of the system

ALM_ZONE_INPUT_READ=""	#this will store the value of the zone inputs read
ALM_ZONE_INPUT_STAT="00000000"	#binary representation of the inputs (b7-b0)
ALM_ZONE_INPUT_PREV=""	#previous zone input status
ALM_ZONE_TRIGGER=0		#this will be set to 1 if one or more zones is triggered
ALM_ZONES_STAT=(0 0 0 0 0 0 0 0) #dynamic array of normalised zone status (z1 to z8 order) - 1 is triggered

STAT_RET_VAL=""			#return value from functions

#This helper function will update the alarm config
#file with the specified value (alarm.cfg) so that
#the Web panel can know the latest status
function almUpdateConfigSetting()
{
	#$1 - Setting Name
	#$2 - Setting Value
	sudo sed -i "s/^\($1\s*= *\).*/\1$2/" /etc/pi-alarm/alarm.cfg
}

# GPIO SET UP ###################################
#Set up the Raspberry Pi GPIO pins
#Refer to Chapter 2 for info
#D0 (GPIO17) Arm/Disarm Key Input
sudo echo 17 > /sys/class/gpio/export
sudo echo in > /sys/class/gpio/gpio17/direction

#D4 (GPIO23) Armed LED Output
sudo echo 23 > /sys/class/gpio/export
sudo echo out > /sys/class/gpio/gpio23/direction
sudo echo 0 > /sys/class/gpio/gpio23/value

#D5 (GPIO24) Exit Buzzer Output
sudo echo 24 > /sys/class/gpio/export
sudo echo out > /sys/class/gpio/gpio24/direction
sudo echo 0 > /sys/class/gpio/gpio24/value

#D6 (GPIO25) Alarm LED Output
sudo echo 25 > /sys/class/gpio/export
sudo echo out > /sys/class/gpio/gpio25/direction
sudo echo 0 > /sys/class/gpio/gpio25/value

#D7 (GPIO4)  Alarm Bell Output
sudo echo 4 > /sys/class/gpio/export
sudo echo out > /sys/class/gpio/gpio4/direction
sudo echo 0 > /sys/class/gpio/gpio4/value

#This helper function will switch a specified GPIO output on or off
function almSetGPIOValue()
{
	#$1 - GPIO pin number
	#$2 - Value
	sudo echo $2 > /sys/class/gpio/gpio$1/value
}
#Helper functions to switch on and off the outputs
function almSetArmedLED()
{
	#$1 - 0 or 1 (Off or On)
	almSetGPIOValue 23 $1
	echo "[ALM] Armed LED set to $1"
}
function almSetExitBuzzer()
{
	#$1 - 0 or 1 (Off or On)
	almSetGPIOValue 24 $1
	echo "[ALM] Exit Buzzer set to $1"
}
function almSetAlarmLED()
{
	#$1 - 0 or 1 (Off or On)
	almSetGPIOValue 25 $1
	echo "[ALM] Alarm Trigger LED set to $1"
}
function almSetAlarmBell()
{
	#$1 - 0 or 1 (Off or On)
	almSetGPIOValue 4 $1
	echo "[ALM] Alarm Bell set to $1"
}
#this function returns whether the system is armed via
#either the web console or key switch
function almGetArmedSwitchStatus()
{	
	STAT_RET_VAL="0"
	#read arm key switch input from 
	local L_VAL=$(sudo cat /sys/class/gpio/gpio17/value)
	if [ $L_VAL -eq 1 ]; then
		#system has been armed with key switch
		echo "[ALM] System ARMED with key switch"
		ALM_KEY_ARMED=1
		almUpdateConfigSetting "SYSTEM_ARMED" "1" #set system armed console flag
		STAT_RET_VAL="1"
	else
		#read system armed value from web console config file
		if [ $SYSTEM_ARMED == 1 ]; then
			echo "[ALM] System ARMED with web console"
			STAT_RET_VAL="1"
		fi	
	fi	
}
#################################################


# PORT EXPANDER SET UP ##########################
#Refer to Chapter 4 for more information about the I2C bus

#We will set up I/O BUS A as all inputs
sudo i2cset -y 1 0x20 0x00 0xFF

#Whilst we're not using BUS B in our system,
#we can set that up as all inputs too
sudo i2cset -y 1 0x20 0x01 0xFF

#This function will read the port inputs and set the
#status of each zone
function almReadZoneInputs()
{
	#preserve previous zone status
	ALM_ZONE_INPUT_PREV=$ALM_ZONE_INPUT_STAT
	#read the 8-bit hex value of port a
	ALM_ZONE_INPUT_READ=$(sudo i2cget -y 1 0x20 0x12)	
	
	if [[ $ALM_ZONE_INPUT_READ = *"Error"* ]]; then
		#An error occured reading the I2C bus - set default value
		ALM_ZONE_INPUT_READ="0x00"
	fi
	
	#remove the 0x at the start of the value to get the hex value
	local L_HEX=${ALM_ZONE_INPUT_READ:2}
	#convert the hex value to binary
	local L_BIN=$(echo "obase=2; ibase=16; $L_HEX" | bc )
	#zero pad the binary to represent all 8 bits (b7-b0)
	ALM_ZONE_INPUT_STAT=$(printf "%08d" $L_BIN)

	echo "[ALM] Zone I/O Status: $ALM_ZONE_INPUT_STAT ($ALM_ZONE_INPUT_READ)"
	
	#check each zone input to see if it's in a triggered state
	#a triggered state may be either 1 or 0 depending on the input's configuration
	#you'll need to set the logic here accordingly for each input
	#the ALM_ZONES_STAT array contains the definitive trigger value for each input
	
	#zone 1 test (bit 0)
	local L_FLG=${ALM_ZONE_INPUT_STAT:7:1}
	if [ $L_FLG -eq 0 ]; then ALM_ZONES_STAT[0]=0; else ALM_ZONES_STAT[0]=1; fi
	
	#zone 2 test (bit 1)
	local L_FLG=${ALM_ZONE_INPUT_STAT:6:1}
	if [ $L_FLG -eq 0 ]; then ALM_ZONES_STAT[1]=0; else ALM_ZONES_STAT[1]=1; fi

	#zone 3 test (bit 2)
	local L_FLG=${ALM_ZONE_INPUT_STAT:5:1}
	if [ $L_FLG -eq 0 ]; then ALM_ZONES_STAT[2]=0; else ALM_ZONES_STAT[2]=1; fi

	#zone 4 test (bit 3)
	local L_FLG=${ALM_ZONE_INPUT_STAT:4:1}
	if [ $L_FLG -eq 0 ]; then ALM_ZONES_STAT[3]=0; else ALM_ZONES_STAT[3]=1; fi

	#zone 5 test (bit 4)
	local L_FLG=${ALM_ZONE_INPUT_STAT:3:1}
	if [ $L_FLG -eq 0 ]; then ALM_ZONES_STAT[4]=0; else ALM_ZONES_STAT[4]=1; fi
	
	#zone 6 test (bit 5)
	local L_FLG=${ALM_ZONE_INPUT_STAT:2:1}
	if [ $L_FLG -eq 0 ]; then ALM_ZONES_STAT[5]=0; else ALM_ZONES_STAT[5]=1; fi

	#zone 7 test (bit 6)
	local L_FLG=${ALM_ZONE_INPUT_STAT:1:1}
	if [ $L_FLG -eq 0 ]; then ALM_ZONES_STAT[6]=0; else ALM_ZONES_STAT[6]=1; fi

	#zone 8 test (bit 7)
	local L_FLG=${ALM_ZONE_INPUT_STAT:0:1}
	if [ $L_FLG -eq 0 ]; then ALM_ZONES_STAT[7]=0; else ALM_ZONES_STAT[7]=1; fi

	echo "[ALM] Zone Trigger Status: $ALM_ZONES_STAT[*]"
}
#################################################


# MAIN CONTROL ROUTINE ##########################

# initialise system #########
echo "[ALM] Initialising system..."
almUpdateConfigSetting "SYSTEM_ARMED" "0" #clear system armed console flag
sleep 1
sudo cat /etc/pi-alarm/alarm.cfg
sleep 1
echo "[ALM] Initialising done"
#############################

# loop continously###########
while true
do		
	# wait for system to be armed ###############
	echo "[ALM] Alarm now in STAND-BY state - waiting to be armed"
	almSetArmedLED 0 #switch off armed LED
	STAT_RET_VAL="0"
	while [[ $STAT_RET_VAL = "0" ]]; do	
		sleep 1
		#read the control panel status file
		. /etc/pi-alarm/alarm.cfg
		almGetArmedSwitchStatus #result is returned in STAT_RET_VAL
		echo -n "*" # indicate standby mode
	done
	#############################################
	
	
	# perform exit delay ########################
	echo "[ALM] Alarm now in EXIT DELAY state"
	almSetExitBuzzer 1 #switch on exit buzzer
	COUNTER=$ALM_EXIT_DELAY
	while [[ $STAT_RET_VAL = "1" && $COUNTER -gt 0 ]]; do
		sleep 1
		#read the control panel status file
		. /etc/pi-alarm/alarm.cfg
		almGetArmedSwitchStatus #result is returned in STAT_RET_VAL		
		COUNTER-=1
		echo -n "X$COUNTER " # indicate exit mode
	done
	almSetExitBuzzer 0 #switch off exit buzzer
	#############################################	

		
	# system now armed - monitor inputs #########
	ALM_SYS_ARMED=1
	echo "[ALM] Alarm now in ARMED state"	
	almSetArmedLED 1 #switch on armed LED

	#read the control panel status file
	. /etc/pi-alarm/alarm.cfg	
	almReadZoneInputs	# > ALM_ZONES_STAT[x]

	#check each zone input to set if it's enable
	#and has been triggered	
	#NUM_ZONES setting is stored in alarm.cfg
	
	while [[ $ALM_SYS_ARMED -eq 1 ]]; do
		echo -n "A" #indicate armed mode
		
		ALM_ZONE_TRIGGER=0	
		for (( i=$NUM_ZONES; i>0; i-- )); do	
			if [[ $ALM_ZONES_STAT[$i-1] -eq 1 ]]; then
				#zone has been triggered
				echo "[ALM] Zone $i TRIGGERED"			
				E_VAR="ZONE_ENABLE_$i"
				E_VAL=`echo "$E_VAR"` #get zone enabled status loaded from alarm.cfg
				
				if [[ $E_VAL -eq 1 ]]; then
					#zone is enabled
					ALM_ZONE_TRIGGER=1 #set alarm triggered flag
					echo "[ALM] Zone $i ENABLED - alarm will be triggered"			
					almUpdateConfigSetting "ZONE_STATUS_$i" "1" 
					
					## YOU CAN INSERT CODE HERE TO TAKE CAMERA IMAGE IF YOU WANT##
					## REFER BACK TO CHAPTER 6 ##
					
				fi
			fi
		done
		
		. /etc/pi-alarm/alarm.cfg
		almGetArmedSwitchStatus #result is returned in STAT_RET_VAL		
		
		if [[ $ALM_ZONE_TRIGGER -eq 1 ]]; then
			# alarm has been triggered		
			almSetAlarmLED 1
			echo "[ALM] A zone has been triggered"
			
			#####################################
			# ZONE 1 is the ENTRY zone - if that's triggered then delay
			if [[ $ALM_ZONES_STAT[0] -eq 1 ]]; then
				# perform entry delay ###########
				echo "[ALM] Alarm now in ENTRY state"
				setExitBuzzer 1 #switch on entry/exit buzzer
				
				COUNTER=$ALM_EXIT_DELAY	
				STAT_RET_VAL="0"
				while [[ $STAT_RET_VAL = "1" && $COUNTER -gt 0 ]]; do
					echo -n "E$COUNTER " #indicate entry mode
					sleep 1
					#read the control panel status file
					. /etc/pi-alarm/alarm.cfg
					almGetArmedSwitchStatus #result is returned in STAT_RET_VAL		
					COUNTER-=1
				done
			fi
			#####################################
				
				
			#####################################
			# STAY in TRIGGERED mode until system has been disarmed
			if [[ $STAT_RET_VAL = "1" ]]; then
				#alarm has not been disabled
				almSetAlarmBell 1 #switch on alarm bell
				echo "[ALM] Alarm now in TRIGGERED state"

				## YOU CAN INSERT CODE HERE TO SEND YOU AN EMAIL IF YOU WANT##
				## REFER BACK TO CHAPTER 6 ##
				
				COUNTER=0
				STAT_RET_VAL="0"
				while [[ $STAT_RET_VAL = "1" ]]; do
					echo -n "T$COUNTER " #indicate triggered mode
					sleep 1
					#read the control panel status file
					. /etc/pi-alarm/alarm.cfg
					almGetArmedSwitchStatus #result is returned in STAT_RET_VAL		
					
					COUNTER+=1
					if [[ $COUNTER -gt $ALM_BELL_DURATION ]]; then
						almSetAlarmBell 0 #switch off alarm bell						
						echo "[ALM] Bell has been switched OFF"
					fi					
				done
			fi
			#####################################
			
			# alarm has been disarmed ##########
			echo "[ALM] Alarm has been DISARMED"
			ALM_SYS_ARMED=0
			almSetAlarmBell 0 #switch off alarm bell						
			almSetExitBuzzer 0 #switch off exit buzzer
			almSetAlarmLED 0
			almSetArmedLED 0 #switch off armed LED
			
			#####################################
		fi

	done
	#############################################
	
done
#############################################
