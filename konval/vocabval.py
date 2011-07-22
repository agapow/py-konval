"""
Validators that remap values or check vocabulary membership.

"""

__docformat__ = "restructuredtext en"


### IMPORTS

import impl
from basevalidator import BaseValidator


### CONSTANTS & DEFINES

### IMPLEMENTATION ###

class Synonyms (BaseValidator):
	"""
	Map values to other values.

	Note that this does not explicitly throw errors. If a value is un-mapped,
	it is simply returned.
	"""
	def __init__ (self, d):
		"""
		:Parameters:
			d
				a dictionary mapping input values to output values
				
		:Returns:
			the mapped value or the original is no mapping available
			
		For example::
		
			>>> d = {'foo': 1, 'bar': 2}
			>>> v = Synonyms(d)
			>>> v('foo')
			1
			>>> v('quux')
			'quux'
			
		"""
		self._syns = d

	def convert_value (self, value):
		return self._syns.get (value, value)


class Vocab (BaseValidator):
	"""
	Ensure values fall within a fixed set.
	"""
	
	def __init__ (self, vocab, canonize=False, allow_other=False):
		"""
		:Parameters:
			vocab
				a sequence of permitted values or value pairs (input and
				transformation)
			canonize : bool
				should all values be transformed to a canonical form
			allow_other : bool
				allow non-listed values
				
		:Returns:
			the original value, mapped & canonized if supplied and requested
			
		For example::
		
			>>> d = ['foo', ['bar', 'baz'], 'quux']
			>>> v = Vocab(d)
			>>> v('foo')
			'foo'
			>>> v('bar')
			'baz'
			>>> v('corge')
			Traceback (most recent call last):
			...
			ValueError: 'corge' is not a member of ['quux', 'foo', 'bar']
			>>> v = Vocab(d, allow_other=True)
			>>> v('corge')
			'corge'
			>>> v = Vocab(d, canonize=True, allow_other=True)
			>>> v('foo')
			'FOO'
			>>> v('bar')
			'BAZ'
			>>> v('corge')
			'CORGE'
			
			
		"""
		self.conv_dict = {}
		for t in vocab:
			t = impl.make_list (t)
			if canonize:
				k, v = impl.make_canonical(t[0]), impl.make_canonical(t[-1])
			else:
				k, v = t[0], t[-1]
			self.conv_dict[k] = v
		self.canonize = canonize
		self.allow_other = allow_other

	def convert_value (self, value):
		if self.canonize:
			value = impl.make_canonical (value)
		if self.allow_other:
			return self.conv_dict.get (value, value)
		else:
			return self.conv_dict[value]
			
	def make_conversion_error_msg (self, bad_val, err):
		"""
		Generate an meaningful error message for a membership problem.
		"""
		return "'%s' is not a member of %s" % (bad_val, self.conv_dict.keys())



## DEBUG & TEST ###

if __name__ == "__main__":
	import doctest
	doctest.testmod()




### END #######################################################################
