"""
Various functions for using validators.

"""
# TODO: "or" validator


__docformat__ = "restructuredtext en"


### IMPORTS

import exceptions

import impl

__all__ = [
	'sanitize',
	'select',
	'reject',
	'assert_sanity',
]


### CONSTANTS & DEFINES

### IMPLEMENTATION ###

def sanitize (val, validators):
	"""
	Check and/or convert a value, throwing an exception on failure.

	:Parameters:
		val
			the original value to be validated and/or converted
		validators
			a validator or sequence of validators or suitable objects

	:Returns:
		the converted value, or original one if only validation has occurred
		
	The core service method for konval, this can be used to check and convert
	data. Note that this accepts a single value - if you want to sanitize a 
	whole list in the same way, use a list comprehension.
				
	"""

	for c in impl.make_list (validators):
		val = c(val)
	return val


def select (vals, validators):
	"""
	Return those values that pass validation.
	
	Note that the converted values are returned.
	"""
	selected = []
	for v in impl.make_list (vals):
		try:
			selected.append (sanitize (v, validators))
		except:
			pass
	return selected


def reject (vals, validators):
	"""
	Return those values that fail validation.
	
	Note that non-converted values are returned.
	"""
	rejected = []
	for v in impl.make_list (vals):
		try:
			sanitize (v, validators)
		except:
			rejected.append (v)
	return rejected


def assert_sanity (val, validators):
	"""
	Use validators for assertion.
	
	This actually works much like `sanitize` other than converting errors to 
	AssertionErrors and serving as a signal of intent in code. Note that this 
	accepts a single value - If you want to  sanitize a whole list in the same 
	way, use a list comprehension.
	
	For example::
	
		>>> assert_sanity (1, int)
		1
		>>> from konval import IsEqualOrMore, ToLength
		>>> x = assert_sanity ('2', [float, IsEqualOrMore(1)])
		>>> x
		2.0
		>>> assert_sanity (['a', 'b'], [ToLength(), float, IsEqualOrMore(3)])
		Traceback (most recent call last):
		...
		AssertionError: 2.0 is lower than 3
		
	"""
	try:
		return sanitize (val, validators)
	except exceptions.Exception, err:
		raise exceptions.AssertionError (str (err))
	except:
		raise exceptions.AssertionError ("an error occurred when sanitizing '%s'" % val)



## DEBUG & TEST ###

if __name__ == "__main__":
	import doctest
	doctest.testmod()



### END #######################################################################
