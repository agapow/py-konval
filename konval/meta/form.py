from . import BaseValidator

class AutoForm(BaseValidator):
	''' Smart converter / validator for form input.
		Designed for incoming data that came via
		a form and needs to be casted to unicode if
		alphanumeric, or to a more specific datatype if
		the data obviously lends itself.
	'''

	def __init__(self, force_unicode=False):
		self.force_unicode = force_unicode

	def convert_value(self, value):


class IsPlainText(IsRegexMatch):
	'''
	Check the value only contains alphanumerics, underscores, hyphen or spaces.
	
	Useful for checking identifiers.
			
	Idea flinched from FormEncode.
	
	'''
	
	def __init__ (self):
		super(IsPlainText, self).__init__ (r'^[a-zA-Z_\-0-9 ]+$')

	def validate_value(self, value):
		try:
			super(IsPlainText, self).validate_value(value)
		except ValidationError:
			raise ValidationError('The value %s must be plain text only.' % value)


class IsEmailAddress(IsRegexMatch):
	'''
	See if string is a valid email
	'''

	def __init__(self):
		super(IsEmailAddress, self).__init__(r'^[a-z0-9\._\+%-]+@[a-z0-9\.-]+(\.[A-Z]{2,4})+$')

	def validate_value(self, value):
		try:
			super(IsEmailAddress, self).validate_value(value)
		except ValidationError:
			raise ValidationError('The value %s is not a valid email address.' % value)

class IsName(IsRegexMatch):
	'''
	Checks to make sure the string is a name. In otherwords,
	no numbers, symbols, spaces or punctuation.
	'''

	def __init__(self):
		super(IsName, self).__init__(r'^[a-z]+$')

	def validate_value(self, value):
		try:
			super(IsName, self).validate_value(value)
		except ValidationError: 
			raise ValidationError('The value %s is not a valid name.' % value)

class IsIpv4(IsRegexMatch):
	'''
	See if string is a valid IP address
	'''

	def __init__(self):
		super(IsIpv4, self).__init__(r'^([0-9]{1,3}\.){3}[0-9]{1,3}$')

	def validate_value(self, value):
		try:
			super(IsIpv4, self).validate_value(value)
		except ValidationError:
			raise ValidationError('The value %s is not a valid ip address.' % value)

class IsAlpha(IsRegexMatch):
	''' Accepts only strings with alphabetical characters, spaces, underscores or dashes '''

	def __init__(self):
		super(IsAlpha, self).__init__(r'^[A-z \-_]+$')


	def validate_value(self, value):
		try:
			super(IsAlpha, self).validate_value(value)
		except ValidationError:
			raise ValidationError('The value %s is not a valid alphabetical string, containing only letters, dashes, underscores or spaces.' % value)

class IsAlphaNumeric(IsRegexMatch):
	''' Accepts only strings with alphabetical characters, spaces and dashes '''

	def __init__(self):
		super(IsAlphaNumeric, self).__init__(r'^[A-z \-_0-9]+$')


	def validate_value(self, value):
		try:
			super(IsAlphaNumeric, self).validate_value(value)
		except ValidationError:
			raise ValidationError('The value %s is not a valid alphanumeric string, containing only numbers, letters, dashes or spaces.' % value)