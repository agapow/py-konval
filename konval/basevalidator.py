"""
Abstract base class for easy construction of validators.

"""

__docformat__ = "restructuredtext en"

import exceptions

import impl

__all__ = [
	'BaseValidator',
	'WrappingValidator',
]

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
		
		value = self.convert(value)
		self.validate (value)
		return value

	def convert (self, value):
		"""
		Transform a value to the desired form.

		:Parameters:
			value
				value to be transformed

		:Returns:
			the transformed value

		Removing the raise_conversion_error implementation because
		it has no obvious benefit and seems to just overcomplicate
		the raising and handling of exceptions.

		Also, in situations where "smarter" recovery is desirable,
		the standard conversion_error system is inflexible.

		See the ToLength() validator for an example of why.

		"""

		conv_val = self.convert_value (value)
		return conv_val
	
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
	
	def validate (self, value):
		"""
		Is this value correct or of the correct form?
		
		:Parameters:
			value
				value to be checked
		
		This checks the passed value (via `validate_value`) and if successful 
		returns the new value.

		--- What needs to happen here is this method will allow exceptions
		--- to be passed up the chain for handling via the consuming code.
		--- This also allows FXNs like sanitize to be modified to store list
		--- of failures for eventual output to the UI

		"""
		
		self.validate_value(value)
		return value
	
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

		-- Might be cleaner to have the convert_value method catch all exceptions
		-- and wrap the message / type into the validation_error class rather than
		-- making the custom function code specify it each time manually. -PME
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
		
	def validate_value (self, value):
		if self.val_fn:
			return self.val_fn (value)
		else:
			return True