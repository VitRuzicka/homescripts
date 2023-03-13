#!/usr/bin/env python
import minimalmodbus
import serial.tools.list_ports
import time
import os
instrument = 0

def najdiPorty():
    ports = serial.tools.list_ports.comports()
    if ports == []:
        print("Nenalezen volný port")
        print("Končím")
        quit()
    i = 0
    for port, desc, hwid in sorted(ports):
        i+=1
        print("[{}] {}: {}".format(i, port, desc))
        
    volba = input("Zadejte cislo portu: ")
    serport = str(sorted(ports)[int(volba)-1])
    serport = serport[:12:]
    print("vybran ", serport)
    return serport

def pripoj(zvolenyPort):
    global instrument
    instrument = minimalmodbus.Instrument(zvolenyPort, 3) # port name, slave address (in decimal)
    print("pripojuji k %s"%(zvolenyPort))
def vytiskniHodnoty(hodn):
    os.system("clear")         
    print("------------------------------")
    print("reg|    name          |value  |")
    for i, p in enumerate(sluzby):
        if i+10 == 22:
            print ("|%2d| %16s | %3.2f |"%(i+10,p, (float(hodn[i])-10000.0)/100.0))
        else:
            print ("|%2d| %16s | %3d   |"%(i+10,p, hodn[i]))
    print("------------------------------")
    
def ziskejHodnoty():
    hodn = []
    for i in range(len(sluzby)):
        hodn.append(instrument.read_register(i+10, 0))
    vytiskniHodnoty(hodn)

def zmen(reg, hod):
    instrument.write_register(int(reg), int(hod), 0) # Registernumber, value, number of decimals for storage

sluzby = [
        "RED led",
        "GREEN led",
        "BLUE led",
        "Prolinani barev",
        "Brightness",
        "WHITE led",
        "UVC led",
        "IR brana dopis",
        "IR brana balik",
        "COOL tl.",
        "NOUZE tl.",
        "fotoodpor",
        "Temp. fridge",
        "OUT1",
        "OUT2",
        "IN2",
        "IN3",
        "ZAMEK",
        "ZAMEK sense",
        "COOL ZAMEK",
        "COOL ZAMEK sense",
        "Test in"
]

if __name__ == '__main__':
    port = najdiPorty()
    pripoj(port)
    while True:
        ziskejHodnoty()
        t = input("[ENTER] pro refresh, [NUM] pro změnu registru: ")
        if t != '' and 0 < int(t) and int(t) < 50:
            zmen(t, int(input("Zadejte hodnotu registru: ")))
        else:
            time.sleep(1)


