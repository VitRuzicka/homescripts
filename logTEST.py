#!/usr/bin/env python
import minimalmodbus
import serial.tools.list_ports
from datetime import datetime
import os
now = datetime.now()
instrument = 0
def pripoj():
    global instrument
    instrument = minimalmodbus.Instrument("/dev/ttyACM0", 3) # port name, slave address (in decimal)

if __name__ == '__main__':
    pripoj()
    print(now.strftime("%d/%m/%Y, %H:%M:%S,"), instrument.read_register(31, 0))


