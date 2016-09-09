#!/bin/bash
#/etc/pi-alarm/setup-ramfs.sh

RAM_DISK="/ramfs"
RAM_DISK_SIZE=64M

# Create RAM Disk ##########################
if [ ! -z "$RAM_DISK" ]; then
  echo "[INIT] Creating RAM Disk... $RAM_DISK"
  mkdir -p $RAM_DISK
  chmod 777 $RAM_DISK
  mount -t tmpfs -o size=$RAM_DISK_SIZE tmpts $RAM_DISK/
  echo "[INIT] RAM Disk created at $RAM_DISK"	
fi
############################################
