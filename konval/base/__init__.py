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

class KonvalResult(object):

	def __init__(self, schema):
		self.schema = schema
		self.errors = {}
		self.successes = {}

	def add_error(self, name, message):
		if name in self.schema.keys():
			if name not in self.errors.keys():
				self.errors[name] = []
			self.errors[name].append(message)

	def add_success(self, name, value):
		if name in self.schema.keys():
			self.successes[name] = value

	def get_errors(self):
		return dict((k, v) for k, v in self.errors.iteritems() if v != [])

	def get_valid(self):
		return dict((k, v) for k, v in self.successes.iteritems() if v is not None)

	def is_valid(self):
		return self.get_errors() == {}

	def get_value(self, name):
		try:
			return self.successes[name]
		except KeyError:
			return None

def validate(schema, data):
	result = KonvalResult(schema)
	for name, value in data.iteritems():
		if name in schema.keys():
			validators = schema[name]

			if type(validators) is not list:
				validators = [validators]
			for validator in validators:
				try:
					processed_value = validator(value)
					result.add_success(name, processed_value)
				except KonvalError as e:
					result.add_error(name, e.message)
	return result

class KonvalError(Exception): pass

class ValidationError(KonvalError): pass

class KonversionError(KonvalError): pass