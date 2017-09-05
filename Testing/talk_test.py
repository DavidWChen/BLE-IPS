import serial
s = serial.Serial("/dev/ttyS0", 57600)

while 1:
	print(s.read())
	