import serial
ser = serial.Serial('/dev/ttyUSB0') # open serial port
print(ser.name)
ser.write(b'A')
print(ser.read(1))
ser.close()

