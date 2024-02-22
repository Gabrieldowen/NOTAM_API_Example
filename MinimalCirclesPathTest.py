from MinimalCirclesPath import *
import unittest

class TestMinimalCirclesPath(unittest.TestCase):
	def testGetDistance(self):
		# tests gets distance betweeen two points (haversine)
		# test data from https://www.nhc.noaa.gov/gccalc.shtml

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


	def testCalculateBearing(self):
		# tests method that gets bearing given two points
		# test data from https://www.movable-type.co.uk/scripts/latlong.html

		# DFW to DEN
		self.assertAlmostEqual(calculateBearing(32.897, -97.038, 39.862, -104.673), 320.78, places = 2)

	def testGetPath(self):
		# tests that the amount of points returned is less than the number of circles lined edge to edge
		# DFW to DEN
		radius = 100
		DFW_DEN = getPath(32.897, -97.038, 39.862, -104.673, radius, 50)

		# this is making sure the distance from the last search point encapsulates the final area we want covered
		# the radius of the NOTAM circle is greater than the distance from the last point to the dest plus the desired range
		self.assertGreater(radius, getDistance(DFW_DEN[-1][0], DFW_DEN[-1][1], 39.862,  -104.673)+(50/25))


		# HAX to MKO (two airports close in Muskogee Oklahoma)
		self.assertAlmostEqual(len(getPath(35.746, -95.413, 35.667, -95.367, 100, 50)), 1, places = 0)

