import unittest
from konval.basevalidator import *
from konval.containerval import *
from konval.sizeval import *
from konval.stringval import *
from konval.typeval import *
from konval.vocabval import *

class TestBaseValidator(unittest.TestCase):

	def setUp(self):
		self.bv = BaseValidator()

	def test_convert(self):
		test = self.bv.convert('abc')
		self.assertEqual(test, 'abc')

	def test_validate(self):
		test = self.bv.validate('abc')
		self.assertTrue(test)

class TestKonval(unittest.TestCase):

	def setUp(self):
		schema = {
					'name': [IsType([str]), IsNonBlank(), LengthRange(max=15)],
					'age': [IsType([int]), MinVal(13), IsNotEmpty()],
					'gender': [InList(['male', 'female', 'unspecified']), IsNonBlank()]
				 }
		
		self.kv = Konval(schema)

	def test_process_value(self):
		self.kv.process_value('name', 'Peter')

		self.assertTrue(self.kv.is_valid())
		self.assertEqual(self.kv.get_processed()['name'], 'Peter')
		self.assertEqual(self.kv.get_valid()['name'], 'Peter')

		self.kv.process_value('name', 123)
		self.assertFalse(self.kv.is_valid())
		self.assertEqual(self.kv.get_valid(), {})
		self.assertEqual(self.kv.get_errors().keys(), ['name'])

		self.kv.process_value('name', '')
		self.assertFalse(self.kv.is_valid())
		self.assertEqual(self.kv.get_valid(), {})
		self.assertEqual(self.kv.get_errors().keys(), ['name'])
		
		self.kv.process_value('name', 'Shankramanalyman Garankahmnanan')
		self.assertFalse(self.kv.is_valid())
		self.assertEqual(self.kv.get_valid(), {})
		self.assertEqual(self.kv.get_errors().keys(), ['name'])

	def test_process(self):
		data = {'name': 'Peter', 'age': 15, 'gender': 'male'}
		self.kv.process(data)

		self.assertTrue(self.kv.is_valid())
		self.assertEqual(self.kv.get_valid().keys(), ['gender', 'age', 'name'])
		self.assertEqual(self.kv.get_errors(), {})

		data = {'name': 123, 'age': 'not a number', 'gender': 'martian'}
		self.kv.process(data)

		self.assertFalse(self.kv.is_valid())
		self.assertEqual(self.kv.get_valid(), {})
		self.assertEqual(self.kv.get_errors().keys(), ['gender', 'age', 'name'])

if __name__ == '__main__':
	unittest.main()