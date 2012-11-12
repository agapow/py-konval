import unittest
from konval.basevalidator import BaseValidator

class TestBaseValidator(unittest.TestCase):

	def setUp(self):
		self.bv = BaseValidator()

	def test_convert(self):
		test = self.bv.convert('abc')
		self.assertEqual(test, 'abc')

	def test_validate(self):
		test = self.bv.validate('abc')
		self.assertTrue(test)

if __name__ == '__main__':
	unittest.main()