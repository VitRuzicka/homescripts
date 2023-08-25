#!/bin/bash
echo "setting up the board"
setxkbmap -layout cz
echo "setxkbmap -layout cz" |sudo tee -a /home/linaro/.bashrc  #setup czech keyboard
echo "deb http://archive.debian.org/debian/ stretch main contrib non-free \
deb http://archive.debian.org/debian/ stretch-proposed-updates main contrib non-free \
deb http://archive.debian.org/debian-security stretch/updates main contrib non-free" |sudo tee /etc/apt/sources.list #replace the original sources list



sudo apt update -y
sudo apt upgrade -y
sudo apt install nano python3 python3-pip cron gcc -y
pip3 install pyserial
pip3 install minimalmodbus
wget https://raw.githubusercontent.com/VitRuzicka/homescripts/main/otevirani.py
chmod +x otevirani.py
wget https://raw.githubusercontent.com/VitRuzicka/homescripts/main/debug.py
chmod +x debug.py
wget https://raw.githubusercontent.com/VitRuzicka/homescripts/main/start.sh
chmod +x start.sh
wget https://raw.githubusercontent.com/VitRuzicka/homescripts/main/monitor.desktop
chmod +x monitor.desktop
sudo mv monitor.desktop /home/linaro/Desktop/
wget https://raw.githubusercontent.com/VitRuzicka/homescripts/main/ovladani.desktop
chmod +x ovladani.desktop
sudo mv ovladani.desktop /home/linaro/Desktop/

##ted neco pro spravny reset pica:
wget https://raw.githubusercontent.com/jkulesza/usbreset/master/usbreset.c
gcc usbreset.c -o usbreset

#write out current crontab
#sudo crontab -l > mycron
echo "toto prosím zadejte do crontab -e"
#echo new cron into cron file
echo "@reboot export DISPLAY=:0 && sleep 20s && /home/linaro/start.sh" # >> mycron

#install new cron file
#sudo crontab mycron
#rm mycron
