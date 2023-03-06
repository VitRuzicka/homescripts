#!/usr/bin/env python
import minimalmodbus
from datetime import datetime
import os
import threading
from threading import Thread
import time

now = datetime.now()
instrument = 0
def pripoj():
    global instrument
    instrument = minimalmodbus.Instrument("/dev/ttyACM0", 3) # port name, slave address (in decimal)
def posli(p):
    instrument.write_register(27, p, 0)
def loguj(cas):
    while True:
        file1 = open("log.txt", "a")
        str1 = str(now.strftime("%d/%m/%Y, %H:%M:%S, ")+str(instrument.read_register(22,0))+" "+str(instrument.read_register(31, 0)) + " \n")
        file1.write((str1))
        file1.close()
        time.sleep(cas*60)
if __name__ == '__main__':
    pripoj()
    daemon = Thread(target=loguj, args=(5,), daemon=True, name='Logovani')
    daemon.start()
    while True:
        r = input()
        if r == "pomoc":
            posli(1)
