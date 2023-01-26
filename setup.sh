#!/bin/bash
sudo apt update -y
sudo apt upgrade -y
sudo apt install nano python3 python3-pip cron -y
pip3 install pyserial
wget https://raw.githubusercontent.com/VitRuzicka/homescripts/main/otevirani.py
chmod +x otevirani.py
wget https://raw.githubusercontent.com/VitRuzicka/homescripts/main/debug.py
chmod +x debug.py
wget https://raw.githubusercontent.com/VitRuzicka/homescripts/main/start.sh
chmod +x start.sh
wget https://raw.githubusercontent.com/VitRuzicka/homescripts/main/monitor.desktop
chmod +x monitor.desktop
sudo mv monitor.desktop /home/linaro/Desktop/
wget https://raw.githubusercontent.com/VitRuzicka/homescripts/main/otevirani.desktop
chmod +x otevirani.desktop
sudo mv otevirani.desktop /home/linaro/Desktop/
#write out current crontab
crontab -l > mycron
#echo new cron into cron file
echo "@reboot sh /home/linaro/start.sh &" >> mycron
#install new cron file
crontab mycron
rm mycron
