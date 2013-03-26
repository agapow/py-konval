class Konvalidator(object):
	'''
	The abstract base class for konvalidators.

	Override validate_value for validation logic.
	Override convert_vlaue for conversion logic.
	
	Use ValidationError for validation exceptions
	Use ConversionError for conversion exceptions
	
	Return True for successful validation
	Return value for successful conversion

	'''

	def __call__ (self, value):
		'''
		Validates and converts user input.
		
		Validation must happen before conversion because validation
		is always based on raw user input.

		Conversion is strictly for post-processing after input has been validated.
		'''
		
		self.validate(value)
		value = self.convert(value)
		return value

	def convert (self, value):
		'''
		The interface for invoking the converter

		'''

		converted_value = self.convert_value(value)
		return converted_value
	
	def convert_value (self, value):
		'''
		Transform a value to the desired form.
		
		Return converted value on success, exception on failure.

		'''
		return value
	
	def validate (self, value):
		'''
		The interface for invoking the validator

		'''

		self.validate_value(value)
		return value
	
	def validate_value (self, value):
		'''
		Check a value is of the desired form.
		
		Override this method, return True on success, raise exception on failture.
		
		'''
		return True

class Or(Konvalidator):
	'''
	Given a list of validators, return the first that succeeds.
	Raise last exception if none succeed.
	
	'''
	
	def __init__(self, validators):
		self.validators = validators
	
	def __call__(self, value):
		last_exception = None
		for validator in self.validators:
			try:
				valid_value = validator(value)
				return valid_value
			except KonvalError as e:
				last_exception = e

		raise last_exception


class And(Konvalidator):
	''' All validators must succeed. If a group specific error message is supplied
		it will be raised, otherwise the first error raised is thrown. 
	'''
	value = ''

	def __init__(self, validators, error_message=None):
		self.validators = validators
		self.error_message = error_message

	def __call__(self, value):
		self.value = value
		current_value = value
		for validator in self.validators:
			try:
				current_value = validator(current_value)
			except KonvalError as e:
				if self.error_message:
					raise KonvalError(self.error_message.format(value=current_value))
				else:
					raise e
		return current_value

class If(Konvalidator):
	''' If condition is satisfied, then validate / convert '''

	def __init__(self, condition, validator):
		self.condition = condition
		self.validator = validator

	def __call__(self, value):
		if self.condition:
			return self.validator(value)
		return value

class IfElse(Konvalidator):
	''' If first validator fails, try second one. '''

	def __init__(self, validator, other_validator):
		self.validator = validator
		self.other_validator = other_validator

	def __call__(self, value):
		try:
			return self.validator(value)
		except KonvalError:
			return self.other_validator(value)

class Default(Konvalidator):
	'''
	Return a default value if the supplied validator fails.
	This validator never throws, always returns a value.
	
	'''
	
	def __init__(self, validator, default):
		self.default = default
		self.validator = validator

	def __call__(self, value):
		try:
			valid_value = self.validator(value)
			return valid_value
		except KonvalError:
			return self.default

class Constant(Konvalidator):
	'''
	Return the same value for all inputs.

	'''

	def __init__(self, constant_value):
		self.constant_value = constant_value
	
	def __call__(self, value):
		return self.constant_value

class Konval(object):
	'''
	This service object encapsulates a convenient interface for 
	managing common operations on a single schema.

	Takes a schema that is simply a dictionary with the validators for
	each key as the corresponding value.

	Error and message handling are also encapsulated here in a convenient
	manner.

	See tests for examples.

	'''

	def __init__(self, schema):
		self.schema = schema
		self.reset()
		
	def reset(self):
		self.processed = dict.fromkeys(self.schema.keys(), None)
		self.errors = dict.fromkeys(self.schema.keys(), [])
		self.valid = True

	def process(self, pairs):
		for name, value in pairs.iteritems():
			self.process_value(name, value)

	def process_value(self,	 name, value):
		if name in self.schema.keys():
			self.errors[name] = []
			self.processed[name] = None
			validators = self.schema[name]
			
			if type(validators) is not list:
				validators = [validators]

			for validator in validators:
				try:
					processed_value = validator(value)
				except KonvalError as e:
					self.errors[name].append(e.message)

			if self.errors[name] == []:
				self.processed[name] = processed_value
	
	def get_processed(self):
		return self.processed

	def get_errors(self):
		return dict((k, v) for k, v in self.errors.iteritems() if v != [])

	def get_valid(self):
		return dict((k, v) for k, v in self.processed.iteritems() if v is not None)

	def is_valid(self):
		return self.get_errors() == {}


class KonvalError(Exception): pass

class ValidationError(KonvalError): pass

class KonversionError(KonvalError): pass