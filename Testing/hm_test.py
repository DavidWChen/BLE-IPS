from __future__ import print_function
import serial
import sys

points=120
s = serial.Serial("/dev/ttyS0", 57600)
rssilist=[[],[],[],[]]
num_data = [0,0,0,0]
f=open("datafile.txt", "a")

def getBTString():
	btstr = ""
	#until the string contains "DISCE"
	while(btstr.find("DISCE")<=0):
		#read in from serial byte-by-byte
		temp = s.read()
		if (temp != '\n'):
			#append to string
			btstr = btstr + temp
	return btstr

#stabilize RSSI value
def processRSSI(new, lst):
	#add new rssi to list and keep most recent 20 values
	lst.append(int(new))
	if len(lst) > 20:
		lst.pop(0)
	#sort the list and remove bottom and top 10% if applicable
	toavg = sorted(lst)
	if len(toavg) < 3:
		pass
	elif len(toavg) < 15:
		toavg = toavg[1:-1]
	else:
		toavg = toavg[2:-2]
	#retun average of the list
	return str(sum(toavg)/float(len(toavg)))

def getRSSI():
	#init
	global num_data
	flag = [0,0,0,0]
	rssis = ["", "", "" , ""]
	output = ""
	while(1):
		#get the bluetooth signal string
		#DISC:8Factory:32UUID:4Maj4Min2MeasuredPow:12Mac:4RSSIOK+
		btstr = getBTString()
		#iterate through string, not including BTDiscovery Header and Footer
		for i in range(11, len(btstr)-8):
			#when reaching the discovery entry
			if (btstr[i:i+4] == "DISC"):
				#get the MAC address and RSSI
				mac = btstr[i+58:i+70]
				rssi = btstr[i+71:i+75]
				#store the value if it matches a beacon
				if (mac == "D43639DE6243"):
					output = "BEAK1: " + processRSSI(rssi[:4], rssilist[0])
					print(output)
					print(output, file = f)
					num_data[0] = num_data[0] + 1
				elif (mac == "508CB169DE3F"):
					output = "BEAK2: " + processRSSI(rssi[:4], rssilist[1])
					print(output)
					print(output, file = f)
					num_data[1] = num_data[1] + 1
				elif (mac == "D43639DE6139"):
					output = "BEAK3: " + processRSSI(rssi[:4], rssilist[2])
					print(output)
					print(output, file = f)
					num_data[2] = num_data[2] + 1
				elif (mac == "D43639DC36A6"):
					output = "BEAK4: " + processRSSI(rssi[:4], rssilist[3])
					print(output)
					print(output, file = f)
					num_data[3] = num_data[3] + 1
				else:
					output = ""
		if ((num_data[0] >= points) and (num_data[1] >= points) and (num_data[2] >= points) and (num_data[3] >= points)):
			print ("DONE, file contains at least 100 data points for each beacon.")
			return
print(sys.argv[1])
print(sys.argv[1], file=f)
getRSSI()
