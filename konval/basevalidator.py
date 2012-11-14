"""
Base Modules, includes exceptions
Abstract base class for easy construction of validators.

-- Note: removed WrappingValidator as it added no clear benefit.

"""

__docformat__ = "restructuredtext en"

import exceptions

import impl

__all__ = [
	'BaseValidator',
	'Konval',
	'ValidationError',
	'ConversionError',
]

class BaseValidator (object):
	"""
	A base class for custom validators.

	Override validate_value for validation logic.
	Override convert_vlaue for conversion logic.
	Use ValidationError for validation exceptions
	Use ConversionError for conversion exceptions
	Return True for successful validation
	Return value for successful conversion

	"""

	def __call__ (self, value):
		"""
		Validates and converts user input.
		
		Validation must happen before conversion because validation
		is always based on raw user input.

		Conversion is strictly for post-processing after input has been validated.
		"""
		
		self.validate(value)
		value = self.convert(value)
		return value

	def convert (self, value):
		"""
		The interface for invoking the converter

		"""

		conv_val = self.convert_value (value)
		return conv_val
	
	def convert_value (self, value):
		"""
		Transform a value to the desired form.
		
		Return converted value on success, exception on failure.

		"""
		return value
	
	def validate (self, value):
		"""
		The interface for invoking the validator

		"""

		self.validate_value(value)
		return value
	
	def validate_value (self, value):
		"""
		Check a value is of the desired form.
		
		Override this method, return True on success, raise exception on failture.
		
		"""
		return True

class Konval(object):
	"""
	The object that encapsulates a convenient service interface for 
	managing a batch validation operation and the 
	resulting errors and successes.

	Takes a schema that is simply a dictionary with the validators for
	each key as the corresponding value.

	See unit test for examples.

	"""

	def __init__(self, schema):
		self.schema = schema
		self.processed = dict.fromkeys(schema.keys(), None)
		self.errors = dict.fromkeys(schema.keys(), [])

	def process(self, pairs):
		self.valid = True
		for name, value in pairs.items():
			self.process_value(name, value)

	def process_value(self, name, value):
		if name in self.schema.keys():
			self.errors[name] = []
			self.processed[name] = None
			validators = self.schema[name]
			
			for v in validators:
				try:
					pr_value = v(value)
				except (ValidationError) as e:
					self.errors[name].append(e.message)

			if self.errors[name] == []:
				self.processed[name] = pr_value
	
	def get_processed(self):
		return self.processed

	def get_errors(self):
		return dict((k, v) for k, v in self.errors.iteritems() if v != [])

	def get_valid(self):
		return dict((k, v) for k, v in self.processed.iteritems() if v is not None)

	def is_valid(self):
		return self.get_errors() == {}


class ValidationError(Exception):
	pass

class ConversionError(Exception):
	pass