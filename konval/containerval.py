"""
Validators that check value size or length.

"""

__docformat__ = "restructuredtext en"


### IMPORTS

from basevalidator import BaseValidator


### CONSTANTS & DEFINES

### IMPLEMENTATION ###

class ToLength (BaseValidator):
	"""
	Convert a sequence to its length.

	--- len() obviously does not work on integers, fix applied
	--- not using the built in raise_exception methods because
	--- they strike me as redunant and inflexible as an alternative
	--- to using the standard library

	"""
	
	def convert_value (self, value):
		try:
			length = len(value)
			return length
		except TypeError as e:
			if isinstance(value, int):
				return self.convert_value(str(value))

		raise ValueError('Could not get length of "%s" of type %s' % (value, type(value)))


class CheckLength (BaseValidator):
	"""
	Only allow values of a certain sizes.

	Length limitations are expressed as (inclusive) minimum and maximum sizes.
	This is most useful for strings, but could be used for lists.
	
	"""

	def __init__ (self, min=None, max=None):
		self.min = min
		self.max = max

	def validate_value (self, value):
		if self.min is not None:
			assert self.min <= len (value), "'%s' is shorter than %s" % (value, self.min)
		if self.max is not None:
			assert len (value) <= self.max, "'%s' is longer than %s" % (value, self.max)
		return True


class IsEmpty(CheckLength):
	"""
	Checks the value is empty (an empty string, list, etc.)
	
	"""

	def __init__ (self):
		CheckLength.__init__ (self, max=0)


class IsNotEmpty(CheckLength):
	"""
	Checks the value is not empty (a nonblank string, list with items, etc.)
	
	If a string evaluates and there are no letters, does it still make a sound?
	Debatable whether that should be considered empty or not...
	
	"""

	def __init__ (self):
		CheckLength.__init__ (self, min=1)


class IsMember (BaseValidator):
	"""
	Only allow values of a particular set.

	Length limitations are expressed as (inclusive) minimum and maximum sizes.
	This is most useful for strings, but could be used for lists.
	
	"""

	def __init__ (self, vocab):
		self.vocab = vocab

	def validate_value (self, value):
		return value in self.vocab


class ToIndex (BaseValidator):
	"""
	Convert to the index of the 

	Length limitations are expressed as (inclusive) minimum and maximum sizes.
	This is most useful for strings, but could be used for lists.
	
	"""

	def __init__ (self, vocab):
		self.vocab = vocab

	def convert_value (self, value):
		return self.vocab.index (value)