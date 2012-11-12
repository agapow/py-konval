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

	def test_checklength(self):
		v = CheckLength(min=5, max=10)

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

	def test_ismember(self):
		my_list = [1, 2, 3, 4, 5]
		my_dict = {'a': 1, 'b': 2, 'c': 3}
		my_set = set([1, 2, 3])
		my_tuple = (1, 2, 3)
		
		v = IsMember(my_list)
		with self.assertRaises(ValidationError):
			v(6)
		v(1)

		v = IsMember(my_dict)
		with self.assertRaises(ValidationError):
			v(9)
		v('a')

		v = IsMember(my_set)
		with self.assertRaises(ValidationError):
			v(5)
		v(3)

		v = IsMember(my_tuple)
		with self.assertRaises(ValidationError):
			v(5)
		v(1)

	def test_toindex(self):
		my_string = 'abc'
		my_list = [1, 2, 3]

		v = ToIndex(my_string)
		with self.assertRaises(ValidationError):
			v('d')
		v('a')

		v = ToIndex(my_list)
		with self.assertRaises(ValidationError):
			v(4)
		v(2)