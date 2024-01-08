#!/usr/bin/env python
import minimalmodbus
from datetime import datetime
from threading import Thread
import time
from paho.mqtt import client as mqtt_client
from serial.tools.list_ports import comports
import serial

#################  MQTT setup   #########################

client_id = 'rantirovska'  #edit this line {dlouha, rantirovska}
subTopic = "/boxy/" + client_id + "/ovladani/#"


broker = '20.61.188.187'
port = 1883
username = None
password = None

##################

SCAN_ANY=1 #opens the regular lock after any code is scanned
AUTO_DIM=1
LOGGING=0   #needs to have AUTO_DIM enabled
USE_MQTT=1

regular_code = "openregular"
cool_code = "opencool"

fullBrightStart = [7, 0, 0]
fullBrightStop = [19, 0, 0]

now = datetime.now()
instrument = None
ctecka = None


###MQTT###

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        #print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        if "ovladani/cool" in msg.topic:
            if("1" in msg.payload.decode()):
                print("Oteviram chlazenou schranku z MQTT")
                zamek(1)
        elif "ovladani/basic" in msg.topic:
            if("1" in msg.payload.decode()):
                print("Oteviram normalni schranku z MQTT")
                zamek(0)

    client.subscribe(subTopic)
    client.on_message = on_message
####
    
def pripoj():  #function loops until it connects to homeboard and reader
    global instrument
    global ctecka
    print("trying to connect to reader and homeIOboard")
    while(1):
        for port in comports():
            if(port[1] == "Pico - Board CDC"):
                print("homeIOboard connected")
                instrument = minimalmodbus.Instrument(port[0], 3) # port name, slave address (in decimal)
            if ( "NLS-FM430-U" in port[1]):
                print("reader connected")
                ctecka  = serial.Serial(port[0], 115200)
        if instrument != None and ctecka != None: #both ports were assigned 
            break
     
def zamek(p):
    if p == 0: #open the regular lock
        instrument.write_register(27, 1, 0)
    elif p == 1: #open the cool section
        instrument.write_register(29, 1, 0)
    
def jas(p):
    instrument.write_register(14, p, 0)

def loguj(cas):
    while True:
        if LOGGING:
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

def checkReader():  #open the lock if the correct code had been scanned
    bytesToRead = ctecka.inWaiting()
    if(bytesToRead != 0):
        ret = str(ctecka.read(bytesToRead))
        if (regular_code in ret):
            zamek(0)
        elif(cool_code in ret):
            zamek(1)
        elif SCAN_ANY:
            zamek(0)

if __name__ == '__main__':
    if( username == None or password == None):
        print("Zadejte prvně jméno a heslo k MQTT")
        exit()
    pripoj()
    if AUTO_DIM:
        daemon = Thread(target=loguj, args=(5,), daemon=True, name='Logovani') #bezi kazdych 5min
        daemon.start()
    if(USE_MQTT):
        client = connect_mqtt()
        subscribe(client)
        daemon2 = Thread(target=client.loop_forever, args=(), daemon=True, name='MQTT komunikace') #bezi porad
        daemon2.start()

    while True:
        checkReader() #opens the lock if the command comes
        time.sleep(0.1)
