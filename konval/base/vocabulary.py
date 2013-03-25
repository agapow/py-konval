from . import Konvalidator, KonversionError, ValidationError, canonicals

class Synonyms(Konvalidator):
	'''
	Map values to other values.

	'''

	def __init__ (self, mapping):
		self.mapping = mapping

	def convert_value (self, value):
		if value not in self.mapping:
			raise KonversionError('The value %s has no valid synonym mapping in %s' % (repr(value), self.mapping))
		
		return self.mapping[value]


class InList(Konvalidator):
	'''
	Ensure values fall within a pre-defined list.
	'''
	
	def __init__ (self, term_list):
		self.term_list = term_list

	def validate_value (self, value):
		if value not in self.term_list:
			raise ValidationError('Value %s is not in term list %s' % (repr(value), self.term_list))
		return True