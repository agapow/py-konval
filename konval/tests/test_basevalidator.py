from nose.tools.trivial import assert_equal, assert_true, assert_false

import konval

def test_base_validator():
	validator = konval.BaseValidator()
	string = 'abc'
	test = validator.convert(string)
	assert_equal(test, string)

	test = validator.validate(string)
	assert_true(test)

def test_konval_object():
	test_schema = {
		u'name': [konval.IsType([str]), konval.IsNonBlank(), konval.LengthRange(max=15)],
		u'age': [konval.IsType([int]), konval.MinVal(13), konval.IsNotEmpty()],
		u'gender': [konval.InList([u'male', u'female', u'unspecified']), konval.IsNonBlank()]
	}

	obj = konval.Konval(test_schema)

	obj.process_value(u'name', u'Peter')

	assert_true(obj.is_valid())
	assert_equal(obj.get_processed()[u'name'], u'Peter')
	assert_equal(obj.get_valid()[u'name'], u'Peter')

	obj.reset()
	obj.process_value(u'name', 123)
	assert_false(obj.is_valid())
	assert_equal(obj.get_valid(), {})
	assert_equal(obj.get_errors().keys(), [u'name'])

	data = {u'name': u'Peter', u'age': 15, u'gender': u'male'}
	obj.reset()
	obj.process(data)
	
	assert_true(obj.is_valid())
	assert_equal(obj.get_valid().keys(), [u'gender', u'age', u'name'])
	assert_equal(obj.get_errors(), {})

	silly_data = {u'name': 123, u'age': u'not a number', u'gender': u'martian'}

	obj.reset()
	obj.process(silly_data)
	assert_false(obj.is_valid())
	assert_equal(obj.get_valid(), {})
	assert_equal(obj.get_errors().keys(), [u'gender', u'age', u'name'])