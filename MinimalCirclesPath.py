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

# used geeksforgeeks.org
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

    # TODO For actual application you would need to capture N/S/E/W

    
      
    # gets total distance from start to finish
    totalDistance = getDistance(startLat, startLong, destLat, destLong)

    # gets step distance (pythagorean theorum)
    stepDistance = 2 * sqrt((radius)**2-(pathWidth/2)**2)

    # gets direction
    bearing = calculateBearing(startLat, startLong, destLat, destLong)


    # gets point to call NOTAM and include all of starting area from farther down path
    startPoint = nextPoint(startLat,startLong, bearing, radius - (pathWidth/2) )

    # List to return with path of points from start to dest
    coordList = [startPoint]

    # loops for each step until passed the destination
    for _ in range(floor((totalDistance - (radius - (pathWidth/2)))/stepDistance)):
        nextCircle = nextPoint(coordList[-1][0],coordList[-1][1], bearing, stepDistance)
        coordList.append(nextCircle)

    coordList.append((destLat, destLong))
    return coordList
       



# THIS IS AN EXAMPLE
# uncomment and run `python3 MinimalCirclesPath.py` to see example of what getPath() returns

pathList = getPath(startLat = 32.7767, startLong = 96.7970, destLat = 39.7392, destLong = 104.9903, radius = 100,  pathWidth = 50)
for i,item in enumerate(pathList):
    print(f"point #{i+1}) {item}\n")



