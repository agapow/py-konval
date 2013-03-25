from nose.tools.trivial import assert_equal, assert_true, assert_false, assert_raises, assert_raises_regexp

import konval

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

def test_if(): pass

def test_if_else(): pass

def test_default(): pass

def test_constant(): pass

def test_konval(): pass