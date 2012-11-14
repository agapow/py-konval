"""
Validators that remap values or check vocabulary membership.

"""

__docformat__ = "restructuredtext en"


import impl
from basevalidator import BaseValidator, ValidationError, ConversionError
from stringval import ToCanonical


class Synonyms (BaseValidator):
	"""
	Map values to other values.

	"""

	def __init__ (self, mapping):
		self.mapping = mapping

	def convert_value (self, value):
		if value not in self.mapping:
			raise ConversionError('The value %s has no valid synonym mapping in %s' % (value, self.mapping))
		
		return self.mapping[value]


class InList(BaseValidator):
	"""
	Ensure values fall within a pre-defined list.

	Canonization here is always used for validation.
	
	Conversion will return the canonized value.

	"""
	
	def __init__ (self, term_list):
		self.term_list = term_list

	def validate_value (self, value):
		v = ToCanonical().convert(value)
		if v not in self.term_list:
			raise ValidationError('Value %s is not in term list %s' % (value, self.term_list))

		return True

	def convert_value(self, value):
		v = ToCanonical().convert(value)
		return v