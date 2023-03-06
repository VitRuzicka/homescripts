#!/usr/bin/env python
import minimalmodbus
from datetime import datetime
import os
import threading
from threading import Thread
import time

fullBrightStart = [7, 0, 0]
fullBrightStop = [19, 0, 0]


now = datetime.now()
instrument = 0
def pripoj():
    global instrument
    instrument = minimalmodbus.Instrument("/dev/ttyACM0", 3) # port name, slave address (in decimal)
def zamek(p):
    instrument.write_register(27, p, 0)
def jas(p):
    instrument.write_register(14, p, 0)
def loguj(cas):
    while True:
        file1 = open("log.txt", "a")
        str1 = str(now.strftime("%d/%m/%Y, %H:%M:%S, ")+str(instrument.read_register(22,0))+" "+str(instrument.read_register(31, 0)) + " \n")
        file1.write((str1))
        file1.close()
        #automaticke ztlumeni svetel
        if (int(now.strftime("%H")) == fullBrightStart[0] and int(now.strftime("%M")) >= fullBrightStart[1]) and (int(now.strftime("%H")) == fullBrightStart[0] and int(now.strftime("%M")) < fullBrightStart[0]+5):
            jas(255) #plny jas po cely den
        elif (int(now.strftime("%H")) == fullBrightStop[0] and int(now.strftime("%M")) >= fullBrightStop[1]) and (int(now.strftime("%H")) == fullBrightStop[0] and int(now.strftime("%M")) <= fullBrightStop[1]+5):
            jas(30)  #snizeny jas v noci
        time.sleep(cas*60)
             
if __name__ == '__main__':
    pripoj()
    daemon = Thread(target=loguj, args=(5,), daemon=True, name='Logovani') #bezi kazdych 5min
    daemon.start()
    while True:
        r = input()
        if r == "pomoc":
            zamek(1)
