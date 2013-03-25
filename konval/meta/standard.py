from ..base import Konvalidator, KonversionError, ValidationError, And, Or, If, IfElse, Default, strings, types

import ipaddress

class IsAlpha(And):
	''' Accepts only strings with alphabetical characters, spaces, underscores or dashes '''

	def __init__(self):
		super(IsAlpha, self).__init__(
			(
				types.ToType(unicode),
				strings.IsRegexMatch(r'^[A-Z \-_]+$')
			),
			'The specified value %s is not a purely alphabetical string.' % repr(self.value)
		)

class IsAlphaNumeric(And):
	''' Accepts only strings with alphabetical characters, spaces and dashes '''

	def __init__(self):
		super(IsAlphaNumeric, self).__init__(
			(
				types.ToType(unicode),
				strings.IsRegexMatch(r'^[A-z \-_0-9]+$')
			),
			'The specified value %s is not a purely alphanumeric string.' % repr(self.value)
		)

class IsEmailAddress(And):
	def __init__(self):
		super(IsEmailAddress, self).__init__(
			(
				types.ToType(unicode),
				strings.IsRegexMatch(r'^[a-z0-9\._\+%-]+@[a-z0-9\.-]+(\.[A-Z]{2,4})+$')
			),
			'The specified value %s is not a valid email address' % repr(self.value)
		)

class IsName(And):
	'''
	Checks to make sure the string is a name. In otherwords,
	no numbers, symbols, or wierd punctuation.
	'''

	def __init__(self):
		super(IsName, self).__init__(
			(
				types.ToType(unicode),
				strings.IsRegexMatch(r'^[a-z \.]+$')
			),
			'The specified value %s is not a valid name.' % repr(self.value)
		)

class IsIpv4(And):
	'''
	See if string is a valid IP address
	'''

	def __init__(self):
		super(IsIpv4, self).__init__(
			(
				types.ToType(unicode),
				strings.IsRegexMatch(r'^([0-9]{1,3}\.){3}[0-9]{1,3}$'),
				types.ToType(ipaddress.IPv4Address)
			),
			'The specified value %s is not a valid IPV4 address.' % repr(self.value)
		)
