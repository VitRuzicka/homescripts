import serial
try:
  ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
except FileNotFoundError:
  quit()
while True:
  if input() == 'pomoc':
    ser.write('o')
    ser.write('z')
ser.close()
  
