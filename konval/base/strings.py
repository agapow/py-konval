import re

from . import Konvalidator, KonversionError, ValidationError, canonicals

class ToStripped(Konvalidator):
	'''
	Transform strings by stripping flanking space.

	'''

	def convert_value(self, value):
		try:
			stripped = value.strip()
			return stripped
		except:
			raise KonversionError('Cannot strip spaces from %s' % repr(value))


class ToLower(Konvalidator):
	'''
	Transform string to lower case, conversion error on type exception
	
	'''
	
	def convert_value(self, value):
		try:
			lower_case = value.lower()
			return lower_case
		except:
			raise KonversionError('Cannot convert %s to lowercase.' % repr(value))


class ToUpper(Konvalidator):
	'''
	Transform strings by converting to upper case.
		
	'''

	def convert_value (self, value):
		try:
			upper_case = value.upper()
			return upper_case
		except:
			raise KonversionError('Cannot covert %s to uppercase.' % repr(value))

class IsRegexMatch(Konvalidator):
	'''
	Only allow values that match a certain regular expression.

	This uses a case insensitive match to add flexibility for strings
	that are going to be converted to lower (or upper) case anyway.
		
	'''

	def __init__(self, pattern):
		self.re = re.compile(pattern, re.IGNORECASE)
		self.pattern = pattern

	def validate_value(self, value):
		result = self.re.match(value)
		if not result:
			raise ValidationError('The value %s does not match the pattern %s' % (repr(value), self.pattern))
		return True

class ToCanonical(Konvalidator):
	'''
	Reduce strings to a canonical form.
	
	Canonical for this library is as follows:
	- Stripped spaces
	- Underscores instead of dashes or spaces
	- Lowercase
		
	'''

	def convert_value(self, value):
		try:
			canonical_value = canonicals.CANON_SPACE_RE.sub('_', value.strip().lower())
			return canonical_value
		except:
			raise KonversionError('Could not convert %s to canonical form.' % type(value))

class ToSlug(Konvalidator):
	''' Convert a string to a slug value '''

	def convert_value(self, value):
		try:
			clean_value = re.sub(canonicals.PUNCTUATION_RE, '', value)
			slug_value = re.sub(canonicals.SLUG_RE, '-', clean_value.lower())
			return slug_value
		except:
			raise KonversionError('Could not slugify %s' % repr(value))

class LengthRange(Konvalidator):
	''' Inclusive length range '''

	def __init__(self, minimum=None, maximum=None):
		self.minimum = minimum
		self.maximum = maximum

	def validate_value(self, value):
		if self.minimum and len(value) < self.minimum:
			raise ValidationError('The specified value %s is below the minimum length.' % repr(value))
		if self.maximum and len(value) > self.maximum:
			raise ValidationError('The specified value %s is below the maxium length.' % repr(value))
		return True

class LengthMinimum(LengthRange):
	''' Ensure minimum length string '''

	def __init__(self, minimum=None):
		super(LengthMinimum, self).__init__(minimum=minimum)

class LengthMaximum(LengthRange):
	''' Ensure maximum length string '''

	def __init__(self, maximum=None):
		super(LengthMaximum, self).__init__(maximum=maximum)

class LengthBetween(LengthRange):
	''' Ensure exclusive length bounds '''

	def validate_value(self, value):
		if self.minimum and len(value) <= self.minimum:
			raise ValidationError('The length of %s is not within lower bound %s' % repr(value))
		if self.maximum and len(value) >= self.maximum:
			raise ValidationError('The length of %s is not within upper bound %s' % repr(value))
		return True