from math import sin, cos, radians, asin, atan2, sqrt, degrees, ceil, floor
import geojson as gj
import json

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
    startLanRad = radians(startLat)
    startLongRad = radians(startLong)
    bearingRad = radians(bearingDegrees)

    angularDistanceRad = distanceNm / earthRadiusNm
    destLatRad = asin(sin(startLanRad) * cos(angularDistanceRad) +
                      cos(startLanRad) * sin(angularDistanceRad) * cos(bearingRad))
    destLongRad = startLongRad + atan2(sin(bearingRad) * sin(angularDistanceRad) * cos(startLanRad),
                                       cos(angularDistanceRad) - sin(startLanRad) * sin(destLatRad))

    destLat = degrees(destLatRad)
    destLong = degrees(destLongRad)
    return destLat, destLong

def getDistance(startLat, startLong, destLat, destLong):
    earthRadiusNm = 3440.065
    startLat, startLong, destLat, destLong = map(radians, [startLat, startLong, destLat, destLong])

    latDifference = destLat - startLat
    longDifference = destLong - startLong

    a = sin(latDifference / 2) ** 2 + cos(startLat) * cos(destLat) * sin(longDifference / 2) ** 2
    c = 2 * asin(sqrt(a))
    distanceNm = earthRadiusNm * c

    return distanceNm

def getPath(startLat, startLong, destLat, destLong, radius, pathWidth):
    stepDistance = 2 * sqrt((radius)**2 - (pathWidth/2)**2)
    bearing = calculateBearing(startLat, startLong, destLat, destLong)

    updatedStart = nextPoint(startLat, startLong, bearing, radius - (pathWidth/2))
    updatedDest = nextPoint(destLat, destLong, bearing, (pathWidth/2))

    totalDistance = getDistance(updatedStart[0], updatedStart[1], updatedDest[0], updatedDest[1])
    coordList = [updatedStart]

    for _ in range(ceil((totalDistance - (stepDistance/2))/stepDistance)):
        nextLat, nextLong = nextPoint(coordList[-1][0], coordList[-1][1], bearing, stepDistance)
        coordList.append((nextLat, nextLong))
        bearing = calculateBearing(nextLat, nextLong, destLat, destLong)

    return coordList

def createGeoJSON(coordList):
    features = []
    for latitude, longitude in coordList:
        features.append(gj.Feature(geometry=gj.Point((longitude, latitude))))
    feature_collection = gj.FeatureCollection(features)
    return feature_collection

if __name__ == '__main__':
    pathList = getPath(startLat = 32.8968,  # DFW Latitude
                       startLong = -97.0380,  # DFW Longitude
                       destLat = 33.9416,  # LAX Latitude
                       destLong = -118.4085,  # LAX Longitude
                       radius = 100, 
                       pathWidth = 50)
    # For output as GeoJSON
    geojson_result = createGeoJSON(pathList)

    # For printing points
    for i, item in enumerate(pathList):
        print(f"point #{i+1}) {item}\n")
