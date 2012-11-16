"""
Validators that check value magnitude.

-- Note: removed Length() validator as it was a duplicate of CheckLength(), now renamed to LengthRange()

"""

__docformat__ = "restructuredtext en"

from basevalidator import BaseValidator, ValidationError, ConversionError


class Range(BaseValidator):
	"""
	Only allow values between certain inclusive bounds.
	
	"""

	def __init__ (self, min=None, max=None):
		self.min = min
		self.max = max

	def validate_value(self, value):
		if self.min is not None and value < self.min:
			raise ValidationError('The specified value %s is below the required minimum %s' % (value, self.min))
		if self.max is not None and value > self.max:
			raise ValidationError('The specified value %s is above the required maximum %s' % (value, self.max))
		
		return True

class MinVal(Range):
	def __init__ (self, minimum):
		super(MinVal, self).__init__(min=minimum)


class MaxVal(Range):
	def __init__ (self, maximum):
		super(MaxVal, self).__init__(max=maximum)

class Between(BaseValidator):
	"""
	Only allow values between certain exclusive bounds.

	"""

	def __init__(self, min=None, max=None):
		self.min = min
		self.max = max

	def validate_value(self, value):
		if self.min is not None and value <= self.min:
			raise ValidationError('The specified value %s is not within lower bound %s' % (value, self.min))
		if self.max is not None and value >= self.max:
			raise ValidationError('The specified value %s is not within upper bound %s' % (value, self.max))
		
		return True

class IsEqual(BaseValidator):
	"""
	Make sure a value is equal to a pre-determined value.
	"""

	def __init__(self, equal):
		self.equal = equal

	def validate_value(self, value):
		if value != self.equal:
			raise ValidationError('The value %s is not equal to %s' % (value, self.equal))

		return True

class IsZero(IsEqual):
	"""
	Only allow zero.
	"""

	def __init__(self):
		super(IsZero, self).__init__(0)

