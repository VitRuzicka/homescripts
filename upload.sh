#!/bin/bash
if test -f "usbreset" ; then 
    echo "usbreset downloaded"
else
#kompilace usbreset
    sudo apt update && sudo apt install gcc -y
    wget --no-check-certificate https://raw.githubusercontent.com/jkulesza/usbreset/master/usbreset.c
    gcc usbreset.c -o usbreset
    chmod +x usbreset
fi

wget --no-check-certificate https://github.com/VitRuzicka/homescripts/raw/main/fw/firmware.elf #stazeni firmwaru
wget --no-check-certificate https://github.com/VitRuzicka/homescripts/raw/main/fw/firmware.uf2
uzivatel="${USER}"
sudo stty -F /dev/ttyACM0 1200
echo waiting
echo uploading new firmware to board
while [ ! -d /media/$uzivatel/RPI-RP2 ]; do sleep 0.1; done
sleep 0.5
echo copying
cp firmware.uf2 /media/$uzivatel/RPI-RP2/
#./rp2040load -D firmware.elf -v
echo done
: '
#nyni je potreba pico restartovat aby dobre nacetlo program
#utilitou, kterou jsme drive zkompilovali
echo "resetting pico"
sleep 2
VENDOR="2e8a"
PRODUCT="000a"
lsusb -d $VENDOR:$PRODUCT | while read _ bus _ device _; do
    sudo ./usbreset "/dev/bus/usb/${bus}/${device%:}"
done
'
rm firmware*
