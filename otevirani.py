import serial
with serial.Serial('/dev/ttyS1', 115200, timeout=1) as ser:
  
