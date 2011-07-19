"""
Various functions for using validators.

"""
# TODO: "or" validator


__docformat__ = "restructuredtext en"


### IMPORTS

__all__ = [

]


### CONSTANTS & DEFINES

### IMPLEMENTATION ###

def validate (val, converters):
	"""
	Check and/or convert a value, throwing an exception on failure.

	:Parameters:
		val
			the original value to be validated and/or converted
		converters
			a sequence of converters

	:Returns:
		the converted value, or original one if only validation has occurred
	"""
	for c in converters:
		val = c(val)
	return val


# TODO: filter?
# TODO: assert


### END #######################################################################
