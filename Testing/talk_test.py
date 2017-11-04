#Print what is read from the serial connection
#inside the LinkIt
import serial
s = serial.Serial("/dev/ttyS0", 57600)

while 1:
	print(s.read())
	