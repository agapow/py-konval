import unittest

from konval.basevalidator import ValidationError, ConversionError
from konval.numberval import *

class TestNumberVal(unittest.TestCase):

	def test_range(self):
		v = Range(min=1, max=5)
		
		self.assertEqual(v(1), 1)
		self.assertEqual(v(3), 3)
		self.assertEqual(v(5), 5)

		with self.assertRaises(ValidationError):
			v(0)

		with self.assertRaises(ValidationError):
			v(6)

	def test_minval(self):
		v = MinVal(5)

		self.assertEqual(v(6), 6)
		self.assertEqual(v(5), 5)

		with self.assertRaises(ValidationError):
			v(4)

	def test_maxval(self):
		v = MaxVal(5)

		self.assertEqual(v(4), 4)
		self.assertEqual(v(5), 5)

		with self.assertRaises(ValidationError):
			v(6)

	def test_between(self):
		v = Between(min=1, max=5)

		self.assertEqual(v(2), 2)

		with self.assertRaises(ValidationError):
			v(1)

		with self.assertRaises(ValidationError):
			v(5)

		with self.assertRaises(ValidationError):
			v(0)

		with self.assertRaises(ValidationError):
			v(6)