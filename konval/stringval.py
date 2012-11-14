"""
Validators that clean or transform strings.

"""

__docformat__ = "restructuredtext en"

import re
from basevalidator import BaseValidator, ValidationError, ConversionError
import defs


class Strip(BaseValidator):
	"""
	Transform strings by stripping flanking space.

	"""

	def convert_value(self, value):
		try:
			stripped = value.strip()
			return stripped
		except:
			raise ConversionError('Cannot strip spaces from %s' % type(value))


class ToLower(BaseValidator):
	"""
	Transform string to lower case, conversion error on type exception
	
	"""
	
	def convert_value(self, value):
		try:
			lc = value.lower()
			return lc
		except:
			raise ConversionError('Cannot convert %s to lowercase.' % type(value))


class ToUpper(BaseValidator):
	"""
	Transform strings by converting to upper case.
		
	"""

	def convert_value (self, value):
		try:
			uc = value.upper()
			return uc
		except:
			raise ConversionError('Cannot covert %s to uppercase.' % type(value))


class IsNonBlank(BaseValidator):
	"""
	Only allow non-blank strings (i.e. those with a length more than 0).
	
	Spaces are stripped automatically for this validator to ensure that
	strings with only spaces are not allowed through.
		
	"""

	def validate_value (self, value):
		try:
			s = Strip().convert(value)
		except ConversionError:
			return False
			
		if len(s) <= 0:
			raise ValidationError('The value "%s" is blank!' % value)
		
		return True


class IsRegexMatch (BaseValidator):
	"""
	Only allow values that match a certain regular expression.
		
	"""

	def __init__ (self, pattern):
		self.re = re.compile (pattern)
		self.pattern = pattern

	def validate_value (self, value):
		result = self.re.match(value)
		if not result:
			raise ValidationError('The value %s does not match the pattern %s' % (value, self.pattern))
		
		return result

class IsPlainText(IsRegexMatch):
	"""
	Check the value only contains alphanumerics, underscores, hyphen or spaces.
	
	Useful for checking identifiers.
			
	Idea flinched from FormEncode.
	
	"""
	
	def __init__ (self):
		super(IsPlainText, self).__init__ (r'^[a-zA-Z_\-0-9 ]+$')

	def validate_value(self, value):
		try:
			super(IsPlainText, self).validate_value(value)
		except ValidationError:
			raise ValidationError('The value %s must be plain text only.' % value)

class ToCanonical (BaseValidator):
	"""
	Reduce strings to a canonical form.
	
	Canonical for this library is as follows:
	- Stripped spaces
	- Underscores instead of dashes or spaces
	- Lowercase
		
	"""

	def convert_value(self, value):
		try:
			new_val = value.strip().lower()
			new_val = defs.CANON_SPACE_RE.sub ('_', new_val)
			return new_val
		except:
			raise ConversionError('Could not convert %s to canonical form.' % type(value))