import serial
import time
import json
import requests
URL = 'http://192.168.1.69:8080/update'
s = serial.Serial("/dev/ttyS0", 57600)

dummy =[{'rssi1': -81, 'rssi2': -91, 'rssi3': -94, 'rssi4': -89},
		{'rssi1': -80, 'rssi2': -90, 'rssi3': -93, 'rssi4': -88},
		{'rssi1': -92, 'rssi2': -77, 'rssi3': -90, 'rssi4': -95},
		{'rssi1': -94, 'rssi2': -91, 'rssi3': -78, 'rssi4': -91},
		{'rssi1': -91, 'rssi2': -95, 'rssi3': -92, 'rssi4': -71},
		{'rssi1': -94, 'rssi2': -88, 'rssi3': -80, 'rssi4': -93},
		{'rssi1': -79, 'rssi2': -92, 'rssi3': -96, 'rssi4': -89},
		{'rssi1': -94, 'rssi2': -91, 'rssi3': -78, 'rssi4': -91}]

def sendData(data):
	j = json.dumps(data, sort_keys = True)
	headers = {'content-type':'application/json'}
	try:
		r = requests.post(URL, data=j , headers=headers)
	except requests.exceptions.RequestException:
		pass
	print(j)

while (1):
	for i in range(len(dummy)):
		sendData(dummy[i])