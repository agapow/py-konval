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
* functions for easily using validators in a variety of ways


Status
------

*konval* is in an exploratory state, having been produced to support another
package and see if use can be got out of generalising conversion. As such. it 
is still an early release and the API may change. Comment is invited.


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

Most commonly, konval will be used to check or clean values. Failures result in
exceptions being thrown::

	# convert user input to a actual integer
	>>> from konval import *
	>>> sanitize ('1.0', ToInt())
	1
	>>> sanitize ('one', ToInt())
	Traceback (most recent call last)
	...
	ValueError: can't convert '1.0' to integer
	
A single validator or list can be passed to `sanitize`. Failure in any will
result in any exception::

	# check a list has no more than 3 members
	>>> sanitize (['a', 'b', 'c'], [ToLength(),IsEqualOrLess(3)])
	3
	# check a password is long enough
	>>> sanitize ('mypass', [ToLength(),IsEqualOrMore(8)])
	Traceback (most recent call last)
	...
	ValueError: 6 is lower than 8

Any callable object that accepts and returns a single value can be used as a
validator::
	
	>>> from string import *
	>>> sanitize (" my title ", [strip, capitalize])
	'My title'

A rich library of prebuilt validators is supplied::

	>>> sanitize ('abcde', IsNonblank())
	'abcde'
	>>> sanitize (5, IsInRange(1,6))
	5
	>>> sanitize ('foo', Synonyms({'foo': 'bar', 'baz': 'quux'}))
	'bar'

Custom validators can easily be subclassed from a supplied base class::

	class IsFoo (BaseValidator):
		def validate_value (self, value):
			if value != 'foo':
				self.raise_validation_error (value)
			return True


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

