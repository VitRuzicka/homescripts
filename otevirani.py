#!/usr/bin/env python
import minimalmodbus
from datetime import datetime
from threading import Thread
import time
from paho.mqtt import client as mqtt_client
from serial.tools.list_ports import comports
import serial
#################  MQTT setup   #########################

client_id = 'identificator'  #edit this line {dlouha, rantirovska}
subTopic = "/boxy/" + client_id + "/ovladani/#"
pubTopic = "/boxy/" + client_id + "/stav"

broker = IP_adresa
port = 1883
username = None
password = None
################

SCAN_ANY=0 #opens the regular lock after any code is scanned
TELEMETRY=1
LOGGING=0   #needs to have AUTO_DIM enabled
USE_MQTT=1

regular_code = "open"
cool_code = "opencool"

fullBrightStart = [7, 0, 0]
fullBrightStop = [19, 0, 0]

now = datetime.now()
ioBoard = None
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
    try:
        client.connect(broker, port)
    except OSError:
        print("Internet doesnt work, lets move on")
        return None
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
    global ioBoard
    global ctecka
    print("trying to connect to reader and homeIOboard")
    while(1):
        for port in comports():
            if(port[1] == "Pico - Board CDC" and ioBoard == None):
                print("homeIOboard connected")
                ioBoard = minimalmodbus.Instrument(port[0], 3) # port name, slave address (in decimal)
            if ( "NLS" in port[1] and ctecka == None):
                print("reader connected")
                ctecka  = serial.Serial(port[0], 115200)
        if ioBoard != None and ctecka != None: #both ports were assigned 
            break
     
def zamek(p):
    if p == 0: #open the regular lock
        ioBoard.write_register(27, 1, 0)
    elif p == 1: #open the cool section
        ioBoard.write_register(29, 1, 0)
    
def jas(p):
    ioBoard.write_register(14, p, 0)

def sendTelemetry():
    #read all the info from modbus to array
    data = []
    for registr in range(10,32):
        #print(ioBoard.read_register(registr))
        data.append( ioBoard.read_register(registr))
    print("gathered data " + str(data))
    #now try to send telemetry
    try:
        client.publish(pubTopic, str(data))
    except:
        print("Failed to send telemetry data")

def telemetry(cas):
    while True:
        if LOGGING:
            file1 = open("log.txt", "a")
            str1 = str(now.strftime("%d/%m/%Y, %H:%M:%S, ")+str(ioBoard.read_register(22,0))+" "+str(ioBoard.read_register(31, 0)) + " \n")
            file1.write((str1))
            file1.close()
        #automaticke ztlumeni svetel
        if (int(now.strftime("%H")) == fullBrightStart[0] and int(now.strftime("%M")) >= fullBrightStart[1]) and (int(now.strftime("%H")) == fullBrightStart[0] and int(now.strftime("%M")) < fullBrightStart[0]+5):
            jas(255) #plny jas po cely den
        elif (int(now.strftime("%H")) == fullBrightStop[0] and int(now.strftime("%M")) >= fullBrightStop[1]) and (int(now.strftime("%H")) == fullBrightStop[0] and int(now.strftime("%M")) <= fullBrightStop[1]+5):
            jas(30)  #snizeny jas v noci
        sendTelemetry()  #send the telemetry data to server
        time.sleep(cas)

def checkReader():  #open the lock if the correct code had been scanned
    while(1):
        bytesToRead = ctecka.inWaiting()
        if(bytesToRead != 0):
            ret = str(ctecka.read(bytesToRead))
            if (cool_code in ret):
                print("oteviram chlazenou sekci")
                zamek(1)
            elif(regular_code in ret):
                print("oteviram normalni sekci")
                zamek(0)
            elif SCAN_ANY:
                print("oteviram bezny zamek")
                zamek(0)
        time.sleep(0.1)

if __name__ == '__main__':
    if( username == None or password == None):
        print("Zadejte prvně jméno a heslo k MQTT")
        exit()
    pripoj()

    #check the reader every once in a while
    print("started the reader thread")
    daemon2 = Thread(target=checkReader, args=(), daemon=True, name='Ctecka') #bezi porad
    daemon2.start()

    if TELEMETRY:
        daemon = Thread(target=telemetry, args=(30,), daemon=True, name='Logovani') #bezi kazdych 5min
        daemon.start()

    if(USE_MQTT):
        client = connect_mqtt()
        if client == None:
            #the script could not connect to the internet
            while client == None: #try to connect every 10s
                client = connect_mqtt()
                time.sleep(10)  
            print("Now connected to internet")
        subscribe(client)
        daemon3 = Thread(target=client.loop_forever, args=(), daemon=True, name='MQTT komunikace') #bezi porad
        daemon3.start()

    while True:
        time.sleep(1)
