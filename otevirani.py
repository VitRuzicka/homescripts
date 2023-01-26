import serial
import time
try:
  ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
except FileNotFoundError:
  quit()
while True:
  if input() == 'pomoc':
    ser.write(b'o')
    time.sleep(1)
    ser.write(b'z')
ser.close()
  
