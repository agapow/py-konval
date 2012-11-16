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

		s = '@)(($&*($@# some invalid user garbage'
		with self.assertRaises(ValidationError):
			v(s)

	def test_email_address(self):
		v = IsEmailAddress()
		s = 'petermelias@gmail.com'

		self.assertEqual(v(s), s)

		s = 'peter m elias@gmail.foobar'
		with self.assertRaises(ValidationError):
			v(s)

		s = 'PETERMELIAS@GMAIL.COM'
		self.assertEqual(v(s), s)

	def test_is_name(self):
		v = IsName()
		s = 'Peter'

		self.assertEqual(v(s), s)

		s = 'peter'
		self.assertEqual(v(s), s)

		s = 'p3t3r'
		with self.assertRaises(ValidationError):
			v(s)

	def test_is_ipv4(self):
		v = IsIpv4()
		s = '127.0.0.1'

		self.assertEqual(v(s), s)

		s = 'blatantly not an ip address'
		with self.assertRaises(ValidationError):
			v(s)

		s = '1234.1234.1234.1337'
		with self.assertRaises(ValidationError):
			v(s)

		s = '1337.1337.1337.foobar'
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
