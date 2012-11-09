import unittest
from konval.basevalidator import BaseValidator, WrappingValidator

class TestBaseValidator(unittest.TestCase):

	def setUp(self):
		self.bv = BaseValidator()

	def test_convert(self):
		test = self.bv.convert('abc')
		self.assertEqual(test, 'abc')

	def test_validate(self):
		test = self.bv.validate('abc')
		self.assertTrue(test)

	def test_wrapping_validator(self):
		conv_fn = lambda x: x.upper()
		conv_message = 'Cannot validate / convert a non-string value'
		val_fn = lambda x: isinstance(x, str)
		val_message = 'Value must be a string!'
		wv = WrappingValidator(conv_fn, conv_message, val_fn, val_message)

		r = wv.convert_value('abc')
		self.assertEqual(r, 'ABC')

		with self.assertRaises(AttributeError):
			wv.convert_value(123)

if __name__ == '__main__':
	unittest.main()