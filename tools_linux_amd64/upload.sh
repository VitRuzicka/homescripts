#!/bin/bash
uzivatel="${USER}"
sudo stty -F /dev/ttyACM0 1200
echo waiting
echo nahravam do /media/$uzivatel/RPI-RP2
while [ ! -d /media/$uzivatel/RPI-RP2 ]; do sleep 0.1; done
sleep 0.5
if [ "$*" = "" ]; then echo rebooting; sudo picotool reboot; exit; fi
echo copying
#cp $1 /media/$uzivatel/RPI-RP2
./rp2040load -D $1 -v
echo done