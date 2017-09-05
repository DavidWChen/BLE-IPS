import numpy
from scipy import optimize
import math
import time

locations = [numpy.array([0,0,0]), numpy.array([0,3.91,2.7]), numpy.array([3.40,3.91,0]), numpy.array([3.40,0,2.7])]
CENTER_DIST = 5.84278 
CENTER_POINT = numpy.array([1.7,1.955, 1.35]) 

#Helper Functions

def rssiToMeter(rssi, txPower =-71.25):
    ratio = float(rssi)/txPower
    meters = ((1.2583)*pow(ratio, 8.2833))
    return meters
    
def mse(x, locations, distances):
    mse = 0.0
    for location, distance in zip(locations, distances):
        distance_calculated = numpy.linalg.norm(x-location)
        mse += math.pow(distance_calculated - distance, 2.0)
    return mse / len(locations)

def initialLocation(distances):
    data = zip(locations, distances)
    min_distance = CENTER_DIST #float('inf') : distance from beacon to center
    closest_location = CENTER_POINT #None: center point of room
    for member in data:
        if member[1] < min_distance:
            min_distance = member[1]
            closest_location = member[0]
    return closest_location

#Core Functions
def generateCoordinates(x=340,y=391,z=270):
    global actualcoordinates
    actualcoordinates = []
    for i in range(10, x+10,10):
        for j in range(10, y, 10):
            for k in range(10,z+10,10):
                actualcoordinates.append(numpy.array([0.01*(i),0.01*(j),0.01*(k)]))

    return actualcoordinates

def getDistances(actualcoordinates, c1 = numpy.array([0,0,0]), c2 = numpy.array([0,3.91,2.70]), c3 = numpy.array([3.40,3.91,0]), c4 = numpy.array([3.40,0,2.70])):
    #Parse out z-coordinate from array

    Distances = []

    # List of Distances from 0,0,0
    dis = []
    for a in range(len(actualcoordinates)):
        d1 = numpy.linalg.norm(actualcoordinates[a]-c1)
        dis.append(d1)

    # List of Distance from 0,5.67,2.7
    dis2 = []
    for c in range(len(actualcoordinates)):
        d2 = numpy.linalg.norm(actualcoordinates[c]-c2)
        dis2.append(d2)

    #List of Distance from 3.785,5.67,0
    dis3 = []
    for e in range(len(actualcoordinates)):
        d3 = numpy.linalg.norm(actualcoordinates[e]-c3)
        dis3.append(d3)

    
    #List of Distance from 3.785,0,2.7
    dis4 = []
    for g in range(len(actualcoordinates)):
        d4 = numpy.linalg.norm(actualcoordinates[g]-c4)
        dis4.append(d4)

    #Append to Array
    Distances = zip(dis,dis2,dis3,dis4)
    return Distances

def calc(dist):
    rssi = (pow(10,((math.log10(dist)/1.2583))/8.2833)*(-71.25))
    return int(round(rssi,0))

def getRSSI(Distances):
    RSSI = []
    for i in range(len(Distances)):
            rssi = [calc(Distances[i][0]), calc(Distances[i][1]), calc(Distances[i][2]), calc(Distances[i][3])]
            RSSI.append(rssi)
    
    return RSSI

def guessPoint(RSSI):
    distances = []
    for i in range(len(RSSI)):
        rssi = [rssiToMeter(RSSI[i][0]), rssiToMeter(RSSI[i][1]), rssiToMeter(RSSI[i][2]), rssiToMeter(RSSI[i][3])]
        distances.append(rssi)

    #print (distances)
    Results = []
    for a in range(len(distances)):
        result = optimize.minimize(mse,initialLocation(distances[a]),args=(locations, distances[a]), bounds=((0,3.40),(0,3.91),(0,2.70)), method='L-BFGS-B',options={'ftol':1e-5, 'maxiter': 1e+7 }) 
        Results.append(result.x)

    return Results

def main():
    points = guessPoint(getRSSI(getDistances(generateCoordinates())))

    Error = []

    for i in range(len(points)):
        DistanceError = numpy.linalg.norm(actualcoordinates[i]-points[i])
        Error.append(DistanceError)
    
    Sum = 0
    for j in range(len(Error)):
        Sum = Sum + Error[j]
    
    Avg = Sum/len(Error)


    print Avg
    print max(Error)
    print min(Error)

    print time.strftime('%T')
    
if __name__ == "__main__":
    print time.strftime('%T')
    main()


#Main


    
# def get2Dhyptoneuse(x, y):
#     #Get the x and y value inside array list
#     for location in beacons:
#         if location = 0:
#             #get hypotenuse from 0,0,0
#             h1 = math.sqrt(x**2 + y**2)
#             return h1
#         elif location = 1:
#             #get hypotenuse from 0,5.67,2.7
#             h2 = math.sqrt(x**2 + (5.67-y)**2)
#             return h2
#         elif location = 2:
#             #get hypotenuse from 3.785,5.67,0
#             h3 = math.sqrt((3.785-x)**2 + (5.67-y)**2)
#             return h3
#         else:
#             #get hypotenuse from 3.785,0,2.7
#             h4 = math.sqrt((3.785-x)**2 + 5.67**2)
#             return h4