from MinimalCirclesPath import *
import unittest


# magic numbers for testGetPathFinalPoint
RADIUS = 100
PATHWIDTH=50
DFW_DEN_BEARING = 320.7808955450159
LAX_TUL_BEARING = 76.58706577831117

# airport coordinates for testing
DFW_COORDINATES = (32.897, -97.038)
DEN_COORDINATES = (39.862, -104.673)
TUL_COORDINATES = (36.198, -95.888)
WSG_COORDINATES = (40.167, -80.25)
RSW_COORDINATES = (26.542, -81.755)
LAX_COORDINATES = (33.943, -118.407)
HAX_COORDINATES = (35.746, -95.413)
MKO_COORDINATES = (35.667, -95.367)
CTS_COORDINATES = (42.8, 141.667)
ZVM_COORDINATES = (49.467, -96.833)

class TestMinimalCirclesPath(unittest.TestCase):

	# tests gets distance betweeen two points (haversine)
	# test data from https://www.nhc.noaa.gov/gccalc.shtml
	def testGetDistance(self):
		
		# DFW to DEN
		self.assertAlmostEqual(getDistance(DFW_COORDINATES[0], DFW_COORDINATES[1], DEN_COORDINATES[0], DEN_COORDINATES[1]), 557, places = 0)

		# TUL to WSG
		self.assertAlmostEqual(getDistance(TUL_COORDINATES[0], TUL_COORDINATES[1], WSG_COORDINATES[0], WSG_COORDINATES[1]), 774, places = 0)

		# RSW to LAX 
		self.assertAlmostEqual(getDistance(RSW_COORDINATES[0], RSW_COORDINATES[1], LAX_COORDINATES[0], LAX_COORDINATES[1]), 1940, places = -1)

		# HAX to MKO (two airports close in Muskogee Oklahoma)
		self.assertAlmostEqual(getDistance(HAX_COORDINATES[0], HAX_COORDINATES[1], MKO_COORDINATES[0], MKO_COORDINATES[1]), 5, places = 0)

		# japan to germany (CTS to ZVM)
		self.assertAlmostEqual(getDistance(CTS_COORDINATES[0], CTS_COORDINATES[1], ZVM_COORDINATES[0], ZVM_COORDINATES[1]), 4470, places = -1)

		# LAX to TUL
		self.assertAlmostEqual(getDistance(LAX_COORDINATES[0], LAX_COORDINATES[1], TUL_COORDINATES[0], TUL_COORDINATES[1]), 1112.300, places = 1)

	# tests method that gets bearing given two points
	# test data from https://www.movable-type.co.uk/scripts/latlong.html
	def testCalculateBearing(self):
		
		# DFW to DEN
		self.assertAlmostEqual(calculateBearing(DFW_COORDINATES[0], DFW_COORDINATES[1], DEN_COORDINATES[0], DEN_COORDINATES[1]), 320.78, places = 2)

		# LAX to TUL
		self.assertAlmostEqual(calculateBearing(LAX_COORDINATES[0], LAX_COORDINATES[1], TUL_COORDINATES[0], TUL_COORDINATES[1]), 76.59, places = 2)



	# tests that the final NOTAM covers the furthest point we want covered
	def testGetPathFinalPoint(self):

		# gets the final point we want covered
		updateDest = nextPoint(DEN_COORDINATES[0], DEN_COORDINATES[1], DFW_DEN_BEARING, (PATHWIDTH/2))

		# gets all the points for NOTAMs we would cover from DFW to DEN
		DFW_DEN = getPath(startLat=DFW_COORDINATES[0], startLong=DFW_COORDINATES[1], destLat=DEN_COORDINATES[0], destLong=DEN_COORDINATES[1], radius=RADIUS, pathWidth=PATHWIDTH)

		# checks if the final point would include the last point we want covered within RADIUS
		self.assertGreater(RADIUS, getDistance(DFW_DEN[-1][0], DFW_DEN[-1][1], updateDest[0], updateDest[1]))


		# gets the final point we want covered
		updateDestTUL = nextPoint(TUL_COORDINATES[0], TUL_COORDINATES[1], LAX_TUL_BEARING, (PATHWIDTH/2))

		# gets all the points for NOTAMs we would cover from DFW to DEN
		LAX_TUL = getPath(startLat=LAX_COORDINATES[0], startLong=LAX_COORDINATES[1], destLat=TUL_COORDINATES[0], destLong=TUL_COORDINATES[1], radius=RADIUS, pathWidth=PATHWIDTH)
		
		# checks if the final point would include the last point we want covered within RADIUS
		self.assertGreater(RADIUS, getDistance(LAX_TUL[-1][0], LAX_TUL[-1][1], updateDestTUL[0], updateDestTUL[1]))


	# tests that the amount of points returned is less than the number of circles lined edge to edge
	def testGetPathNumPoints(self):

		# HAX to MKO (two airports close in Muskogee Oklahoma)
		self.assertAlmostEqual(len(getPath(HAX_COORDINATES[0], HAX_COORDINATES[1], MKO_COORDINATES[0], MKO_COORDINATES[1], RADIUS, PATHWIDTH)), 1, places = 0)

if __name__ == '__main__':
    unittest.main()
