## Konval: validate without even trying.

![build status](https://travis-ci.org/petermelias/Py-konval.png?branch=master)

Konval is an input-agnostic validation and sanitization library that is
extremely easy to use.

Konval ships with common application validater / sanitizer functions to make
your life as developer even better.

Konval is built on a series of high level abstractions that make it very
easy and flexible to implement customized validation scenarios that can be
dropped in and re-used easily across your program.

### Simple validation

```python
import konval
from konval.meta.standard import IsName

# Quick validation

konval.quick(IsName(), 'Peter M. Elias')
True
konval.quick(IsName(), 123453254)
False

konval.quick([IsName(), LengthBetween(3, 50)], 'Peter M. Elias')
True

# One off validation with results

result = konval.once(IsName(), 'Peter M. Elias')
print result.is_valid()
True

print result.get_value()
u'Peter M. Elias'

# Repeatable validation with schema

schema = {u'name': IsName()}

result = konval.validate(schema, {u'name': 'Peter M. Elias'})

print result.is_valid()
True

result = konval.validate(schema, {u'name': 'Not a real name...4342398!!*#'})

print result.is_valid()
False
print result.get_errors()
{u'name': ['The specified value "Not a real name...4342398!!*#" is not a valid name.']}

```

### Installation

```python
pip install konval
```

### Features

* Includes a standard library of common validators
* Quick Boolean validation
* No strings attached one-off validation with results
* Schema validation for repeatable data defined validation
* Interface for automatically writing processed values to objects or data structures
* Predefined user friendly error messages for each validator
* Validator branching logic (AND, OR, IF, IFELSE, DEFAULT, CONSTANT)
* Data sanitization (type conversion, common transformations)

## More examples

### Lower Level Objects

```python

# Some Base Validators

schema = {
	u'name': [IsType(str), LengthMinimum(10)],
	u'age': [IsType(int), Between(13, 75)]
}

# Combine Validators and Sanitizers

schema = {
	u'name': [IsType(str), LengthMinimum(10), ToType(unicode)],
	u'age': [IsType(str), ToType(int), Between(13, 75)]
}

# Use branching logic directly for complex schema

schema = {
	u'name': [IfElse(IsType(unicode), ToType(unicode)), LengthBetween(5, 255)],
	u'age': [Default(NotZero(), 13)]
}

# Extend Branching logic to create custom validation / sanitization chains

class IsStreet(And):

	def __init__(self):
		super(IsStreet, self).__init__(
			IsNonBlank(),
			IsRegexMatch(r'^[0-9]+ [a-z ]+$'),
			ToType(unicode),
			ToLower()
		)

result = konval.validate({u'street': IsStreet()}, {u'street': '1234 MOUNTAIN STREET'})

print result.get_value(u'street')
u'1234 mountain street'

```

## Quick Reference

### Some Common Validators

* IsAlpha
* IsAlphaNumeric
* IsEmailAddress
* IsName
* IsIpv4
* IsStreet
* IsZipcode
* IsNonBlank

### Validator modules (containing 10 - 15 low level validators each)

* Containers
* Numbers
* Strings
* Types
* Vocabulary

### Meta modules (containing application specific validators)

* Standard
* Form Input
* Command line input


## Background

Validation and conversion of data.

The problem of sanitizing data (checking correctness and transforming to a
useful form) is widespread throughout programming:

* How do I verify user input is correct?
* How do I munge data from a spreadsheet into dates and numbers?
* How do I convert raw database fields into a programmatic object?

Ian Bicking came up with a sensible idiom for this problem, embodied in his
Formencode library [formencode]_: validation and conversion are one and the same
thing, and can be handled by passing raw data through a chain of validators.
Each validator checks and/or transforms the data and passes it on to the next.

In this spirit, *konval* is a package that provides:

* a rich library of validation objects
* base classes for easily producing custom validators
* The Konval service class for easily validating a data set
  based on a predefined validator schema corresponding to input
  value names.

Konval is aimed at a one-way transformation of data, turning user input or
stored data into Python objects. Certainly it could be used in the reverse
direction, but this is not a primary use case. FormEncode is based around
two-way (round trip) conversion of data, so that may be a useful alternative.

The name *konval* was chosen because:

1. there's already a Python library called "sanity"

2. out of "valcon", "valkon", "conval" etc. it was the one with the fewest hits
   on Google


## References

.. [konval-home] `konval home page <http://www.agapow.net/software/py-konval>`__

.. [konval-pypi] `konval on PyPi <http://pypi.python.org/pypi/konval>`__

.. [setuptools] `Setuptools & easy_install <http://packages.python.org/distribute/easy_install.html>`__

.. [konval-github] `konval on github <https://github.com/agapow/py-konval>`__

.. [formencode] `FormEncode <http://formencode.org>`__

