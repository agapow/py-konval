"""
Validators that logically combine or work with other validators.

"""

__docformat__ = "restructuredtext en"


import exceptions

from basevalidator import BaseValidator, ValidationError, ConversionError
from containerval import IsNotEmpty

class Or (BaseValidator):
	"""
	Given a list of validators, return the first that succeeds.
	
	Specify default value if all validators fail.
	
	"""
	
	def __init__ (self, validators, default=None):
		self.validators = validators
		self.default = default
	
	def convert_value (self, value):
		"""
		If any validator succeeds, return the result, else default.

		"""
		last_exception = None
		for v in self.validators:
			try:
				new_val = v(value)
				return new_val
			except (ValidationError, ConversionError) as e:
				last_exception = e
		
		if self.default is None:
			raise last_exception
		else:
			return self.default


class Default (BaseValidator):
	"""
	Return the original value if True, otherwise the default.
	
	Will use IsNotEmpty validator to determine emptiness unless custom function is specified.
	
	Note that this validator should never throw - all cases should be handled.

	This is useful to append as part of an Or instead of adding defaults to other validators.
	
	"""
	
	def __init__ (self, default, test=None):
		self.default = default
		if test is None:
			self.test = IsNotEmpty()
		else:
			self.test = test
	
	def convert_value (self, value):
		"""
		If value is not empty, return it, else default.

		The purpose of try block is for use with other validators

		The purpose of the conditional is for use with simple boolean functions

		"""

		try:
			if self.test(value):
				return value
		except:
			pass
		
		return self.default

class Constant (BaseValidator):
	"""
	Return the same value for all inputs.

	Idea flinched from FormEncode.

	"""

	def __init__ (self, value):
		self.value = value
	
	def convert_value (self, value):
		"""
		Return the specified value

		"""
		return self.value