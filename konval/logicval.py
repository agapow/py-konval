"""
Validators that logically combine or work with other validators.

"""

__docformat__ = "restructuredtext en"


### IMPORTS

import exceptions

from basevalidator import BaseValidator


### CONSTANTS & DEFINES

### IMPLEMENTATION ###

class Or (BaseValidator):
	"""
	Given a list of validators, return the first that succeeds.
	
	This allows us to test against a series of cases, e.g. where a value can be
	an integer or string (``MAXVAL``, ``VERBOSE``) and return the result of
	the first successful validation. A default value can be supplied to return
	if all validators fail, otherwise the most recent error is propagated. 
	
	For example::
	
		>>> from konval import *
		>>> v = Or ([IsType(int), IsType(str)])
		>>> v(5)
		5
		>>> v("foo")
		'foo'
		>>> v (True)
		Traceback (most recent call last):
		...
		ValueError: can't convert 'True'
		>>> v = Or ([IsType(int), IsType(str)], default='bar')
		>>> v (True)
		'bar'

	"""
	def __init__ (self, validators, default=None):
		self.validators = validators
		self.default = default
	
	def convert_value (self, value):
		"""
		If any validator succeeds, return the result, else default.
		"""
		last_err = None
		for v in self.validators:
			try:
				new_val = v(value)
				return new_val
			except exceptions.Exception, err:
				last_err = err
			except:
				last_err = None
		if self.default is None:
			raise last_err
		else:
			return self.default


class Default (BaseValidator):
	"""
	Return the original value if True, otherwise the default.
	
	This is for the use case where if a value is defined, it is used, else a
	default is used. This might be used for interpreting commandline or config
	file values. "Defined" in this instance means "evaluates to True", although
	the test function can be defined, which will allow "false" values like
	``0`` or ``None`` to be returned.
	
	Note that this validator should never throw - all cases should be handled.
	
	For example::
	
		>>> v = Default (100)
		>>> v(5)
		5
		>>> v(0)
		100
		>>> v = Default ("default", test=lambda x: x not in ['0', 'none'])
		>>> v(0)
		0
		>>> v('none')
		'default'
		
	"""
	
	def __init__ (self, default, test=None):
		self.default = default
		if test is None:
			self.test = lambda x: x
		else:
			self.test = test
	
	def convert_value (self, value):
		"""
		If value (or test of value) evaluates as true, return value, else default.
		"""
		if self.test (value):
			return value
		else:
			return self.default


class Constant (BaseValidator):
	"""
	Return the same value for all inputs.
	
	It's difficult to think of any case where this would be necessary. It has
	been argued, that it is necessary for some uses of `Or` (e.g. if you want to
	return ``None`` as the default), but this is included mostly for
	completeness. 
	
	For example::
	
		>>> v = Constant("foo")
		>>> v (5)
		'foo'
	
	Idea flinched from FormEncode.
	"""

	def __init__ (self, value):
		self.value = value
	
	def convert_value (self, value):
		"""
		If value (or test of value) evaluates as true, return value, else default.
		"""
		return self.value



## DEBUG & TEST ###

if __name__ == "__main__":
	import doctest
	doctest.testmod()



### END #######################################################################
