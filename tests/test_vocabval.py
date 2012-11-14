import unittest

from konval.basevalidator import ValidationError, ConversionError
from konval.vocabval import *

class TestVocabVal(unittest.TestCase):

	def test_synonyms(self):
		m = {'alpha': 'bravo', 'charlie': 'bravo', 'delta': 'echo'}
		v = Synonyms(m)

		self.assertEqual(v('alpha'), 'bravo')
		self.assertEqual(v('charlie'), 'bravo')
		self.assertEqual(v('delta'), 'echo')

		with self.assertRaises(ConversionError):
			v('foxtrot')

	def test_inlist(self):
		m = ['papa', 'yankee', 'tango', 'hotel', 'oscar', 'november']
		v = InList(m)

		self.assertEqual(v('papa'), 'papa')
		self.assertEqual(v('november'), 'november')
		self.assertEqual(v('PAPA'), 'papa')
		self.assertEqual(v(' PaPa '), 'papa')

		with self.assertRaises(ValidationError):
			v('juliet')

if __name__ == '__main__':
	unittest.main()