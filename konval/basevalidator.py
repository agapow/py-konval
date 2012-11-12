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

class ValidationError(Exception):
	pass

class ConversionError(Exception):
	pass