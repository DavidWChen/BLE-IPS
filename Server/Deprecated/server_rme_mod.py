import numpy
import time
import math
from scipy import optimize
import json
import sys
from PIL import Image, ImageDraw

#CONSTANTS
RAD = 5
CHIP_ID = 1 #unique to chip
URL = 'http://192.168.1.108:8080/update'
CENTER_DIST = 7.476063 #can change to be a fucntion of location
CENTER_POINT = numpy.array([4.7,5.655,1.35]) #see above
locations = [numpy.array([0,0,0]), numpy.array([0,11.31,2.7]), numpy.array([9.4,11.31,0]), numpy.array([9.4,0,2.7])]

#INITIALIZE
prev_time=0

def rssiToMeter(rssi, txPower =-90):
	if (rssi == 0):
		return CENTER_DIST
	ratio = float(rssi)/txPower
	if(ratio <1.0):
		return (261.23*ratio-176.14)/100
	else:
		meters = ((382.81)*pow(ratio, 14.693))/100
		return meters

def initialLocation(distances):
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

def translate(value, coordMin, coordMax, mapMin, mapMax):
    # Figure out how 'wide' each range is
    coordSpan = coordMax - coordMin
    mapSpan = mapMax - mapMin
    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - coordMin) / float(coordSpan)
    # Convert the 0-1 range into a value in the right range.
    return mapMin + (valueScaled * mapSpan)

def makeMap(xc,yc, xmax = 9.4, ymax = 11.31):
	imageFile = "code.jpg"
	im = Image.open(imageFile)
	draw = ImageDraw.Draw(im)
	#translte arguements depend on orintation of map
	x = translate(yc, 0, ymax, 0, im.size[0])
	y = translate(xc, 0, xmax, 0, im.size[1])
	draw.ellipse([x-RAD, y-RAD, x+RAD, y+RAD], fill =128)
	del draw
	im.show()
	im.save('location.png')

def main():
	rssi = [sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]]
	#print(rssi)
	distances = [rssiToMeter(rssi[0]), rssiToMeter(rssi[1]),rssiToMeter(rssi[2]), rssiToMeter(rssi[3])]
	#print (distances)
	result = optimize.minimize(
		mse,                         # The error function
		initialLocation(distances),            # The initial guess
		args=(locations, distances), # Additional parameters for mse
		method='L-BFGS-B',           # The optimisation algorithm
		options={'ftol':1e-5, 'maxiter': 1e+7 })      # Tolerance, # Maximum iterations
	location = result.x

	makeMap(float(location[0]), float(location[1]))
	
	#create a dictionary entry w/time stamp & convert to json
	data = {'chip'+str(CHIP_ID):{
		'raw_time': time.time(),
		'x-coordinate': float(location[0]), 
		'y-coordinate': float(location[1]), 
		'z-coordinate': float(location[2])}}
	j = json.dumps(data, sort_keys = True)
	headers = {'content-type':'application/json'}
	#r = requests.post(URL, data=j , headers=headers)
	print(j)
	return(j)

if __name__ == "__main__":
	main()
