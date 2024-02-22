from MinimalCirclesPath import *
import unittest

class TestGetDistance(unittest.TestCase):
	def testUS(self):
		# tests gets distance betweeen two points (haversine)
		# test data from https://www.nhc.noaa.gov/gccalc.shtml

		# DFW to DEN
		self.assertAlmostEqual(getDistance(32.897, -97.038, 39.862, -104.673), 557, places = 0)

		# TUL to WSG
		self.assertAlmostEqual(getDistance(36.198, -95.888, 40.167, -80.25), 774, places = 0)

		# RSW to LAX 
		self.assertAlmostEqual(getDistance(26.542, -81.755, 33.943, -118.407), 1940, places = -1)

	def testForeign(self):
		# japan to germany (CTS to ZVM)
		self.assertAlmostEqual(getDistance(42.8, 141.667, 49.467, -96.833), 4470, places = -1)
