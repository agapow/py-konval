"""
Validators that remap values or check vocabulary membership.

"""

__docformat__ = "restructuredtext en"


import impl
from basevalidator import BaseValidator, ValidationError, ConversionError
from stringval import ToCanonical
import defs


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

	Canonization here is always used for validation,
	but value is returned as inputted.
	
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

class ToYesOrNo(Synonyms):
	"""
	Determines whether input is affirmative or negative based on
	the common English language interpretations of words and
	abbreviations as defined in the defs module.
		
	"""

	def __init__ (self):
		super(ToYesOrNo, self).__init__(defs.TRUE_FALSE_DICT)

	def convert_value (self, value):
		try:
			result = super(ToYesOrNo, self).convert_value(value.strip().upper())
			return result
		except:
			pass

		raise ConversionError('The value %s could not be determined as Yes or No' % value)