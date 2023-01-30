import serial
try:
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
    while 1:
      print(ser.readline()[:-2])
except ValueError:
    print("seriovy port nenalezen, restartuj skript")
    ser.close()
