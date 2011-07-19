"""
Validators that confirm or convert types.

"""

__docformat__ = "restructuredtext en"


### IMPORTS

from basevalidator import BaseValidator


### CONSTANTS & DEFINES

### IMPLEMENTATION ###

class ToType (BaseValidator):
	"""
	Convert a value to a given type.
	
	This is largely syntactic sugar: It will actually accept any callable as an
	argument, but is intended for use with class constructors. You could use
	raw types and classes, but this throws much nicer error messages. Conversion
	is done by simply passing a value to the parameter callable.
	
	"""

	def __init__ (self, to_type, type_name=None):
		"""
		Class c'tor, accepting a type.
		
		:Parameters:
			to_type : callable
				A class constructor (old or new style), built-in type, or function
				that can be called to convert a type and will throw if it fails.
			type_name : string
				A name for the type produced. If not supplied, it will be extracted
				from `to_type` if possible.
		
		"""
		self.to_type = to_type
		if type_name is None:
			# extract the name of the type
			# handle classes, old-style classes, built-in types & functions
			if hasattr (to_type, '__name__'):
				type_name = getattr (totype, '__name__')
			# lambdas and all other require explicit name
			assert (type_name not in [None, '<lambda>']), \
				"type validator requires type name for lambda"
		self.type_name = type_name

	def make_error_msg (self, bad_val, err):
		"""
		Generate an error message for a conversion problem.
		
		:Parameters:
			bad_val
				The value that failed to convert.
			err : Exception, None
				The exception caught during conversion.
		
		Override in subclass if need be.
		"""
		# TODO: shift to base class
		return "can't convert '%s' to %s" % (bad_val, type_name)

	def raise_error (self, bad_val, err):
		# TODO: shift to base class
		raise exceptions.ValueError (self.make_error_msg (bad_val, err))

	def convert (self, value):
		try:
			conv_val = self.to_type (value)
			return conv_val
		except exceptions.Exception, err:
			self.raise_error (bad_val, err)
		except:
			self.raise_error (bad_val, None)


class ToInt (BaseToType):
	"""
	Convert a value to an integer.
	
	While you could just use ``int``, this throws a much nicer error message.
	"""
	def __init__ (self):
		BaseToType.__init__ (self, int, type_name='integer')


class ToFloat (BaseValidator):
	"""
	Convert a value to a float.

	While you could just use ``float``, this throws a much nicer error message.
	"""
	def __init__ (self):
		BaseToType.__init__ (self, float)


class ToStr (BaseValidator):
	"""
	Convert a value to a string.

	While you could just use ``str``, this throws a much nicer error message.
	"""
	def __init__ (self):
		BaseToType.__init__ (self, float)


class IsInstance (BaseValidator):
	def __init__ (self, allowed_classes):
		self.allowed_classes = allowed_classes
	
	def validate (self, value):
		if not isinstance (value, self.allowed_classes):
			self.raise_validation_error (bad_val, None)
		self.raise_validation_error (bad_val, None)
		
	def make_validation_error_msg (self, bad_val, err):
		"""

		"""
		# TODO: shift to base class
		return "'%s' type is not one of %s" % (bad_val,
			', '.join([t.__name__ for t in allowed_classes]))


class IsType (BaseValidator):
	def __init__ (self, allowed_classes):
		self.allowed_classes = allowed_classes
	
	def validate (self, value):
		for t in self.allowed_classes:
			if type(value) is t:
				return
		self.raise_validation_error (bad_val, None)
		
	def make_validation_error_msg (self, bad_val, err):
		"""

		"""
		# TODO: shift to base class
		return "'%s' type is not one of %s" % (bad_val,
			', '.join([t.__name__ for t in allowed_classes]))


class IsSubclass (BaseValidator):
	def __init__ (self, allowed_classes):
		self.allowed_classes = allowed_classes
	
	def validate (self, value):
		if not issubclass (value, self.allowed_classes):
			self.raise_validation_error (bad_val, None)
		
	def make_validation_error_msg (self, bad_val, err):
		"""

		"""
		# TODO: shift to base class
		return "'%s' type is not one of %s" % (bad_val,
			', '.join([t.__name__ for t in allowed_classes]))


class ConfirmType(FancyValidator):
    """
    Confirms that the input/output is of the proper type.

    Uses the parameters:

    subclass:
        The class or a tuple of classes; the item must be an instance
        of the class or a subclass.
    type:
        A type or tuple of types (or classes); the item must be of
        the exact class or type.  Subclasses are not allowed.

    Examples::

        >>> cint = ConfirmType(subclass=int)
        >>> cint.to_python(True)
        True
        >>> cint.to_python('1')
        Traceback (most recent call last):
            ...
        Invalid: '1' is not a subclass of <type 'int'>
        >>> cintfloat = ConfirmType(subclass=(float, int))
        >>> cintfloat.to_python(1.0), cintfloat.from_python(1.0)
        (1.0, 1.0)
        >>> cintfloat.to_python(1), cintfloat.from_python(1)
        (1, 1)
        >>> cintfloat.to_python(None)
        Traceback (most recent call last):
            ...
        Invalid: None is not a subclass of one of the types <type 'float'>, <type 'int'>
        >>> cint2 = ConfirmType(type=int)
        >>> cint2(accept_python=False).from_python(True)
        Traceback (most recent call last):
            ...
        Invalid: True must be of the type <type 'int'>
    """

    subclass = None
    type = None

    messages = dict(
        subclass=_('%(object)r is not a subclass of %(subclass)s'),
        inSubclass=_('%(object)r is not a subclass of one of the types %(subclassList)s'),
        inType=_('%(object)r must be one of the types %(typeList)s'),
        type=_('%(object)r must be of the type %(type)s'))

    def __init__(self, *args, **kw):
        FancyValidator.__init__(self, *args, **kw)
        if self.subclass:
            if isinstance(self.subclass, list):
                self.subclass = tuple(self.subclass)
            elif not isinstance(self.subclass, tuple):
                self.subclass = (self.subclass,)
            self.validate_python = self.confirm_subclass
        if self.type:
            if isinstance(self.type, list):
                self.type = tuple(self.type)
            elif not isinstance(self.type, tuple):
                self.type = (self.type,)
            self.validate_python = self.confirm_type

    def confirm_subclass(self, value, state):
        if not isinstance(value, self.subclass):
            if len(self.subclass) == 1:
                msg = self.message('subclass', state, object=value,
                                   subclass=self.subclass[0])
            else:
                subclass_list = ', '.join(map(str, self.subclass))
                msg = self.message('inSubclass', state, object=value,
                                   subclassList=subclass_list)
            raise Invalid(msg, value, state)

    def confirm_type(self, value, state):
        for t in self.type:
            if type(value) is t:
                break
        else:
            if len(self.type) == 1:
                msg = self.message('type', state, object=value,
                                   type=self.type[0])
            else:
                msg = self.message('inType', state, object=value,
                                   typeList=', '.join(map(str, self.type)))
            raise Invalid(msg, value, state)
        return value

    def is_empty(self, value):
        return False