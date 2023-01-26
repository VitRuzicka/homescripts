#!/bin/bash
sudo apt update -y
sudo apt upgrade -y
sudo apt install nano python3 python3-pip -y
pip3 install pyserial
wget https://raw.githubusercontent.com/VitRuzicka/homescripts/main/otevirani.py
chmod +x otevirani.py
sudo mv otevirani.py /home/$USER/Desktop/
