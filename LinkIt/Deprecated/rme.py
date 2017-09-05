import serial
import numpy
import time
import math
from scipy import optimize
import json
import requests
import sys

#CONSTANTS
CHIP_ID = 1 #unique to chip
PERIOD = 10 #seconds between each instance
URL = 'http://192.168.1.108:8080/update'
CENTER_DIST = 7.476063 #can change to be a fucntion of location
CENTER_POINT = numpy.array([4.7,5.655,1.35]) #see above
#id = [beacon1, beacon2, beacon3, beacon4]
locations = [numpy.array([0,0,0]), numpy.array([0,11.31,2.7]), numpy.array([9.4,11.31,0]), numpy.array([9.4,0,2.7])]

#INITIALIZE
prev_time=0
#s = None
#s = serial.Serial("/dev/tty/S0", 57600)

#need to actually implement with bluetooth
def findRSSI():
	rssi = [-78, -79.2, -79.7,-79.1] # function to store rssi in a list like this(inorder)
	rssi = [0,-92,-87,-92]
	rssi = [0,-95,-83,-87]
	return rssi

def rssiToMeter(rssi, txPower =-90):
	if (rssi == 0):
		return CENTER_DIST
	ratio = rssi*1.0/txPower
	if(ratio <1.0):
		return (261.23*ratio-176.14)/100
	else:
		meters = ((382.81)*pow(ratio, 14.693))/100
		return meters

def initialLocation():
	data = zip(locations, distances)
	min_distance = CENTER_DIST #float('inf') : distance from beacon to center
	closest_location = CENTER_POINT #None: center point of room
	for member in data:
		if member[1] < min_distance:
			min_distance = member[1]
			closest_location = member[0]
	return closest_location

def mse(x, locations, distances):
	mse = 0.0
	for location, distance in zip(locations, distances):
		distance_calculated = numpy.linalg.norm(x-location)
		mse += math.pow(distance_calculated - distance, 2.0)
	return mse / len(locations)

while 1:
	if (time.time()> prev_time()+PERIOD)
		continue
	prev_time = time.time()
	rssi = findRSSI()
	distances = [rssiToMeter(rssi[0]), rssiToMeter(rssi[1]),rssiToMeter(rssi[2]), rssiToMeter(rssi[3])]
	#distances = [10, 9, 4, 2]
	result = optimize.minimize(
		mse,                         # The error function
		initialLocation(),            # The initial guess
		args=(locations, distances), # Additional parameters for mse
		method='L-BFGS-B',           # The optimisation algorithm
		options={'ftol':1e-5, 'maxiter': 1e+7 })      # Tolerance, # Maximum iterations
	location = result.x

	#create a dictionary entry w/time stamp & convert to json
	data = {'chip'+str(CHIP_ID):{
		'raw_time': time.time(),
		'x-coordinate': float(location[0]), 
		'y-coordinate': float(location[1]), 
		'z-coordinate': float(location[2])}}
	j = json.dumps(data, sort_keys = True)
	headers = {'content-type':'application/json'}
	r = requests.post(URL, data=j , headers=headers)
	print(j)