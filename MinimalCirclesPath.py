from math import sin, cos, radians, asin, atan2, sqrt, degrees, ceil, floor


def calculateBearing(startLat, startLon, destLat, destLon):
    startLatRad = radians(startLat)
    startLonRad = radians(startLon)
    destLatRad = radians(destLat)
    destLonRad = radians(destLon)

    deltaLon = destLonRad - startLonRad

    y = sin(deltaLon) * cos(destLatRad)
    x = cos(startLatRad) * sin(destLatRad) - sin(startLatRad) * cos(destLatRad) * cos(deltaLon)

    initialBearingRad = atan2(y, x)

    initialBearingDeg = degrees(initialBearingRad)
    compassBearing = (initialBearingDeg + 360) % 360

    return compassBearing

def nextPoint(startLat, startLong, bearingDegrees, distanceNm=100):

    earthRadiusNm = 3440.065  # Radius of the Earth in nautical miles

    # Convert latitude and longitude to radians
    startLanRad = radians(startLat)
    startLongRad = radians(startLong)
    bearingRad = radians(bearingDegrees)

    # Calculate angular distance
    angularDistanceRad = distanceNm / earthRadiusNm

    # Calculate destination latitude
    destLatRad = asin(sin(startLanRad) * cos(angularDistanceRad) +
                         cos(startLanRad) * sin(angularDistanceRad) * cos(bearingRad))

    # Calculate destination longitude
    destLongRad = startLongRad + atan2(sin(bearingRad) * sin(angularDistanceRad) * cos(startLanRad),
                                     cos(angularDistanceRad) - sin(startLanRad) * sin(destLatRad))

    # Convert latitude and longitude back to degrees
    destLat = degrees(destLatRad)
    destLong = degrees(destLongRad)

    return destLat, destLong

# used geeksforgeeks.org, gets the distance between two points on earth
def getDistance(startLat, startLong, destLat, destLong):
    earthRadiusNm = 3440.065  # Radius of the Earth in nautical miles

    # Convert latitude and longitude from degrees to radians
    startLat, startLong, destLat, destLong = map(radians, [startLat, startLong, destLat, destLong])

    # Calculate differences
    latDifference = destLat - startLat
    longDifference = destLong - startLong

    # Calculate distance using Haversine formula
    a = sin(latDifference / 2) ** 2 + cos(startLat) * cos(destLat) * sin(longDifference / 2) ** 2
    c = 2 * asin(sqrt(a))
    distanceNm = earthRadiusNm * c

    return distanceNm

# pathWidth is the desired scaned distance from play diameter, radius is radius of circle passed to NOTAM
def getPath( startLat, startLong, destLat, destLong, radius, pathWidth):
    
    # gets step distance (pythagorean theorum)
    stepDistance = 2 * sqrt((radius)**2-(pathWidth/2)**2)

    # gets direction
    bearing = calculateBearing(startLat, startLong, destLat, destLong)

    # updates the start so the area in the opposite direction of the path is right on the edge of the first circle
    updatedStart = nextPoint(startLat,startLong, bearing, radius - (pathWidth/2) )

    # updates the dest so that it is the furthest point on the path. This means going the pathWidth/2 past the dest
    updatedDest = nextPoint(destLat, destLong, bearing, (pathWidth/2))

    # gets total distance from start to finish
    totalDistance = getDistance(updatedStart[0], updatedStart[1], updatedDest[0], updatedDest[1])

    # List to return with path of points from start to dest
    coordList = [updatedStart]

    # loops for each step until passed the destination. range(split total distance minus area covered from start point)
    for _ in range(ceil((totalDistance - (stepDistance/2))/stepDistance)):
        nextLat, nextLong = nextPoint(coordList[-1][0],coordList[-1][1], bearing, stepDistance)
        coordList.append((nextLat, nextLong))

        # update bearing for next point 
        bearing = calculateBearing(nextLat, nextLong, destLat, destLong)
 
    return coordList
       


# THIS IS AN EXAMPLE
if __name__ == '__main__':
    pathList = getPath(startLat = 32.8968,  # DFW Latitude
                   startLong = -97.0380,  # DFW Longitude
                   destLat = 33.9416,  # LAX Latitude
                   destLong = -118.4085,  # LAX Longitude
                   radius = 100, 
                   pathWidth = 50)

    for i,item in enumerate(pathList):
        print(f"point #{i+1}) {item}\n")
