"""
Validators that check value size or length.

"""

__docformat__ = "restructuredtext en"


### IMPORTS

from basevalidator import BaseValidator


### CONSTANTS & DEFINES

### IMPLEMENTATION ###

class Length (BaseValidator):
	"""
	Only allow values of a certain sizes.

	Length limitations are expressed as (inclusive) minimum and maximum sizes.
	This is most useful for strings, but could be used for lists.
	"""
	def __init__ (self, min=None, max=None):
		self.min = min
		self.max = max

	def make_validation_error_msg (self, bad_val, err):
		"""
		Generate an meaningful error message for a length problem.
		"""
		if err:
			return str (err)
		else:
			return BaseValidator.make_validation_error_msg (self, bad_val, err)
		

	def validate_value (self, value):
		if self.min is not None:
			assert self.min <= len (value), "%s is shorter than %s" % (value, self.min)
		if self.max is not None:
			assert len (value) <= self.max, "%s is longer than %s" % (value, self.max)


# TODO: min & max length
# TODO: membership 

class IsEmpty(BaseValidator):
	"""
	Checks the value is empty (an empty string, list, etc.)
	"""
	def __init__ (self):
		Length.__init__ (self, max=0)
		
	def make_validation_error_msg (self, bad_val, err):
		"""
		Generate an meaningful error message for an empty value.
		"""
		return "'%s' is not empty" % (value, bad_val)


class IsNotEmpty(Length):
	"""
	Checks the value is not empty (an empty string, list, etc.)
	"""
	def __init__ (self):
		Length.__init__ (self, min=1)
		
	def make_validation_error_msg (self, bad_val, err):
		"""
		Generate an meaningful error message for an empty value.
		"""
		return "'%s' is empty" % (value, bad_val)


class IsMember (BaseValidator):
	"""
	Only allow values of a particular set.

	Length limitations are expressed as (inclusive) minimum and maximum sizes.
	This is most useful for strings, but could be used for lists.
	"""
	def __init__ (self, vocab):
		self.vocab = vocab

	def make_validation_error_msg (self, bad_val, err):
		"""
		Generate an meaningful error message for a membership problem.
		"""
		return "'%s' is not a member of %s" % (value, self.vocab)

	def validate_value (self, value):
		assert (value in self.vocab)


class ToIndex (BaseValidator):
	"""
	Convert to the index of the 

	Length limitations are expressed as (inclusive) minimum and maximum sizes.
	This is most useful for strings, but could be used for lists.
	"""
	def __init__ (self, vocab):
		self.vocab = vocab
	
	def make_conversion_error_msg (self, bad_val, err):
		"""
		Generate an meaningful error message for a membership problem.
		"""
		return "'%s' is not a member of %s" % (value, self.vocab)

	def convert_value (self, value):
		return self.vocab.index (value)


### END #######################################################################
