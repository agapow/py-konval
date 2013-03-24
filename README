============
About konval
============

Background
----------

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

Status
------

This release is now fairly stable and well tested (all validators covered by extensive unittests)
and the service class provides a very straight forward API for using the library.

The library can always use more validators, and the validator modules may be rearranged 
in the coming weeks but the fundamental structure of the library is pretty stable.

Expecting to drive towards a 1.0 release over the next month that will include a rock-solid
API and at least 20-50 additional validators and covering tests.

Detailed documentation will follow closely alongside the 1.0 release.

Installation
------------

The simplest way to install *konval* is via ``easy_install`` [setuptools]_ or an
equivalent program::

	% easy_install konval

Alternatively the tarball can be downloaded, unpacked and ``setup.py`` run::

	% tar zxvf konval.tgz
	% cd konval
	% python set.py install

*konval* has no prerequisites and should work with just about any version of
Python.


Using konval
------------

A full API is included in the source distribution.


Examples
~~~~~~~~

1) Using the validators directly.

>>> v = IsType([str, int])
>>> v('123')
'123'
v({'obviously': 'not', 'a': 'string or int'})
ValidationError('Value {'obviously': 'not', 'a': 'string or int'} is not in the list of allowed types [<type str>, <type int>]')

2) Using the Konval service class
>>> schema = {
			'name': [IsType([str]), IsNonBlank(), LengthRange(max=50)],
			'age': [IsType([int]), IsNotEmpty()],
			'gender': [IsType([str]), InList(['male', 'female', 'not sure'])], IsNonBlank()]
		 }

>>> k = Konval(schema)
>>> data_set = {'name': 'Peter', 'age': 37, 'gender': 'male'}
>>> k.process(data_set)
>>> k.is_valid()
True
>>> k.get_valid()
{'name': 'Peter', 'age': 37, 'gender': 'male'}
>>> data_set = {'name': 1337, 'age': 'clearly not a number', 'gender': 'unknown'}
>>> k.process(data_set)
>>> k.is_valid()
False
>>> k.get_valid()
{}
>>> k.get_errors()
{'name': <explanation of error>, 'age': <explanation of error>, 'gender': <explanation of error>}




Limitations
-----------

*konval* is aimed at a one-way transformation of data, turning user input or
stored data *into* Python objects. Certainly it could be used in the reverse
direction, but this is not a primary use case. FormEncode is based around
two-way (round trip) conversion of data, so that may be a useful alternative.

The name *konval* was chosen because:

1. there's already a Python library called "sanity"

2. out of "valcon", "valkon", "conval" etc. it was the one with the fewest hits
   on Google


References
----------

.. [konval-home] `konval home page <http://www.agapow.net/software/py-konval>`__

.. [konval-pypi] `konval on PyPi <http://pypi.python.org/pypi/konval>`__

.. [setuptools] `Setuptools & easy_install <http://packages.python.org/distribute/easy_install.html>`__

.. [konval-github] `konval on github <https://github.com/agapow/py-konval>`__

.. [formencode] `FormEncode <http://formencode.org>`__

