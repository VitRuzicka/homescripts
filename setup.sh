#!/bin/bash
sudo apt update -y
sudo apt upgrade -y
sudo apt install nano -y
wget https://raw.githubusercontent.com/VitRuzicka/homescripts/main/otevirani.py
chmod +x otevirani.py
sudo mv otevirani.py /home/$USER/Desktop/
