from . import Konvalidator, KonversionError, ValidationError

class ToType(Konvalidator):
	'''
	Convert a value to a given type.
	
	Will actually accept any callable as an argument, but is intended for use 
	with class constructors. You could use raw types and classes, but this throws 
	much nicer error messages. Conversion is done by simply passing a value to 
	the parameter callable.
	'''

	def __init__(self, to_type):
		self.to_type = to_type
		if hasattr (to_type, '__name__'):
			self.type_name = getattr(to_type, '__name__')
		else:
			self.type_name = 'the specified type.'

	def convert_value(self, value):
		try:
			new_type = self.to_type(value)
			return new_type
		except:
			raise KonversionError('The value %s could not be converted to %s' % (repr(value), self.type_name))


class IsInstance(Konvalidator):
	'''
	Checks that values are instances of a list of classes or their subclasses.
	'''
	
	def __init__(self, allowed_classes):
		self.allowed_classes = tuple(allowed_classes)
	
	def validate_value(self, value):
		result = isinstance(value, self.allowed_classes)
		if not result:
			raise ValidationError('Value %s is not in the allowed class list: %s' % (repr(value), self.allowed_classes))
		return True


class IsType(Konvalidator):
	'''
	Checks that values are instances of a list of classes (not their subclasses).
	
	'''
	
	def __init__(self, allowed_classes):
		if type(allowed_classes) is not list:
			allowed_classes = list(allowed_classes)
		self.allowed_classes = allowed_classes
	
	def validate_value(self, value):
		for allowed_class in self.allowed_classes:
			if type(value) is allowed_class:
				return True
		raise ValidationError('The value %s is not any of the allowed types: %s' % (repr(value), self.allowed_classes))