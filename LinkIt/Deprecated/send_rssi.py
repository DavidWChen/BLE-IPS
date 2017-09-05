import serial
import time
import mraa
import json
import requests
URL = 'http://192.168.1.108:8080/update'
s = serial.Serial("/dev/ttyS0", 57600)
data = ''
out =[]
while(1):
	if (s.read() == '\n'):
		break;
while (1):
	a = s.read()
	#print (a)
	if (a == ","):
		out.append(data)
		data = ''
	elif(a == '\n'):
		if len(out) != 4:
			data = ''
			out = []
			continue
		f = {'rssi1': out[0][:4],
		'rssi2': out[1][:4], 
		'rssi3': out[2][:4], 
		'rssi4': out[3][:4]}
		j = json.dumps(f, sort_keys = True)
		headers = {'content-type':'application/json'}
		try:
			r = requests.post(URL, data=j , headers=headers)
		except requests.exceptions.RequestException:
			pass
		print(j)
		data = ''
		out = []
	else:
		data = data + a