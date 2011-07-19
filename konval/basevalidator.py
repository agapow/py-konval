"""
Abstract base class for constructing validators.

"""

__docformat__ = "restructuredtext en"


### IMPORTS

### CONSTANTS & DEFINES

### IMPLEMENTATION ###

class BaseValidator (object):
	"""
	A base class for custom validators.

	Ideally, this should make validator subclasses simple to construct.  Derived
	valuidators will often only have to override one method (of ``__call__``,
	``convert`` and ``validate``) and perhaps supply a c'tor.
	"""

	def __call__ (self, value):
		"""
		Converts and validates user input.

		:Parameters:
			value
				value to be checked or transformed

		:Returns:
			the transformed or validated value

		Should throw an error if any problems. Override in subclass if required.
		"""
		# NOTE: override in subclass
		value = self.convert(value)
		self.validate (value)
		return value

	def validate (self, value):
		"""
		Is this value correct or of the correct form?

		:Parameters:
			value
				value to be checked

		Should throw an exception if validations fails.  Override in subclass if
		required.
		"""
		# NOTE: override in subclass
		# probably a series of assertions
		pass

	def convert (self, value):
		"""
		Transform this value to the desired form.

		:Parameters:
			value
				value to be transformed

		:Returns:
			the transformed value

		Can throw if conversion fails.  Override in subclass if required.
		"""
		# NOTE: override in subclass
		return value

	def make_conversion_error_msg (self, bad_val, err):
		"""
		Generate an error message for a conversion problem.

		:Parameters:
			bad_val
				The value that failed to convert.
			err : Exception, None
				The exception caught during conversion.

		Override in subclass if need be.
		"""
		# TODO: shift to base class
		return "can't convert '%s'" % bad_val

	def raise_conversion_error (self, bad_val, err):
		# TODO: shift to base class
		raise exceptions.ValueError (self.make_conversion_error_msg (bad_val,
			err))

	def make_validation_error_msg (self, bad_val, err):
		"""
		Generate an error message for a conversion problem.

		:Parameters:
			bad_val
				The value that failed to convert.
			err : Exception, None
				The exception caught during conversion.

		Override in subclass if need be.
		"""
		# TODO: shift to base class
		return "can't convert '%s' to %s" % (bad_val, type_name)

	def raise_validation_error (self, bad_val, err):
		# TODO: shift to base class
		raise exceptions.ValueError (self.make_validation_error_msg (bad_val,
			err))




### END #######################################################################
