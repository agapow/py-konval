"""
Validators that clean or transform strings.

"""

__docformat__ = "restructuredtext en"

import re

import impl
from basevalidator import BaseValidator, ValidationError, ConversionError


class Strip(BaseValidator):
	"""
	Transform strings by stripping flanking space.
			
	"""

	def convert_value(self, value):
		try:
			stripped = value.strip()
			return stripped
		except:
			raise ConversionError('Cannot strip spaces from %s' % (type(value))


class ToLower(BaseValidator):
	"""
	Transform strings by converting to lower case.
	
	"""

	def convert_value (self, value):
		# lower case and return




class ToUpper (BaseValidator):
	"""
	Transform strings by converting to upper case.
	
	Note that this does not explicitly throw errors.
	
	For example::
	
		>>> v = ToUpper()
		>>> v ('aBcD')
		'ABCD'
	
	"""
	def convert_value (self, value):
		return value.upper()


class IsNonblank (BaseValidator):
	"""
	Only allow non-blank strings (i.e. those with a length more than 0).
	
	For example::
	
		>>> v = IsNonblank()
		>>> v ('abcd')
		'abcd'
		>>> v ('')
		Traceback (most recent call last):
		...
		ValueError: can't validate ''
		
	"""
	def validate_value (self, value):
		assert isinstance (value, basestring)
		assert 0 < len(value), "can't be a blank string"
		return True


class IsRegexMatch (BaseValidator):
	"""
	Only allow values that match a certain regular expression.
	
	For example::
	
		>>> v = IsRegexMatch('[a-z]+')
		>>> v ('abcd')
		'abcd'
		>>> v ('')
		Traceback (most recent call last):
		...
		ValueError: '' does not match the pattern '[a-z]+'
		
	"""
	# TODO: compile flags?
	def __init__ (self, patt):
		self.re = re.compile (patt)
		self.patt = patt

	def validate_value (self, value):
		return self.re.match (value)

	def make_validation_error_msg (self, bad_val, err):
		"""
		Generate an meaningful error message for an empty value.
		"""
		return "'%s' does not match the pattern '%s'" % (bad_val, self.patt)


class IsPlainText(IsRegexMatch):
	"""
	Check the value only contains alphanumerics, underscores & hyphen.
	
	Useful for checking identifiers.
	
	For example::
	
		>>> v = IsPlainText()
		>>> v ('abcd')
		'abcd'
		>>> v ('ab cd')
		Traceback (most recent call last):
		...
		ValueError: 'ab cd' is not plain text
		>>> v ('ab!cd')
		Traceback (most recent call last):
		...
		ValueError: 'ab!cd' is not plain text
		
	Idea flinched from FormEncode.
	"""
	def __init__ (self):
		IsRegexMatch.__init__ (self, r'^[a-zA-Z_\-0-9]*$')
		
	def make_validation_error_msg (self, bad_val, err):
		"""
		Generate an meaningful error message for an empty value.
		"""
		return "'%s' is not plain text" % (bad_val)


class ToCanonical (BaseValidator):
	"""
	Reduce strings to a canonical form.
	
	A common problem in cleaning user input is to catch trivial variants, e.g.
	how to recognise 'foo-bar', 'Foo-bar', ' foo-bar ' and 'foo_bar' as being
	the same value. This function achieves that by stripping flanking spaces, 
	converting letters to uppercase and converting internal stretches of spaces,
	underscores and hyphens to a single underscore. Thus, all of the previous 
	values would be converted to 'FOO_BAR'.
	
	For example::
	
		>>> v = ToCanonical()
		>>> v ('aBcD')
		'ABCD'
		>>> v ('  ab cd_')
		'AB_CD_'
		>>> v ('AB-_ CD')
		'AB_CD'
		
	"""
	def convert_value (self, value):
		return impl.make_canonical (value)