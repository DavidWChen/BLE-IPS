import time
import json
import requests
URL = 'http://192.168.1.77:8080/update'

# dummy =[{'rssi1': -81, 'rssi2': -91, 'rssi3': -94, 'rssi4': -89},
# 		{'rssi1': -80, 'rssi2': -90, 'rssi3': -93, 'rssi4': -88},
# 		{'rssi1': -92, 'rssi2': -77, 'rssi3': -90, 'rssi4': -95},
# 		{'rssi1': -94, 'rssi2': -91, 'rssi3': -78, 'rssi4': -91},
# 		{'rssi1': -91, 'rssi2': -95, 'rssi3': -92, 'rssi4': -71},
# 		{'rssi1': -94, 'rssi2': -88, 'rssi3': -80, 'rssi4': -93},
# 		{'rssi1': -79, 'rssi2': -92, 'rssi3': -96, 'rssi4': -89},
# 		{'rssi1': -94, 'rssi2': -91, 'rssi3': -78, 'rssi4': -91}]
dummy ={'chip2':{
		'raw_time': time.time(),
		'x-coordinate': str(2),
		'y-coordinate': str(2),
		'z-coordinate': str(2)}}

def sendData(data):
	j = json.dumps(data, sort_keys = True)
	headers = {'content-type':'application/json'}
	try:
		r = requests.post(URL, data=j , headers=headers)
	except requests.exceptions.RequestException:
		pass
	print(j)
sendData(dummy)
# while (1):
# 	sendData(dummy)
	# for i in range(len(dummy)):
	# 	sendData(dummy[i])