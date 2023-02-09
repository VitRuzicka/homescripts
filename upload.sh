#!/bin/bash
if test -f "rp2040load" ; then 
    echo "rp2040load stažen"
else
    wget https://github.com/VitRuzicka/homescripts/raw/main/rp2040load
    chmod +x rp2040load
fi
if test -f "picotool" ; then 
    echo "picotool stažen"
else
    wget https://github.com/VitRuzicka/homescripts/raw/main/picotool
    chmod +x picotool
fi
wget https://github.com/VitRuzicka/homescripts/raw/main/fw/firmware.elf #stazeni firmwaru
wget https://github.com/VitRuzicka/homescripts/raw/main/fw/firmware.uf2
uzivatel="${USER}"
sudo stty -F /dev/ttyACM0 1200
echo waiting
echo nahravam program do rpi pico
while [ ! -d /media/$uzivatel/RPI-RP2 ]; do sleep 0.1; done
sleep 0.5
#if [ "$*" = "" ]; then echo rebooting; sudo ./picotool reboot; exit; fi
echo copying
cp firmware.uf2 /media/$uzivatel/RPI-RP2/
#./rp2040load -D firmware.elf -v
echo done
rm firmware*
