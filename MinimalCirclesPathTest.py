from MinimalCirclesPath import *
import unittest

class TestMinimalCirclesPath(unittest.TestCase):

	# tests gets distance betweeen two points (haversine)
	# test data from https://www.nhc.noaa.gov/gccalc.shtml
	def testGetDistance(self):
		
		# DFW to DEN
		self.assertAlmostEqual(getDistance(32.897, -97.038, 39.862, -104.673), 557, places = 0)

		# TUL to WSG
		self.assertAlmostEqual(getDistance(36.198, -95.888, 40.167, -80.25), 774, places = 0)

		# RSW to LAX 
		self.assertAlmostEqual(getDistance(26.542, -81.755, 33.943, -118.407), 1940, places = -1)

		# HAX to MKO (two airports close in Muskogee Oklahoma)
		self.assertAlmostEqual(getDistance(35.746, -95.413, 35.667, -95.367), 5, places = 0)

		# japan to germany (CTS to ZVM)
		self.assertAlmostEqual(getDistance(42.8, 141.667, 49.467, -96.833), 4470, places = -1)


	# tests method that gets bearing given two points
	# test data from https://www.movable-type.co.uk/scripts/latlong.html
	def testCalculateBearing(self):
		
		# DFW to DEN
		self.assertAlmostEqual(calculateBearing(32.897, -97.038, 39.862, -104.673), 320.78, places = 2)


	# tests that the final NOTAM covers the furthest point we want covered
	def testGetPathFinalPoint(self):

		# DFW to DEN
		radius = 100
		destLat=39.862
		destLong=-104.673
		pathWidth=50
		bearing = 320.7808955450159

		# gets the final point we want covered
		updateDest = nextPoint(destLat, destLong, bearing, (pathWidth/2))

		# gets all the points for NOTAMs we would cover from DFW to DEN
		DFW_DEN = getPath(startLat=32.897, startLong=-97.038, destLat=destLat, destLong=destLong, radius=radius, pathWidth=pathWidth)

		# checks if the final NOTAM includes the last point we want covered
		self.assertGreater(radius, getDistance(DFW_DEN[-1][0], DFW_DEN[-1][1], updateDest[0], updateDest[1]))


	# tests that the amount of points returned is less than the number of circles lined edge to edge
	def testGetPathNumPoints(self):

		# HAX to MKO (two airports close in Muskogee Oklahoma)
		self.assertAlmostEqual(len(getPath(35.746, -95.413, 35.667, -95.367, 100, 50)), 1, places = 0)

if __name__ == '__main__':
    unittest.main()
