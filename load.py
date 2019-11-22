import serial
ser = serial.Serial('/dev/ttyUSB0') # open serial port
print(ser.name)
ser.write(b'C')
print(ser.read(1))
ser.write(b'I')
print(ser.read(1))
ser.write(b'S')
print(ser.read(2))
ser.close()

