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
wget https://raw.githubusercontent.com/VitRuzicka/homescripts/main/ovladani.desktop
chmod +x ovladani.desktop
sudo mv ovladani.desktop /home/linaro/Desktop/
#write out current crontab
#sudo crontab -l > mycron
echo "toto prosím zadejte do crontab -e"
#echo new cron into cron file
echo "@reboot export DISPLAY=:0 && sleep 30s && /home/linaro/start.sh" # >> mycron
echo "00 07 * * * echo j |sudo tee /dev/ttyACM0" # >> mycron
echo "00 19 * * * echo k |sudo tee /dev/ttyACM0" # >> mycron

#install new cron file
#sudo crontab mycron
rm mycron
