import unittest

from konval.basevalidator import ValidationError, ConversionError
from konval.stringval import *

class TestStringVal(unittest.TestCase):

	def test_strip(self):
		v = Strip()
		s = ' a string with flanking spaces '

		self.assertEqual(v(s), 'a string with flanking spaces')

		s = 1337
		with self.assertRaises(ConversionError):
			v(s)

		s = 'a string with NO flanking spaces'

		self.assertEqual(v(s), s)

	def test_lower(self):
		v = ToLower()
		s = 'AN UPPERCASE STRING'

		self.assertEqual(v(s), 'an uppercase string')

		s = 1337
		with self.assertRaises(ConversionError):
			v(s)

		s = 'a lowercase string'
		self.assertEqual(v(s), s)

	def test_upper(self):
		v = ToUpper()
		s = 'a lowercase string'

		self.assertEqual(v(s), 'A LOWERCASE STRING')

		s = 1337

		with self.assertRaises(ConversionError):
			v(s)

		s = 'AN UPPERCASE STRING'
		self.assertEqual(v(s), s)

	def test_nonblank(self):
		v = IsNonBlank()
		s = ' this string is not blank '

		self.assertEqual(v(s), s)

		s = '  '
		with self.assertRaises(ValidationError):
			v(s)

		s = ''
		with self.assertRaises(ValidationError):
			v(s)

	def test_regex_match(self):
		p = r'^[a-zA-Z]+$'
		v = IsRegexMatch(p)
		
		s = 'thiswillmatch'
		self.assertEqual(v(s), s)

		s = 'this will not match'
		with self.assertRaises(ValidationError):
			v(s)

	def test_is_plain_text(self):
		v = IsPlainText()
		s = 'this is just plain text'

		self.assertEqual(v(s), s)

		s = '@)(($&*($@# some invalid shit'
		with self.assertRaises(ValidationError):
			v(s)

	def test_canonical(self):
		v = ToCanonical()
		c = 'foo_bar'

		s = 'foo-bar'
		self.assertEqual(v(s), c)
		
		s = 'Foo-bar'
		self.assertEqual(v(s), c)

		s = ' foo-bar '
		self.assertEqual(v(s), c)

		s = 'FOO_BAR'
		self.assertEqual(v(s), c)

		s = 'foo_bar'
		self.assertEqual(v(s), s)

		s = 1337
		with self.assertRaises(ConversionError):
			v(s)
