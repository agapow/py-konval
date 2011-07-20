"""
Validators that remap values or check vocabulary membership.

"""

__docformat__ = "restructuredtext en"


### IMPORTS

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
			allow_others : bool
				allow non-listed values
		"""
		self.conv_dict = {}
		for t in vocab:
			t = impl.make_list (t)
			if canonize:
				k, v = impl.make_canonical(t[0]), impl.make_canonical(t[-1])
			else:
				k, v = t[0], t[-1]
			conv_dict[k] = v
		self.canonize = canonize
		self.allow_other = allow_other

	def convert_value (self, value):
		if self.canonize:
			value = impl.canonize(value)
		if self.allow_other:
			return self.conv_dict.get (value, value)
		else:
			return self.conv_dict[value]
		
		assert value in self._allowed_values, \
			"'%s' is not a recognised member of the vocabulary" % value
			
	def make_convert_error_msg (self, bad_val, err):
		"""
		Generate an meaningful error message for a membership problem.
		"""
		return "'%s' is not a member of %s" % (value, self.conv_dict.keys())



### END #######################################################################
