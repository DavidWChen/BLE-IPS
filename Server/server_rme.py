import numpy
import time
import math
from scipy import optimize
import json
import sys
from PIL import Image, ImageDraw, ImageFont
import os

#CONSTANTS
RAD = 20 #radius of marker on map (makeMap/PIL)
CHIP_ID = 1 #unique to chip
ROOMX = 3.4
ROOMY = 3.91
ROOMZ = 2.7

#Custom Constants for each Beacon
#txPower #Constant #Power # Intercept
beak = [[],[],[],[],[]]
#HM-10 6m calib
# beak[0] = [-53.271875, 0.780981093, 7.560401965, 0.143759333]
# beak[1] = [-52.523125, 0.748478338, 7.466859451, 0.222755831]
# beak[2] = [-52.74875,  0.990821161, 6.816424409, 0.114132889]
# beak[3] = [-51.126875, 0.567019708, 7.544558612, 0.087529552]
# beak[4] = [-56.68875,  0.817605163, 8.413765389, 0.150619058]
# hm-10 9m calib
# beak[0] = [-53.271875, 0.865997779, 6.671966657, 0.030395271 ]
# beak[1] = [-52.523125, 0.803602054, 6.328629529, 0.000632869 ]
# beak[2] = [-52.74875,  1.025328944, 6.282396721, 0.100437912 ]
# beak[3] = [-51.126875, 0.647572021, 6.549757098, 0.11833359  ]
# beak[4] = [-56.68875,  0.987488097, 7.527083279, -0.097823287]
#HM-10 New
# beak[0] = [-58.58, 1.435078656, 7.95861262,  -0.075405515]
# beak[1] = [-57.93, 0.85675138,  7.485017329, -0.070413823]
# beak[2] = [-53.54, 1.033530531, 6.960015713,  0.021849336]
# beak[3] = [-61.02, 1.949954006, 8.646893611, -0.184386183]
# beak[4] = [-61.83, 1.900078708, 8.742523826, -0.068671391]

#Seekcy Calib
beak[0] = [-71.25, 1.340229386, 8.204114342, 0.249993729]
beak[1] = [-74.22, 1.741886547, 8.119907761, 0.367144088]
beak[2] = [-66.9,  0.563158214, 9.463797027, 0.126813606]
beak[3] = [-68.52, 0.682448161, 9.067687555, 0.234432795]
beak[4] = [-75.36, 2.37342462,  6.165065024, 0.271584429]
#create room specs
locations = [numpy.array([0,0,0]),
			 numpy.array([0,ROOMY, ROOMZ]), 
			 numpy.array([ROOMX,ROOMY,0]), 
			 numpy.array([ROOMX,0,ROOMZ])]
ORIGIN = numpy.array([0,0,0])
LIMIT = numpy.array([ROOMX,ROOMY, ROOMZ])
CENTER_POINT = numpy.array([(ROOMX/2),(ROOMY/2), (ROOMZ/2)])
CENTER_DIST = numpy.linalg.norm(CENTER_POINT-locations[0])
MIN_DIST = 0.05 #m
MAX_DIST = numpy.linalg.norm(LIMIT-ORIGIN)

#convert rssis to distance in meters
def rssiToMeter(rssi, beak_id = 0):
	#determine which constants to use
	txPower =   beak[beak_id][0]
	constant =  beak[beak_id][1]
	power =     beak[beak_id][2]
	intercept = beak[beak_id][3]
	#calculate distance
	ratio = float(rssi)/txPower
	meters = (constant*pow(ratio, power)) - intercept
	#limit distance to a known range
	if meters>MAX_DIST:
		return MAX_DIST
	elif meters<MIN_DIST:
		return MIN_DIST
	else:
		return meters

#determines start point for minimization
def initialLocation(distances):
	data = zip(locations, distances)
	#start at center of the room
	min_distance = CENTER_DIST
	closest_location = CENTER_POINT
	#unless the item is closer to one of the beacons
	for member in data:
		if member[1] < min_distance:
			min_distance = member[1]
			closest_location = member[0]
	return closest_location

#calculates mean square error of 
#the distance from inital location to the beacons vs. 
#the distance calculated from the rssis
def mse(x, locations, distances):
	mse = 0.0
	for location, distance in zip(locations, distances):
		distance_calculated = numpy.linalg.norm(x-location)
		mse += math.pow(distance_calculated - distance, 2.0)
	return mse / len(locations)

#maps one range of values to another
def translate(value, coordMin, coordMax, mapMin, mapMax):
	# Figure out how 'wide' each range is
	coordSpan = coordMax - coordMin
	mapSpan = mapMax - mapMin
	# Convert the left range into a 0-1 range (float)
	valueScaled = float(value - coordMin) / float(coordSpan)
	# Convert the 0-1 range into a value in the right range.
	return mapMin + (valueScaled * mapSpan)

#indicates item location on a map
def makeMap(xc,yc, zc, xmax = ROOMX, ymax = ROOMY):
	#open black map and create an ImageDraw object
	imageFile = "smallroom.png"
	im = Image.open(imageFile)
	draw = ImageDraw.Draw(im)
	#translate arguments depending on orintation of map img
	x = translate(yc, 0, ymax, 0, im.size[0])
	y = translate(xc, 0, xmax, 0, im.size[1])
	curr_dir = os.path.dirname(__file__) #'/path/to/fonts/'
	serifFont = ImageFont.truetype(os.path.join(curr_dir, 'FreeSerif.ttf'), 32)
	#draw item location on map
	draw.ellipse([x-RAD, y-RAD, x+RAD, y+RAD], fill =128)
	#write coordinates
	draw.text ((x+RAD,y), str(format(xc, '.2f')) + ", " + str(format(yc, '.2f')) + ", " + str(format(zc, '.2f')), fill='black', font = serifFont)
	del draw
	#save map 
	im.save('location.png')

def main():
	#collect rssis & convert to distance
	rssi = [sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]]
	distances = [rssiToMeter(rssi[0],1), rssiToMeter(rssi[1],2),rssiToMeter(rssi[2],3), rssiToMeter(rssi[3],4)]
	#optimize predicted location by minmizing mse
	result = optimize.minimize(mse,initialLocation(distances),
			args=(locations, distances), 
			bounds = ((0,ROOMX), (0,ROOMY), (0, ROOMZ)),
			method='L-BFGS-B',
			options={'ftol':1e-5, 'maxiter': 1e+7 }) 
	location = result.x

	#create map png based on optimized coordinates
	makeMap(float(location[0]), float(location[1]), float(location[2]))
	
	#create a dictionary entry w/time stamp & convert to json
	data = {'chip'+str(CHIP_ID):{
		'raw_time': time.time(),
		'x-coordinate': float(location[0]),
		'y-coordinate': float(location[1]),
		'z-coordinate': float(location[2])}}
	j = json.dumps(data, sort_keys = True)
	headers = {'content-type':'application/json'}
	print(j)

if __name__ == "__main__":
	main()


