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
	
	For example::
	
		>>> v = ToLength()
		>>> v("abc")
		3
		>>> v([1, 2])
		2
	
	"""
	
	def convert_value (self, value):
		return len (value)


class CheckLength (BaseValidator):
	"""
	Only allow values of a certain sizes.

	Length limitations are expressed as (inclusive) minimum and maximum sizes.
	This is most useful for strings, but could be used for lists.
	
	For example::
	
		>>> v = CheckLength(min=2, max=4)
		>>> v("abc")
		'abc'
		>>> v("abcde") #doctest: +ELLIPSIS
		Traceback (most recent call last):
		...
		ValueError: 'abcde' is longer than 4
		>>> v("a")
		Traceback (most recent call last):
		...
		ValueError: 'a' is shorter than 2
		>>> v = CheckLength(max=4)
		>>> v("abc")
		'abc'
		>>> v("abcde")
		Traceback (most recent call last):
		...
		ValueError: 'abcde' is longer than 4
		>>> v("a")
		'a'
		>>> v = CheckLength(min=2)
		>>> v("abc")
		'abc'
		>>> v("abcde")
		'abcde'
		>>> v("a")
		Traceback (most recent call last):
		...
		ValueError: 'a' is shorter than 2
	
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
			assert self.min <= len (value), "'%s' is shorter than %s" % (value, self.min)
		if self.max is not None:
			assert len (value) <= self.max, "'%s' is longer than %s" % (value, self.max)


# TODO: min & max length
# TODO: membership 

class IsEmpty(CheckLength):
	"""
	Checks the value is empty (an empty string, list, etc.)
	
	For example::
	
		>>> v = IsEmpty()
		>>> v("abc")
		Traceback (most recent call last):
		...
		ValueError: 'abc' is not empty
		>>> v([])
		[]
	
	"""
	def __init__ (self):
		CheckLength.__init__ (self, max=0)
		
	def make_validation_error_msg (self, bad_val, err):
		"""
		Generate an meaningful error message for an empty value.
		"""
		return "'%s' is not empty" % (bad_val)


class IsNotEmpty(CheckLength):
	"""
	Checks the value is not empty (a nonblank string, list with items, etc.)
	
	For example::
	
		>>> v = IsNotEmpty()
		>>> v("abc")
		'abc'
		>>> v([])
		Traceback (most recent call last):
		...
		ValueError: '[]' is empty
	
	"""
	def __init__ (self):
		CheckLength.__init__ (self, min=1)
		
	def make_validation_error_msg (self, bad_val, err):
		"""
		Generate an meaningful error message for an empty value.
		"""
		return "'%s' is empty" % (bad_val)


class IsMember (BaseValidator):
	"""
	Only allow values of a particular set.

	Length limitations are expressed as (inclusive) minimum and maximum sizes.
	This is most useful for strings, but could be used for lists.
	
	For example::
	
		>>> v = IsMember([1, 2, 3])
		>>> v(1)
		1
		>>> v(4)
		Traceback (most recent call last):
		...
		ValueError: '4' is not a member of [1, 2, 3]
	
	"""
	def __init__ (self, vocab):
		self.vocab = vocab

	def make_validation_error_msg (self, bad_val, err):
		"""
		Generate an meaningful error message for a membership problem.
		"""
		return "'%s' is not a member of %s" % (bad_val, self.vocab)

	def validate_value (self, value):
		assert (value in self.vocab)


class ToIndex (BaseValidator):
	"""
	Convert to the index of the 

	Length limitations are expressed as (inclusive) minimum and maximum sizes.
	This is most useful for strings, but could be used for lists.
	
	For example::
	
		>>> v = ToIndex(['a', 'b', 'c'])
		>>> v('a')
		0
		>>> v('d')
		Traceback (most recent call last):
		...
		ValueError: 'd' is not a member of ['a', 'b', 'c']
	
	"""
	def __init__ (self, vocab):
		self.vocab = vocab
	
	def make_conversion_error_msg (self, bad_val, err):
		"""
		Generate an meaningful error message for a membership problem.
		"""
		return "'%s' is not a member of %s" % (bad_val, self.vocab)

	def convert_value (self, value):
		return self.vocab.index (value)


## DEBUG & TEST ###

if __name__ == "__main__":
	import doctest
	doctest.testmod()


### END #######################################################################
