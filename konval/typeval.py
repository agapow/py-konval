"""
Validators that confirm or convert types.

-- Note: removed all the proxy type shortcuts, no clear benefit to API

"""

__docformat__ = "restructuredtext en"

import defs
import types

from basevalidator import BaseValidator, ValidationError, ConversionError
from vocabval import Synonyms


class ToType(BaseValidator):
	"""
	Convert a value to a given type.
	
	Will actually accept any callable as an argument, but is intended for use 
	with class constructors. You could use raw types and classes, but this throws 
	much nicer error messages. Conversion is done by simply passing a value to 
	the parameter callable.
	
	"""

	def __init__ (self, to_type):
		
		self.to_type = to_type
		if hasattr (to_type, '__name__'):
			self.type_name = getattr (to_type, '__name__')
		else:
			self.type_name = 'the specified type.'

	def convert_value (self, value):
		try:
			new_type = self.to_type(value)
			return new_type
		except:
			raise ConversionError('The value %s could not be converted to %s' % (value, self.type_name))


class IsInstance(BaseValidator):
	"""
	Checks that values are instances of a list of classes or their subclasses.
			
	"""
	
	def __init__ (self, allowed_classes):
		self.allowed_classes = tuple(allowed_classes)
	
	def validate_value (self, value):
		try:
			result = isinstance(value, self.allowed_classes)
			if result:
				return result
		except:
			pass
		
		raise ValidationError('Value %s is not in the allowed class list: %s' % (value, self.allowed_classes))


class IsType(BaseValidator):
	"""
	Checks that values are instances of a list of classes (not their subclasses).
	
	"""
	
	def __init__ (self, allowed_classes):
		self.allowed_classes = allowed_classes
	
	def validate_value (self, value):
		try:
			for t in self.allowed_classes:
				if type(value) is t:
					return True
		except TypeError:
			raise Exception('You must use a list for allowed classes')
	
		raise ValidationError('The value %s is not any of the allowed types: %s' % (value, self.allowed_classes))		


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