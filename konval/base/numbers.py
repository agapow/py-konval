from . import Konvalidator, KonversionError, ValidationError

class Range(Konvalidator):
	'''
	Only allow values between certain inclusive bounds.
	
	'''

	def __init__(self, minimum=None, maximum=None):
		self.minimum = minimum
		self.maximum = maximum

	def validate_value(self, value):
		if self.minimum and value < self.minimum:
			raise ValidationError('The specified value %s is below the required minimum %s' % (value, self.minimum))
		if self.maximum and value > self.maximum:
			raise ValidationError('The specified value %s is above the required maximum %s' % (value, self.maximum))
		
		return True

class Minimum(Range):
	def __init__ (self, minimum):
		super(Minimum, self).__init__(minimum=minimum)

class Maximum(Range):
	def __init__ (self, maximum):
		super(Maximum, self).__init__(maximum=maximum)

class Between(Konvalidator):
	'''
	Only allow values between certain exclusive bounds.

	'''

	def __init__(self, minimum=None, maximum=None):
		self.minimum = minimum
		self.maximum = maximum

	def validate_value(self, value):
		if self.minimum and value <= self.minimum:
			raise ValidationError('The specified value %s is not within lower bound %s' % (value, self.minimum))
		if self.maximum and value >= self.maximum:
			raise ValidationError('The specified value %s is not within upper bound %s' % (value, self.maximum))
		
		return True

class IsEqual(Konvalidator):
	'''
	Make sure a value is equal to a pre-determined value.
	'''

	def __init__(self, equal):
		self.equal = equal

	def validate_value(self, value):
		if value != self.equal:
			raise ValidationError('The value %s is not equal to %s' % (value, self.equal))

		return True

class IsZero(IsEqual):
	'''
	Only allow zero.
	'''

	def __init__(self):
		super(IsZero, self).__init__(0)