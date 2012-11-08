"""
Abstract base class for easy construction of validators.

"""

__docformat__ = "restructuredtext en"


### IMPORTS

import exceptions

import impl

__all__ = [
	'BaseValidator',
	'WrappingValidator',
]


### CONSTANTS & DEFINES

### IMPLEMENTATION ###

class BaseValidator (object):
	"""
	A base class for custom validators.

	The aim to make construction of new validators easy and quick. Ideally, with
	this as a base class, most subclasses should only need to override one method
	(``convert_value`` or ``validate_value``) and perhaps supply a c'tor if some state
	needs to be stored.
	"""

	def __call__ (self, value):
		"""
		Converts and validates user input.
		
		:Parameters:
			value
				value to be checked or transformed
		
		:Returns:
			the transformed or validated value
		
		This converts the passed value (via `convert`) and then validates it (via
		`validate`). It should throw an error if any problems. This is the primary
		entry-point for validator objects and could be overridden in a subclass if
		required. However, it would probably be easier done in other methods
		called by this.
		"""
		## Main:
		value = self.convert(value)
		self.validate (value)
		## Postconditions & return:
		return value

	def convert (self, value):
		"""
		Transform a value to the desired form.

		:Parameters:
			value
				value to be transformed

		:Returns:
			the transformed value

		This attempts to convert the passed value (via `convert_value`) and if
		successful returns the new value. If any exception is thrown by conversion,
		`raise_conversion_error` is called with the bad value and error (if any).
		Behaviour could be customised by overriding this in a subclass, but
		`convert_value` may be a better target.
		"""
		try:
			conv_val = self.convert_value (value)
			return conv_val
		except exceptions.Exception, err:
			self.raise_conversion_error (value, err)
		except:
			self.raise_conversion_error (value, None)
	
	def convert_value (self, value):
		"""
		Transform a value to the desired form.
		
		:Parameters:
			value
				value to be transformed
		
		:Returns:
			the transformed value
		
		This is the workhorse method that is called by `convert` to transform
		passed values. As such, errors are signalled by throwing a meaningful
		exception. This is one of the obvious and easiest places to customize
		behaviour by overriding in a subclass.
		"""
		return value
	
	def raise_conversion_error (self, bad_val, err):
		"""
		Raise an error for a conversion problem.
		
		:Parameters:
			bad_val
				The value that failed to convert.
			err : Exception, None
				The exception caught during conversion.
		
		Override in subclass if need be, for specific exception types and
		messages.
		"""
		# TODO: shift to base class
		raise exceptions.ValueError (self.make_conversion_error_msg (bad_val,
			err))
		
	def make_conversion_error_msg (self, bad_val, err):
		"""
		Generate an error message for a conversion problem.
		
		Parameters as per `raise_conversion_error`. Override in subclass if need
		be, for more specific and meaningful messages.
		"""
		# TODO: shift to base class
		return "can't convert '%s'" % bad_val
	
	def validate (self, value):
		"""
		Is this value correct or of the correct form?
		
		:Parameters:
			value
				value to be checked
		
		This checks the passed value (via `validate_value`) and if successful 
		returns the new value. If any exception is thrown by validation,
		`raise_validation_error` is called with the bad value and error (if any).
		Behaviour could be customised by overriding this in a subclass, but
		`validate_value` may be a better target.
		"""
		# NOTE: override in subclass
		# probably a series of assertions
		try:
			if self.validate_value (value):
				return
			else:
				raise
		except exceptions.Exception, err:
			self.raise_validation_error (value, err)
		except:
			self.raise_validation_error (value, None)
	
	def validate_value (self, value):
		"""
		Check a value is of the desired form.
		
		:Parameters:
			value
				value to be checked
				
		:Returns:
			success of validation. 
		
		This is the workhorse method that is called by `validate` to check
		passed values. As such, errors are signalled by either by throwing a 
		meaningful exception or by returning false. This is one of the obvious 
		and easiest places to customize behaviour by overriding in a subclass.
		"""
		return True
	
	def raise_validation_error (self, bad_val, err):
		"""
		Generate an error message for a validation problem.
		
		:Parameters:
			bad_val
				The value that failed to validate.
			err : Exception, None
				The exception caught during validation.
		
		Override in subclass if need be, for specific exception types and
		messages.
		"""
		# TODO: shift to base class
		raise exceptions.ValueError (self.make_validation_error_msg (bad_val,
			err))
		
	def make_validation_error_msg (self, bad_val, err):
		"""
		Generate an error message for a validation problem.
		
		Parameters as per `raise_validation_error`. Override in subclass if need
		be, for more specific and meaningful messages.
		"""
		# TODO: shift to base class
		return "can't validate '%s'" % (bad_val)


class WrappingValidator (BaseValidator):
	"""
	Wraps functions and possible error messages in a validator.
	
	This allows converting and validating functions to be easily encapsulated
	in a validator. Given the design of konval (any function that accepts & 
	returns a value can be used as a validator), this is only slightly useful.
	However it does allow useful error messages to be incorporated.
	
	Idea flinched from FormEncode.
	
	"""
	
	def __init__ (self, conv_fn=None, conv_msg=None, val_fn=None, val_msg=None):
		"""
		C'tor accepting functors for validation & conversion.
		
		:Parameters:
			conv_fn : callable
				performs conversion, should accept value and return transformed
			conv_msg : str
				string for error message in event of conversion failure
			val_fn : callable
				performs validation, should accept value and return success
			val_msg : str
				string for error message in event of validation failure
		
		`conv_fn` and `val_fn` can be any callable object (e.g. a class with
		`__call__`, lambda). Note that validation function should return not the
		value but validation success, or just raise an exception. Error
		message strings can include the keyword substitutions 'bad_val' and 'err'
		for the value that raised the exception and the exception itself.
		"""
		
		self.conv_fn = conv_fn
		self.conv_msg = conv_msg
		self.val_fn = val_fn
		self.val_msg = val_msg
	
	def convert_value (self, value):
		if self.conv_fn:
			return self.conv_fn (value)
		else:
			return value
		
	def make_conversion_error_msg (self, bad_val, err):
		if self.conv_msg:
			return self.conv_msg % {'bad_val': bad_val, 'err': err}
		else:
			return BaseValidator.make_conversion_error_msg (self, bad_val, err)
	
	def validate_value (self, value):
		if self.val_fn:
			return self.val_fn (value)
		else:
			return True
		
	def make_validation_error_msg (self, bad_val, err):
		if self.val_msg:
			return self.val_msg % {'bad_val': bad_val, 'err': err}
		else:
			return BaseValidator.make_validation_error_msg (self, bad_val, err)