class ToYesOrNo(Synonyms):
	'''
	Determines whether input is affirmative or negative based on
	the common English language interpretations of words and
	abbreviations as defined in the defs module.
		
	'''

	def __init__(self):
		super(ToYesOrNo, self).__init__(canonicals.TRUE_FALSE_DICT)

	def convert_value(self, value):
		try:
			result = super(ToYesOrNo, self).convert_value(value.strip().upper())
			return result
		except:
			pass

		raise KonversionError('The value %s could not be determined as Yes or No' % value)