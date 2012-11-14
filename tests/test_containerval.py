import unittest

from konval.containerval import *
from konval.basevalidator import ValidationError, ConversionError


class TestContainerVal(unittest.TestCase):

	# len() function working as advertised, excellent.
	def test_tolength(self):
		v = ToLength()

		# str
		l = v('12345')
		self.assertEqual(l, 5)

		# list
		l = v([1, 2, 3])
		self.assertEqual(l, 3)

		# dict
		l = v({'a': 1, 'b': 2, 'c': 3, 'd': 4})
		self.assertEqual(l, 4)

		# tuple
		l = v((1, 2, 3, 4, 5, 6))
		self.assertEqual(l, 6)

		# unicode
		l = v(unicode('myunicodestring'))
		self.assertEqual(l, 15)

		# set
		l = v({'a', 'b', 'c'})
		self.assertEqual(l, 3)

		# bytearray
		l = v(bytearray(123))
		self.assertEqual(l, 123)

		# xrange
		l = v(xrange(5))
		self.assertEqual(l, 5)

	def test_lengthrange(self):
		v = LengthRange(min=5, max=10)

		with self.assertRaises(ValidationError):
			v([1, 2])

		with self.assertRaises(ValidationError):
			v([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

		v([1, 2, 3, 4, 5, 6])

	def test_isempty(self):
		v = IsEmpty()

		with self.assertRaises(ValidationError):
			v([1, 2])

		with self.assertRaises(ValidationError):
			v({'a': 1, 'b': 2})

		with self.assertRaises(ValidationError):
			v(1)

		with self.assertRaises(ValidationError):
			v('a')

		with self.assertRaises(ValidationError):
			v("b")

		with self.assertRaises(ValidationError):
			v(' ')

		with self.assertRaises(ValidationError):
			v(" ")

	def test_isnotempty(self):
		v = IsNotEmpty()

		with self.assertRaises(ValidationError):
			v([])

		with self.assertRaises(ValidationError):
			v({})

		with self.assertRaises(ValidationError):
			t = ()
			v(t)
		
		with self.assertRaises(ValidationError):
			v('')

		with self.assertRaises(ValidationError):
			v("")

		# Use number validators to test for 0 or not, this will pass zeroes.
		self.assertEqual(v(0), 0)