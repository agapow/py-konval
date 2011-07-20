"""
Validators that confirm or convert types.

"""

__docformat__ = "restructuredtext en"


### IMPORTS

from basevalidator import BaseValidator
from vocabval import Synonyms


### CONSTANTS & DEFINES

### IMPLEMENTATION ###

class ToType (BaseValidator):
	"""
	Convert a value to a given type.
	
	This is largely syntactic sugar: It will actually accept any callable as an
	argument, but is intended for use with class constructors. You could use
	raw types and classes, but this throws much nicer error messages. Conversion
	is done by simply passing a value to the parameter callable.
	
	"""

	def __init__ (self, to_type, type_name=None):
		"""
		Class c'tor, accepting a type.
		
		:Parameters:
			to_type : callable
				A class constructor (old or new style), built-in type, or function
				that can be called to convert a type and will throw if it fails.
			type_name : string
				A name for the type produced. If not supplied, it will be extracted
				from `to_type` if possible.
		
		"""
		self.to_type = to_type
		if type_name is None:
			# extract the name of the type
			# handle classes, old-style classes, built-in types & functions
			if hasattr (to_type, '__name__'):
				type_name = getattr (totype, '__name__')
			# lambdas and all other require explicit name
			assert (type_name not in [None, '<lambda>']), \
				"type validator requires type name for lambda"
		self.type_name = type_name
	
	def make_conversion_error_msg (self, bad_val, err):
		"""
		Generate an appropriate error message for type conversion problem.
		"""
		# TODO: shift to base class
		return "can't convert '%s' to %s" % (bad_val, self.type_name)
	
	def convert_value (self, value):
		return self.to_type (value)


class ToInt (BaseToType):
	"""
	Convert a value to an integer.
	
	While you could just use ``int``, this throws a much nicer error message.
	"""
	def __init__ (self):
		BaseToType.__init__ (self, int, type_name='integer')


class ToFloat (BaseValidator):
	"""
	Convert a value to a float.

	While you could just use ``float``, this throws a much nicer error message.
	"""
	def __init__ (self):
		BaseToType.__init__ (self, float)


class ToStr (BaseValidator):
	"""
	Convert a value to a string.

	While you could just use ``str``, this throws a much nicer error message.
	"""
	def __init__ (self):
		BaseToType.__init__ (self, float)


class IsInstance (BaseValidator):
	"""
	Checks that values are instances of a list of classes or their subclasses.
	"""
	def __init__ (self, allowed_classes):
		self.allowed_classes = allowed_classes
	
	def validate_value (self, value):
		if not isinstance (value, self.allowed_classes):
			self.raise_validation_error (bad_val, None)
		
	def make_validation_error_msg (self, bad_val, err):
		# TODO: shift to base class
		return "'%s' type is not one of %s" % (bad_val,
			', '.join([t.__name__ for t in allowed_classes]))


class IsType (BaseValidator):
	"""
	Checks that values are instances of a list of classes (not their subclasses).
	"""
	def __init__ (self, allowed_classes):
		self.allowed_classes = allowed_classes
	
	def validate_value (self, value):
		for t in self.allowed_classes:
			if type(value) is t:
				return
		self.raise_validation_error (bad_val, None)
		
	def make_validation_error_msg (self, bad_val, err):
		# TODO: shift to base class
		return "'%s' type is not an instance of %s" % (bad_val,
			', '.join([t.__name__ for t in allowed_classes]))


class IsSubclass (BaseValidator):
	"""
	Checks that values are subclasses (not instances) of a list of classes.
	"""
	def __init__ (self, allowed_classes):
		self.allowed_classes = allowed_classes
	
	def validate (self, value):
		if not issubclass (value, self.allowed_classes):
			self.raise_validation_error (bad_val, None)
		
	def make_validation_error_msg (self, bad_val, err):
		"""

		"""
		# TODO: shift to base class
		return "'%s' type is not a subclass of %s" % (bad_val,
			', '.join([t.__name__ for t in allowed_classes]))


class StrToBool (Synonyms):
	"""
	Converts common abbreviations for true-false to boolean values.
	"""
	def __init__ (self):
		Synonyms.__init__ (self, defs.TRUE_FALSE_DICT)

	def convert_value (self, value):
		return Synonyms.convert_value (self, value.strip().upper())
		
	def validate_value (self, value):
		assert value in defs.TRUE_FALSE_DICT.keys()
		
	def make_validation_error_msg (self, bad_val, err):
		return "can't recognise %s' as true or false" % (bad_val)



### END #######################################################################

