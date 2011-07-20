"""
Validators that clean or transform strings.

"""

__docformat__ = "restructuredtext en"


### IMPORTS

import re

from basevalidator import BaseValidator


### CONSTANTS & DEFINES

### IMPLEMENTATION ###

class Strip (BaseValidator):
	"""
	Transform strings by stripping flanking space.
	
	Note that this does not explicitly throw errors.
	"""
	def convert_value (self, value):
		return value.strip()


class ToLower (BaseValidator):
	"""
	Transform strings by converting to lower case.
	
	Note that this does not explicitly throw errors.
	"""
	def convert_value (self, value):
		return value.lower()


class ToUpper (BaseValidator):
	"""
	Transform strings by converting to upper case.
	
	Note that this does not explicitly throw errors.
	"""
	def convert_value (self, value):
		return value.upper()


class IsNonblank (BaseValidator):
	"""
	Only allow  non-blank strings (i.e. those with a length more than 0).
	"""
	def validate_value (self, value):
		assert isinstance (value, basestring)
		assert 0 < len(value), "can't be a blank string"


class IsRegexMatch (BaseValidator):
	"""
	Only allow values that match a certain regular expression.
	"""
	# TODO: compile flags?
	def __init__ (self, patt):
		self.re = re.compile (patt)
		self.patt = patt

	def validate_value (self, value):
		assert self.re.match (value)

	def make_validation_error_msg (self, bad_val, err):
		"""
		Generate an meaningful error message for an empty value.
		"""
		return "'%s' does not match the regex '%s'" % (bad_val, self.patt)


class IsPlainText(IsRegexMatch):
	"""
	Check the value only contains alphanumerics, underscores & hyphen.
	
	Useful for checking identifiers. Idea linched from FormEncode.
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
	"""
	def convert_value (self, value):
		new_val = value.strip().upper()
		new_val = CANON_SPACE_RE.sub ('_', value)
		return new_val





### END #######################################################################
