#!/bin/bash
#/etc/pi-alarm/update-alarm-setting.sh
############################################
# Provides access to the sed command from  #
# PHP as it needs write access to a temp   #
# folder.                                  #
# $1 - Setting Name                        #
# $2 - Setting Value                       #
############################################
sed -i "s/^\($1\s*= *\).*/\1$2/" /etc/pi-alarm/alarm.cfg
