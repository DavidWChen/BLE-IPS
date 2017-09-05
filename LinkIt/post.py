import serial
import json
import requests
#change the URL to match your server address
URL = 'http://192.168.1.69:8080/update' 
s = serial.Serial("/dev/ttyS0", 57600)
#Init
rssilist=[[],[],[],[]]
#macs=["D43639DE6243", "508CB169DE3F", "D43639DE6139", "D43639DC36A6"] #HM-10
macs=["FFFFFFFFFFFF", "1918FC042018", "1918FC0420EE", "1918FC042101"] #Seekcy
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

def getRSSI():
	#init
	flag = [0,0,0,0]
	rssis = ["", "", "" , ""]
	while(1):
		#get the bluetooth signal string
		#DISC:8Factory:32UUID:4Maj4Min2MeasuredPow:12Mac:4RSSIOK+
		btstr = getBTString()
		print(btstr)
		#iterate through string, not including BTDiscovery Header and Footer
		for i in range(11, len(btstr)-8):
			#when reaching the discovery entry
			if (btstr[i:i+4] == "DISC"):
				#get the MAC address and RSSI
				mac = btstr[i+58:i+70]
				rssi = btstr[i+71:i+75]
				#store the value if it matches a beacon
				#indicate a value was found with the flag
				if (mac == macs[0]):
					print(macs[0] + rssi)
					rssis[0] = rssi
					flag[0] = 1
				elif (mac == macs[1]):
					print(macs[1] + rssi)
					rssis[1] = rssi
					flag[1] = 1
				elif (mac == macs[2]):
					print(macs[2]+ rssi)
					rssis[2] = rssi
					flag[2] = 1
				elif (mac == macs[3]):
					print(macs[3]+rssi)
					rssis[3] = rssi
					flag[3] = 1
				else:
					pass
		#if all four beacons have been found, return list of rssi
		if ((flag[0] == 1) and (flag[1] == 1) and (flag[2] == 1) and (flag[3] == 1)):
			return rssis

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

while(1):
	rssi = getRSSI()
	#place rssi in dictionary after processing
	f = {'rssi1': processRSSI(rssi[0][:4], rssilist[0]),
		'rssi2': processRSSI(rssi[1][:4], rssilist[1]), 
		'rssi3': processRSSI(rssi[2][:4], rssilist[2]), 
		'rssi4': processRSSI(rssi[3][:4], rssilist[3])}
	#convert to JSON
	j = json.dumps(f, sort_keys = True)
	headers = {'content-type':'application/json'}
	#post to server, keep runnning even in case of failure
	try:
		r = requests.post(URL, data=j , headers=headers)
	except requests.exceptions.RequestException:
		pass