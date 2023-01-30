#!/usr/bin/python3
import serial
import time
from serial import SerialException
key = "pomoc"
while 1:
        if(input() == key):
                try:
                        with serial.Serial("/dev/ttyACM0", 115200, timeout=1) as:
                                ser.write(b'o')
                                time.sleep(1)
                                ser.write(b'z')
                                ser.close()
                except SerialException:
                        print("home deska nenei pripojena")
