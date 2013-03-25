import unittest

from konval.basevalidator import ValidationError, ConversionError
from konval.typeval import *


class TestTypeVal(unittest.TestCase):

	def test_to_type(self):
		v = ToType(int)

		s = '132'
		self.assertEqual(v(s), 132)

		s = 132
		self.assertEqual(v(s), s)

		s = 'hello there'
		with self.assertRaises(ConversionError):
			v(s)

	def test_is_instance(self):
		v = IsInstance([int, str])

		s = 'i am a string'
		self.assertEqual(v(s), s)

		s = 1234
		self.assertEqual(v(s), s)

		s = []
		with self.assertRaises(ValidationError):
			v(s)

	def test_is_type(self):
		v = IsType([int, str])

		s = 'string'
		self.assertEqual(v(s), s)

		s = {}
		with self.assertRaises(ValidationError):
			v(s)