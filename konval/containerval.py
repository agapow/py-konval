"""
Validators that check value size or length.

"""

__docformat__ = "restructuredtext en"

from basevalidator import BaseValidator, ValidationError, ConversionError


class ToLength (BaseValidator):
	"""
	Convert a sequence to its length.

	-- Note: int is cast to str
	
	"""
	
	def convert_value (self, value):
		try:
			length = len(value)
			return length
		except TypeError as e:
			if isinstance(value, int):
				return self.convert_value(str(value))

		raise ConversionError('Could not get length of "%s" of type %s' % (value, type(value)))


class LengthRange (BaseValidator):
	"""
	Only allow values of a certain sizes.

	Will work on most data types.
	
	"""

	def __init__ (self, min=None, max=None):
		self.min = min
		self.max = max

	def validate_value (self, value):
		length = ToLength().convert(value)
		
		if self.min is not None and length < self.min:
			raise ValidationError('The value %s is less than the required minimum: %s' % (value, self.min))
		if self.max is not None and length > self.max:
			raise ValidationError('The value %s is greater than the required maximum: %s' % (value, self.max))
		
		return True


class IsEmpty(BaseValidator):
	"""
	Checks the value is empty (an empty string, list, etc.)

	Proxies to check length to determine emptiness.

	This method will not count a string '  ' as empty. Use string validator for that.
	
	"""

	def validate_value(self, value):
		try:
			LengthRange(max=0).validate(value)
			return True
		except ValidationError:
			raise ValidationError('The specified "%s" is not empty.' % type(value))


class IsNotEmpty(BaseValidator):
	"""
	Checks the value is not empty (a nonblank string, list with items, etc.)
	
	Proxies to check length.
	
	"""

	def validate_value(self, value):
		try:
			LengthRange(min=1).validate(value)
			return True
		except ValidationError:
			raise ValidationError('The specified "%s" is empty.' % type(value))