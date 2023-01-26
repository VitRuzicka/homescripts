import serial
import time
try:
  ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
except FileNotFoundError:
  quit()
while True:
  print(ser.readline())
ser.close()
