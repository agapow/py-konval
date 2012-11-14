from konval.logicval import *
from konval.basevalidator import ValidationError, ConversionError
from konval.containerval import LengthRange, IsNotEmpty
import unittest

class TestLogicVal(unittest.TestCase):

	def test_or(self):
		l = ['a', 'b', 'c']
		
		v = Or([LengthRange(min=2, max=4), IsNotEmpty()])
		self.assertEqual(v(l), l)

		v = Or([IsNotEmpty(), LengthRange(min=2, max=4)])
		self.assertEqual(v(l), l)

		l = []
		with self.assertRaises(ValidationError):
			v(l)

		v = Or([IsNotEmpty(), LengthRange(min=2, max=4)], 'mah brand')
		self.assertEqual(v(l), 'mah brand')

	def test_default(self):
		v = Default('mah brand')

		self.assertEqual(v(''), 'mah brand')
		self.assertEqual(v(1), 1)

		f = lambda x: x > 3
		v = Default('mah brand', f)

		self.assertEqual(v(1), 'mah brand')
		self.assertEqual(v(4), 4)

	def test_constant(self):
		v = Constant('mah brand')

		self.assertEqual(v('something random'), 'mah brand')