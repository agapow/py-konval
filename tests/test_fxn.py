import unittest
from konval.fxn import *
from konval.containerval import ToLength, IsNotEmpty

class TestFxn(unittest.TestCase):

	"""
	def test_sanitize(self):
		r = sanitize(1, int)
		self.assertEquals(r, 1)

		with self.assertRaises((TypeError, ValueError)):
			r = sanitize(1, dict)

		validators = [IsNotEmpty()]

		r = sanitize(1, validators)
		self.assertEquals(r, 1)

		with self.assertRaises(ValueError):
			r = sanitize(0, validators)

		with self.assertRaises(ValueError):
			r = sanitize([], validators)

	"""