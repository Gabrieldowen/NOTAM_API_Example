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
def getDistance(lat1, lon1, lat2, lon2):
    earthRadiusNm = 3440.065  # Radius of the Earth in nautical miles

    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Calculate differences
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Calculate distance using Haversine formula
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    distanceNm = earthRadiusNm * c

    return distanceNm

# pathWidth is the desired scaned distance from play diameter, radius is radius of circle passed to NOTAM
def getMinimalCirclesPath( startLat = 32.7767, startLong = 96.7970, destLat = 39.7392, destLong = 104.9903, radius = 100,  pathWidth = 50 ):
    # TODO For actual application you would need to capture N/S/E/W

    # list of coordinates returned to call API with
    coordList = [(startLat, startLong)]
      
    # gets total distance from start to finish
    totalDistance = getDistance(startLat, startLong, destLat, destLong)

    # gets step distance (pythagorean theorum)
    stepDistance = sqrt((radius)**2-(pathWidth/2)**2)

    # gets direction
    bearing = calculateBearing(startLat, startLong, destLat, destLong)

    # loops for each step until passed the destination
    for _ in range(floor(totalDistance/stepDistance)):
        nextCircle = nextPoint(coordList[-1][0],coordList[-1][1], bearing, stepDistance)
        coordList.append(nextCircle)

    coordList.append((destLat, destLong))
    return coordList
       


print(getMinimalCirclesPath())