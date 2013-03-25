from . import Konvalidator, KonversionError, ValidationError


class ToLength(Konvalidator):
	'''
	Convert a sequence to its length.

	-- Note: int is cast to unicode
	
	'''
	
	def convert_value(self, value):
		try:
			length = len(value)
			return length
		except TypeError as e:
			if isinstance(value, int):
				return self.convert_value(unicode(value))

		raise KonversionError('Could not get length of %s.' % repr(value))


class LengthRange(Konvalidator):
	'''
	Only allow values of a certain sizes.

	Will work on most data types.
	
	'''

	def __init__ (self, minimum=None, maximum=None):
		self.minimum = minimum
		self.maximum = maximum

	def validate_value(self, value):
		length = ToLength().convert(value)
		
		if self.minimum and length < self.minimum:
			raise ValidationError('The value %s is less than the required minimum: %s' % (value, self.minimum))
		if self.maximum and length > self.maximum:
			raise ValidationError('The value %s is greater than the required maximum: %s' % (value, self.maximum))
		
		return True


class IsEmpty(Konvalidator):
	'''
	Checks the value is empty (an empty string, list, etc.)

	Uses LengthRange to determine emptiness.

	This method will not count a string '  ' as empty. Use the string validator IsEmpty for that.
	
	'''

	def validate_value(self, value):
		try:
			return LengthRange(max=0).validate(value)
		except ValidationError:
			raise ValidationError('The value "%s" is not empty.' % repr(value))


class IsNotEmpty(Konvalidator):
	'''
	Checks the value is not empty (a nonblank string, list with items, etc.)
	
	Uses LengthRange to determine non-emptiness
	
	'''

	def validate_value(self, value):
		try:
			return LengthRange(min=1).validate(value)
		except ValidationError:
			raise ValidationError('The value "%s" is empty.' % repr(value))