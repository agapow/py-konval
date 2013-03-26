from nose.tools.trivial import assert_equal, assert_true, assert_false, assert_raises, assert_raises_regexp, assert_is_not_none

import konval
from konval.meta.standard import IsEmailAddress, IsName

def test_konvalidator():
	konvalidator = konval.Konvalidator()
	value = 123
	assert_true(konvalidator.validate(value))
	assert_equal(konvalidator.convert(value), value)
	assert_equal(konvalidator(value), value)

def test_or():
	string_validator = konval.types.IsType(str)
	success_validator = konval.Konvalidator()

	or_validator = konval.Or((string_validator, success_validator))

	numerical_value = 123

	assert_true(or_validator.validate(numerical_value))
	assert_equal(or_validator.validate(numerical_value), numerical_value)

	size_validator = konval.numbers.Minimum(200)
	or_validator = konval.Or((string_validator, size_validator))

	with assert_raises(konval.KonvalError):
		or_validator(numerical_value)

def test_and():
	string_validator = konval.types.IsType(str)
	length_validator = konval.strings.LengthMinimum(10)

	failing_string = 'Hi there'

	and_validator = konval.And((string_validator, length_validator), 'There was a fail whale.')

	with assert_raises_regexp(konval.KonvalError, 'There was a fail whale'):
		and_validator(failing_string)

	succeeding_string = 'I am over ten characters!'

	assert_equal(and_validator(succeeding_string), succeeding_string)

	slug_converter = konval.strings.ToSlug()

	and_validator = konval.And((string_validator, length_validator, slug_converter), 'Oh noes!')

	assert_equal(and_validator(succeeding_string), 'i-am-over-ten-characters')

def test_if():
	if_validator = konval.If(True, konval.types.ToType(int))

	numerical_string = '1234'

	assert_equal(if_validator(numerical_string), 1234)

	if_validator = konval.If(False, konval.types.ToType(int))

	assert_equal(if_validator(numerical_string), numerical_string)

def test_if_else():
	if_else_validator = konval.IfElse(konval.types.IsType(str), konval.types.ToType(str))

	string_value = '1234'

	assert_equal(if_else_validator(string_value), string_value)

	numerical_value = 1234

	assert_equal(if_else_validator(numerical_value), string_value)

def test_default():
	default_validator = konval.Default(konval.types.IsType(str), 'NOT A STRING!')

	string_value = '1234'

	assert_equal(default_validator(string_value), string_value)

	numerical_value = 1234

	assert_equal(default_validator(numerical_value), 'NOT A STRING!')

def test_constant():
	constant_validator = konval.Constant('mah brand.')

	assert_equal(constant_validator('some data'), 'mah brand.')

def test_konval():
	test_schema = {
		u'name': IsName(),
		u'email': IsEmailAddress(),
		u'age': konval.types.IsType(int)
	}

	success_data = {
		u'name': u'Peter M. Elias',
		u'email': u'petermelias@gmail.com',
		u'age': 37
	}

	result = konval.validate(test_schema, success_data)
	assert_true(result.is_valid())

	fail_data = {
		u'name': 123,
		u'email': 1243,
		u'age': 'fourteen'
	}

	result = konval.validate(test_schema, fail_data)
	assert_false(result.is_valid())
	assert_is_not_none(result.get_errors())