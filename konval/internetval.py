#
#
#
#
#
#class Constant(FancyValidator):
#    """
#    This converter converts everything to the same thing.
#
#    I.e., you pass in the constant value when initializing, then all
#    values get converted to that constant value.
#
#    This is only really useful for funny situations, like::
#
#      fromEmailValidator = ValidateAny(
#                               ValidEmailAddress(),
#                               Constant('unknown@localhost'))
#
#    In this case, the if the email is not valid
#    ``'unknown@localhost'`` will be used instead.  Of course, you
#    could use ``if_invalid`` instead.
#
#    Examples::
#
#        >>> Constant('X').to_python('y')
#        'X'
#    """
#
#    __unpackargs__ = ('value',)
#
#    def _to_python(self, value, state):
#        return self.value
#
#    _from_python = _to_python
#
#
#############################################################
### Normal validators
#############################################################
#
#
#
#
#
#
#
#class OneOf(FancyValidator):
#    """
#    Tests that the value is one of the members of a given list.
#
#    If ``testValueList=True``, then if the input value is a list or
#    tuple, all the members of the sequence will be checked (i.e., the
#    input must be a subset of the allowed values).
#
#    Use ``hideList=True`` to keep the list of valid values out of the
#    error message in exceptions.
#
#    Examples::
#
#        >>> oneof = OneOf([1, 2, 3])
#        >>> oneof.to_python(1)
#        1
#        >>> oneof.to_python(4)
#        Traceback (most recent call last):
#          ...
#        Invalid: Value must be one of: 1; 2; 3 (not 4)
#        >>> oneof(testValueList=True).to_python([2, 3, [1, 2, 3]])
#        [2, 3, [1, 2, 3]]
#        >>> oneof.to_python([2, 3, [1, 2, 3]])
#        Traceback (most recent call last):
#          ...
#        Invalid: Value must be one of: 1; 2; 3 (not [2, 3, [1, 2, 3]])
#    """
#
#    list = None
#    testValueList = False
#    hideList = False
#
#    __unpackargs__ = ('list',)
#
#    messages = dict(
#        invalid=_('Invalid value'),
#        notIn=_('Value must be one of: %(items)s (not %(value)r)'))
#
#    def validate_python(self, value, state):
#        if self.testValueList and isinstance(value, (list, tuple)):
#            for v in value:
#                self.validate_python(v, state)
#        else:
#            if not value in self.list:
#                if self.hideList:
#                    raise Invalid(self.message('invalid', state), value, state)
#                else:
#                    try:
#                        items = '; '.join(map(str, self.list))
#                    except UnicodeError:
#                        items = '; '.join(map(unicode, self.list))
#                    raise Invalid(
#                        self.message('notIn', state,
#                            items=items, value=value), value, state)
#
#
#
#
#class Email(FancyValidator):
#    r"""
#    Validate an email address.
#
#    If you pass ``resolve_domain=True``, then it will try to resolve
#    the domain name to make sure it's valid.  This takes longer, of
#    course.  You must have the `pyDNS <http://pydns.sf.net>`__ modules
#    installed to look up DNS (MX and A) records.
#
#    ::
#
#        >>> e = Email()
#        >>> e.to_python(' test@foo.com ')
#        'test@foo.com'
#        >>> e.to_python('test')
#        Traceback (most recent call last):
#            ...
#        Invalid: An email address must contain a single @
#        >>> e.to_python('test@foobar')
#        Traceback (most recent call last):
#            ...
#        Invalid: The domain portion of the email address is invalid (the portion after the @: foobar)
#        >>> e.to_python('test@foobar.com.5')
#        Traceback (most recent call last):
#            ...
#        Invalid: The domain portion of the email address is invalid (the portion after the @: foobar.com.5)
#        >>> e.to_python('test@foo..bar.com')
#        Traceback (most recent call last):
#            ...
#        Invalid: The domain portion of the email address is invalid (the portion after the @: foo..bar.com)
#        >>> e.to_python('test@.foo.bar.com')
#        Traceback (most recent call last):
#            ...
#        Invalid: The domain portion of the email address is invalid (the portion after the @: .foo.bar.com)
#        >>> e.to_python('nobody@xn--m7r7ml7t24h.com')
#        'nobody@xn--m7r7ml7t24h.com'
#        >>> e.to_python('o*reilly@test.com')
#        'o*reilly@test.com'
#        >>> e = Email(resolve_domain=True)
#        >>> e.resolve_domain
#        True
#        >>> e.to_python('doesnotexist@colorstudy.com')
#        'doesnotexist@colorstudy.com'
#        >>> e.to_python('test@nyu.edu')
#        'test@nyu.edu'
#        >>> # NOTE: If you do not have PyDNS installed this example won't work:
#        >>> e.to_python('test@thisdomaindoesnotexistithinkforsure.com')
#        Traceback (most recent call last):
#            ...
#        Invalid: The domain of the email address does not exist (the portion after the @: thisdomaindoesnotexistithinkforsure.com)
#        >>> e.to_python(u'test@google.com')
#        u'test@google.com'
#        >>> e = Email(not_empty=False)
#        >>> e.to_python('')
#
#    """
#
#    resolve_domain = False
#    resolve_timeout = 10 # timeout in seconds when resolving domains
#
#    usernameRE = re.compile(r"^[^ \t\n\r@<>()]+$", re.I)
#    domainRE = re.compile(r'''
#        ^(?:[a-z0-9][a-z0-9\-]{0,62}\.)+ # (sub)domain - alpha followed by 62max chars (63 total)
#        [a-z]{2,}$                       # TLD
#    ''', re.I | re.VERBOSE)
#
#    messages = dict(
#        empty=_('Please enter an email address'),
#        noAt=_('An email address must contain a single @'),
#        badUsername=_('The username portion of the email address is invalid'
#            ' (the portion before the @: %(username)s)'),
#        socketError=_('An error occured when trying to connect to the server:'
#            ' %(error)s'),
#        badDomain=_('The domain portion of the email address is invalid'
#            ' (the portion after the @: %(domain)s)'),
#        domainDoesNotExist=_('The domain of the email address does not exist'
#            ' (the portion after the @: %(domain)s)'))
#
#    def __init__(self, *args, **kw):
#        FancyValidator.__init__(self, *args, **kw)
#        if self.resolve_domain:
#            if not have_dns:
#                warnings.warn(
#                    "pyDNS <http://pydns.sf.net> is not installed on"
#                    " your system (or the DNS package cannot be found)."
#                    "  I cannot resolve domain names in addresses")
#                raise ImportError("no module named DNS")
#
#    def validate_python(self, value, state):
#        if not value:
#            raise Invalid(self.message('empty', state), value, state)
#        value = value.strip()
#        splitted = value.split('@', 1)
#        try:
#            username, domain=splitted
#        except ValueError:
#            raise Invalid(self.message('noAt', state), value, state)
#        if not self.usernameRE.search(username):
#            raise Invalid(
#                self.message('badUsername', state, username=username),
#                value, state)
#        if not self.domainRE.search(domain):
#            raise Invalid(
#                self.message('badDomain', state, domain=domain),
#                value, state)
#        if self.resolve_domain:
#            assert have_dns, "pyDNS should be available"
#            global socket
#            if socket is None:
#                import socket
#            try:
#                answers = DNS.DnsRequest(domain, qtype='a',
#                    timeout=self.resolve_timeout).req().answers
#                if answers:
#                    answers = DNS.DnsRequest(domain, qtype='mx',
#                        timeout=self.resolve_timeout).req().answers
#            except (socket.error, DNS.DNSError), e:
#                raise Invalid(
#                    self.message('socketError', state, error=e),
#                    value, state)
#            if not answers:
#                raise Invalid(
#                    self.message('domainDoesNotExist', state, domain=domain),
#                    value, state)
#
#    def _to_python(self, value, state):
#        return value.strip()
#
#
#class URL(FancyValidator):
#    """
#    Validate a URL, either http://... or https://.  If check_exists
#    is true, then we'll actually make a request for the page.
#
#    If add_http is true, then if no scheme is present we'll add
#    http://
#
#    ::
#
#        >>> u = URL(add_http=True)
#        >>> u.to_python('foo.com')
#        'http://foo.com'
#        >>> u.to_python('http://hahaha.ha/bar.html')
#        'http://hahaha.ha/bar.html'
#        >>> u.to_python('http://xn--m7r7ml7t24h.com')
#        'http://xn--m7r7ml7t24h.com'
#        >>> u.to_python('http://foo.com/test?bar=baz&fleem=morx')
#        'http://foo.com/test?bar=baz&fleem=morx'
#        >>> u.to_python('http://foo.com/login?came_from=http%3A%2F%2Ffoo.com%2Ftest')
#        'http://foo.com/login?came_from=http%3A%2F%2Ffoo.com%2Ftest'
#        >>> u.to_python('http://foo.com:8000/test.html')
#        'http://foo.com:8000/test.html'
#        >>> u.to_python('http://foo.com/something\\nelse')
#        Traceback (most recent call last):
#            ...
#        Invalid: That is not a valid URL
#        >>> u.to_python('https://test.com')
#        'https://test.com'
#        >>> u.to_python('http://test')
#        Traceback (most recent call last):
#            ...
#        Invalid: You must provide a full domain name (like test.com)
#        >>> u.to_python('http://test..com')
#        Traceback (most recent call last):
#            ...
#        Invalid: That is not a valid URL
#        >>> u = URL(add_http=False, check_exists=True)
#        >>> u.to_python('http://google.com')
#        'http://google.com'
#        >>> u.to_python('google.com')
#        Traceback (most recent call last):
#            ...
#        Invalid: You must start your URL with http://, https://, etc
#        >>> u.to_python('http://formencode.org/doesnotexist.html')
#        Traceback (most recent call last):
#            ...
#        Invalid: The server responded that the page could not be found
#        >>> u.to_python('http://this.domain.does.not.exist.example.org/test.html')
#        ... # doctest: +ELLIPSIS
#        Traceback (most recent call last):
#            ...
#        Invalid: An error occured when trying to connect to the server: ...
#
#    If you want to allow addresses without a TLD (e.g., ``localhost``) you can do::
#
#        >>> URL(require_tld=False).to_python('http://localhost')
#        'http://localhost'
#
#    """
#
#    check_exists = False
#    add_http = True
#    require_tld = True
#
#    url_re = re.compile(r'''
#        ^(http|https)://
#        (?:[%:\w]*@)?                           # authenticator
#        (?P<domain>[a-z0-9][a-z0-9\-]{,62}\.)*  # (sub)domain - alpha followed by 62max chars (63 total)
#        (?P<tld>[a-z]{2,})                      # TLD
#        (?::[0-9]+)?                            # port
#
#        # files/delims/etc
#        (?P<path>/[a-z0-9\-\._~:/\?#\[\]@!%\$&\'\(\)\*\+,;=]*)?
#        $
#    ''', re.I | re.VERBOSE)
#
#    scheme_re = re.compile(r'^[a-zA-Z]+:')
#
#    messages = dict(
#        noScheme=_('You must start your URL with http://, https://, etc'),
#        badURL=_('That is not a valid URL'),
#        httpError=_('An error occurred when trying to access the URL:'
#            ' %(error)s'),
#        socketError=_('An error occured when trying to connect to the server:'
#            ' %(error)s'),
#        notFound=_('The server responded that the page could not be found'),
#        status=_('The server responded with a bad status code (%(status)s)'),
#        noTLD=_('You must provide a full domain name (like %(domain)s.com)'))
#
#    def _to_python(self, value, state):
#        value = value.strip()
#        if self.add_http:
#            if not self.scheme_re.search(value):
#                value = 'http://' + value
#        match = self.scheme_re.search(value)
#        if not match:
#            raise Invalid(self.message('noScheme', state), value, state)
#        value = match.group(0).lower() + value[len(match.group(0)):]
#        match = self.url_re.search(value)
#        if not match:
#            raise Invalid(self.message('badURL', state), value, state)
#        if self.require_tld and not match.group('domain'):
#            raise Invalid(
#                self.message('noTLD', state, domain=match.group('tld')),
#                value, state)
#        if self.check_exists and (
#                value.startswith('http://') or value.startswith('https://')):
#            self._check_url_exists(value, state)
#        return value
#
#    def _check_url_exists(self, url, state):
#        global httplib, urlparse, socket
#        if httplib is None:
#            import httplib
#        if urlparse is None:
#            import urlparse
#        if socket is None:
#            import socket
#        scheme, netloc, path, params, query, fragment = urlparse.urlparse(
#            url, 'http')
#        if scheme == 'http':
#            ConnClass = httplib.HTTPConnection
#        else:
#            ConnClass = httplib.HTTPSConnection
#        try:
#            conn = ConnClass(netloc)
#            if params:
#                path += ';' + params
#            if query:
#                path += '?' + query
#            conn.request('HEAD', path)
#            res = conn.getresponse()
#        except httplib.HTTPException, e:
#            raise Invalid(
#                self.message('httpError', state, error=e), state, url)
#        except socket.error, e:
#            raise Invalid(
#                self.message('socketError', state, error=e), state, url)
#        else:
#            if res.status == 404:
#                raise Invalid(
#                    self.message('notFound', state), state, url)
#            if not 200 <= res.status < 500:
#                raise Invalid(
#                    self.message('status', state, status=res.status),
#                    state, url)
#
#
#class XRI(FancyValidator):
#    r"""
#    Validator for XRIs.
#
#    It supports both i-names and i-numbers, of the first version of the XRI
#    standard.
#
#    ::
#
#        >>> inames = XRI(xri_type="i-name")
#        >>> inames.to_python("   =John.Smith ")
#        '=John.Smith'
#        >>> inames.to_python("@Free.Software.Foundation")
#        '@Free.Software.Foundation'
#        >>> inames.to_python("Python.Software.Foundation")
#        Traceback (most recent call last):
#            ...
#        Invalid: The type of i-name is not defined; it may be either individual or organizational
#        >>> inames.to_python("http://example.org")
#        Traceback (most recent call last):
#            ...
#        Invalid: The type of i-name is not defined; it may be either individual or organizational
#        >>> inames.to_python("=!2C43.1A9F.B6F6.E8E6")
#        Traceback (most recent call last):
#            ...
#        Invalid: "!2C43.1A9F.B6F6.E8E6" is an invalid i-name
#        >>> iname_with_schema = XRI(True, xri_type="i-name")
#        >>> iname_with_schema.to_python("=Richard.Stallman")
#        'xri://=Richard.Stallman'
#        >>> inames.to_python("=John Smith")
#        Traceback (most recent call last):
#            ...
#        Invalid: "John Smith" is an invalid i-name
#        >>> inumbers = XRI(xri_type="i-number")
#        >>> inumbers.to_python("!!1000!de21.4536.2cb2.8074")
#        '!!1000!de21.4536.2cb2.8074'
#        >>> inumbers.to_python("@!1000.9554.fabd.129c!2847.df3c")
#        '@!1000.9554.fabd.129c!2847.df3c'
#
#    """
#
#    iname_valid_pattern = re.compile(r"""
#    ^
#    [\w]+                  # A global alphanumeric i-name
#    (\.[\w]+)*             # An i-name with dots
#    (\*[\w]+(\.[\w]+)*)*   # A community i-name
#    $
#    """, re.VERBOSE|re.UNICODE)
#
#
#    iname_invalid_start = re.compile(r"^[\d\.-]", re.UNICODE)
#    """@cvar: These characters must not be at the beggining of the i-name"""
#
#    inumber_pattern = re.compile(r"""
#    ^
#    (
#    [=@]!       # It's a personal or organization i-number
#    |
#    !!          # It's a network i-number
#    )
#    [\dA-F]{1,4}(\.[\dA-F]{1,4}){0,3}       # A global i-number
#    (![\dA-F]{1,4}(\.[\dA-F]{1,4}){0,3})*   # Zero or more sub i-numbers
#    $
#    """, re.VERBOSE|re.IGNORECASE)
#
#    messages = dict(
#        noType=_('The type of i-name is not defined;'
#            ' it may be either individual or organizational'),
#        repeatedChar=_('Dots and dashes may not be repeated consecutively'),
#        badIname=_('"%(iname)s" is an invalid i-name'),
#        badInameStart=_('i-names may not start with numbers'
#            ' nor punctuation marks'),
#        badInumber=_('"%(inumber)s" is an invalid i-number'),
#        badType=_('The XRI must be a string (not a %(type)s: %(value)r)'),
#        badXri=_('"%(xri_type)s" is not a valid type of XRI'))
#
#    def __init__(self, add_xri=False, xri_type="i-name", **kwargs):
#        """Create an XRI validator.
#
#        @param add_xri: Should the schema be added if not present?
#            Officially it's optional.
#        @type add_xri: C{bool}
#        @param xri_type: What type of XRI should be validated?
#            Possible values: C{i-name} or C{i-number}.
#        @type xri_type: C{str}
#
#        """
#        self.add_xri = add_xri
#        assert xri_type in ('i-name', 'i-number'), (
#            'xri_type must be "i-name" or "i-number"')
#        self.xri_type = xri_type
#        super(XRI, self).__init__(**kwargs)
#
#    def _to_python(self, value, state):
#        """Prepend the 'xri://' schema if needed and remove trailing spaces"""
#        value = value.strip()
#        if self.add_xri and not value.startswith('xri://'):
#            value = 'xri://' + value
#        return value
#
#    def validate_python(self, value, state=None):
#        """Validate an XRI
#
#        @raise Invalid: If at least one of the following conditions in met:
#            - C{value} is not a string.
#            - The XRI is not a personal, organizational or network one.
#            - The relevant validator (i-name or i-number) considers the XRI
#                is not valid.
#
#        """
#        if not isinstance(value, basestring):
#            raise Invalid(
#                self.message('badType', state,
#                    type=str(type(value)), value=value), value, state)
#
#        # Let's remove the schema, if any
#        if value.startswith('xri://'):
#            value = value[6:]
#
#        if not value[0] in ('@', '=') and not (
#                self.xri_type == 'i-number' and value[0] == '!'):
#            raise Invalid(self.message('noType', state), value, state)
#
#        if self.xri_type == 'i-name':
#            self._validate_iname(value, state)
#        else:
#            self._validate_inumber(value, state)
#
#    def _validate_iname(self, iname, state):
#        """Validate an i-name"""
#        # The type is not required here:
#        iname = iname[1:]
#        if '..' in iname or '--' in iname:
#            raise Invalid(self.message('repeatedChar', state), iname, state)
#        if self.iname_invalid_start.match(iname):
#            raise Invalid(self.message('badInameStart', state), iname, state)
#        if not self.iname_valid_pattern.match(iname) or '_' in iname:
#            raise Invalid(
#                self.message('badIname', state, iname=iname), iname, state)
#
#    def _validate_inumber(self, inumber, state):
#        """Validate an i-number"""
#        if not self.__class__.inumber_pattern.match(inumber):
#            raise Invalid(
#                self.message('badInumber', state,
#                    inumber=inumber, value=inumber), inumber, state)
#
#
#class OpenId(FancyValidator):
#    r"""
#    OpenId validator.
#
#    ::
#        >>> v = OpenId(add_schema=True)
#        >>> v.to_python(' example.net ')
#        'http://example.net'
#        >>> v.to_python('@TurboGears')
#        'xri://@TurboGears'
#        >>> w = OpenId(add_schema=False)
#        >>> w.to_python(' example.net ')
#        Traceback (most recent call last):
#        ...
#        Invalid: "example.net" is not a valid OpenId (it is neither an URL nor an XRI)
#        >>> w.to_python('!!1000')
#        '!!1000'
#        >>> w.to_python('look@me.com')
#        Traceback (most recent call last):
#        ...
#        Invalid: "look@me.com" is not a valid OpenId (it is neither an URL nor an XRI)
#
#    """
#
#    messages = dict(
#        badId=_('"%(id)s" is not a valid OpenId'
#            ' (it is neither an URL nor an XRI)'))
#
#    def __init__(self, add_schema=False, **kwargs):
#        """Create an OpenId validator.
#
#        @param add_schema: Should the schema be added if not present?
#        @type add_schema: C{bool}
#
#        """
#        self.url_validator = URL(add_http=add_schema)
#        self.iname_validator = XRI(add_schema, xri_type="i-name")
#        self.inumber_validator = XRI(add_schema, xri_type="i-number")
#
#    def _to_python(self, value, state):
#        value = value.strip()
#        try:
#            return self.url_validator.to_python(value, state)
#        except Invalid:
#            try:
#                return self.iname_validator.to_python(value, state)
#            except Invalid:
#                try:
#                    return self.inumber_validator.to_python(value, state)
#                except Invalid:
#                    pass
#        # It's not an OpenId!
#        raise Invalid(self.message('badId', state, id=value), value, state)
#
#    def validate_python(self, value, state):
#        self._to_python(value, state)
#
#
#def StateProvince(*kw, **kwargs):
#    warnings.warn("please use formencode.national.USStateProvince",
#        DeprecationWarning, stacklevel=2)
#    from formencode.national import USStateProvince
#    return USStateProvince(*kw, **kwargs)
#
#
#def PhoneNumber(*kw, **kwargs):
#    warnings.warn("please use formencode.national.USPhoneNumber",
#        DeprecationWarning, stacklevel=2)
#    from formencode.national import USPhoneNumber
#    return USPhoneNumber(*kw, **kwargs)
#
#
#def IPhoneNumberValidator(*kw, **kwargs):
#    warnings.warn("please use formencode.national.InternationalPhoneNumber",
#        DeprecationWarning, stacklevel=2)
#    from formencode.national import InternationalPhoneNumber
#    return InternationalPhoneNumber(*kw, **kwargs)
#
#
#class FieldStorageUploadConverter(FancyValidator):
#    """
#    Handles cgi.FieldStorage instances that are file uploads.
#
#    This doesn't do any conversion, but it can detect empty upload
#    fields (which appear like normal fields, but have no filename when
#    no upload was given).
#    """
#    def _to_python(self, value, state=None):
#        if isinstance(value, cgi.FieldStorage):
#            if getattr(value, 'filename', None):
#                return value
#            raise Invalid('invalid', value, state)
#        else:
#            return value
#
#    def is_empty(self, value):
#        if isinstance(value, cgi.FieldStorage):
#            return not bool(getattr(value, 'filename', None))
#        return FancyValidator.is_empty(self, value)
#
#
#class FileUploadKeeper(FancyValidator):
#    """
#    Takes two inputs (a dictionary with keys ``static`` and
#    ``upload``) and converts them into one value on the Python side (a
#    dictionary with ``filename`` and ``content`` keys).  The upload
#    takes priority over the static value.  The filename may be None if
#    it can't be discovered.
#
#    Handles uploads of both text and ``cgi.FieldStorage`` upload
#    values.
#
#    This is basically for use when you have an upload field, and you
#    want to keep the upload around even if the rest of the form
#    submission fails.  When converting *back* to the form submission,
#    there may be extra values ``'original_filename'`` and
#    ``'original_content'``, which may want to use in your form to show
#    the user you still have their content around.
#
#    To use this, make sure you are using variabledecode, then use
#    something like::
#
#      <input type="file" name="myfield.upload">
#      <input type="hidden" name="myfield.static">
#
#    Then in your scheme::
#
#      class MyScheme(Scheme):
#          myfield = FileUploadKeeper()
#
#    Note that big file uploads mean big hidden fields, and lots of
#    bytes passed back and forth in the case of an error.
#    """
#
#    upload_key = 'upload'
#    static_key = 'static'
#
#    def _to_python(self, value, state):
#        upload = value.get(self.upload_key)
#        static = value.get(self.static_key, '').strip()
#        filename = content = None
#        if isinstance(upload, cgi.FieldStorage):
#            filename = upload.filename
#            content = upload.value
#        elif isinstance(upload, basestring) and upload:
#            filename = None
#            # @@: Should this encode upload if it is unicode?
#            content = upload
#        if not content and static:
#            filename, content = static.split(None, 1)
#            if filename == '-':
#                filename = ''
#            else:
#                filename = filename.decode('base64')
#            content = content.decode('base64')
#        return {'filename': filename, 'content': content}
#
#    def _from_python(self, value, state):
#        filename = value.get('filename', '')
#        content = value.get('content', '')
#        if filename or content:
#            result = self.pack_content(filename, content)
#            return {self.upload_key: '',
#                    self.static_key: result,
#                    'original_filename': filename,
#                    'original_content': content}
#        else:
#            return {self.upload_key: '',
#                    self.static_key: ''}
#
#    def pack_content(self, filename, content):
#        enc_filename = self.base64encode(filename) or '-'
#        enc_content = (content or '').encode('base64')
#        result = '%s %s' % (enc_filename, enc_content)
#        return result
#
#
#class DateConverter(FancyValidator):
#    """
#    Validates and converts a string date, like mm/yy, dd/mm/yy,
#    dd-mm-yy, etc.  Using ``month_style`` you can support
#    ``'mm/dd/yyyy'`` or ``'dd/mm/yyyy'``.  Only these two general
#    styles are supported.
#
#    Accepts English month names, also abbreviated.  Returns value as a
#    datetime object (you can get mx.DateTime objects if you use
#    ``datetime_module='mxDateTime'``).  Two year dates are assumed to
#    be within 1950-2020, with dates from 21-49 being ambiguous and
#    signaling an error.
#
#    Use accept_day=False if you just want a month/year (like for a
#    credit card expiration date).
#
#    ::
#
#        >>> d = DateConverter()
#        >>> d.to_python('12/3/09')
#        datetime.date(2009, 12, 3)
#        >>> d.to_python('12/3/2009')
#        datetime.date(2009, 12, 3)
#        >>> d.to_python('2/30/04')
#        Traceback (most recent call last):
#            ...
#        Invalid: That month only has 29 days
#        >>> d.to_python('13/2/05')
#        Traceback (most recent call last):
#            ...
#        Invalid: Please enter a month from 1 to 12
#        >>> d.to_python('1/1/200')
#        Traceback (most recent call last):
#            ...
#        Invalid: Please enter a four-digit year after 1899
#
#    If you change ``month_style`` you can get European-style dates::
#
#        >>> d = DateConverter(month_style='dd/mm/yyyy')
#        >>> date = d.to_python('12/3/09')
#        >>> date
#        datetime.date(2009, 3, 12)
#        >>> d.from_python(date)
#        '12/03/2009'
#    """
#    ## @@: accepts only US-style dates
#
#    accept_day = True
#    # also allowed: 'dd/mm/yyyy'
#    month_style = 'mm/dd/yyyy'
#    # Use 'datetime' to force the Python 2.3+ datetime module, or
#    # 'mxDateTime' to force the mxDateTime module (None means use
#    # datetime, or if not present mxDateTime)
#    datetime_module = None
#
#    _day_date_re = re.compile(r'^\s*(\d\d?)[\-\./\\](\d\d?|jan|january|feb|febuary|mar|march|apr|april|may|jun|june|jul|july|aug|august|sep|sept|september|oct|october|nov|november|dec|december)[\-\./\\](\d\d\d?\d?)\s*$', re.I)
#    _month_date_re = re.compile(r'^\s*(\d\d?|jan|january|feb|febuary|mar|march|apr|april|may|jun|june|jul|july|aug|august|sep|sept|september|oct|october|nov|november|dec|december)[\-\./\\](\d\d\d?\d?)\s*$', re.I)
#
#    _month_names = {
#        'jan': 1, 'january': 1,
#        'feb': 2, 'febuary': 2,
#        'mar': 3, 'march': 3,
#        'apr': 4, 'april': 4,
#        'may': 5,
#        'jun': 6, 'june': 6,
#        'jul': 7, 'july': 7,
#        'aug': 8, 'august': 8,
#        'sep': 9, 'sept': 9, 'september': 9,
#        'oct': 10, 'october': 10,
#        'nov': 11, 'november': 11,
#        'dec': 12, 'december': 12,
#        }
#
#    ## @@: Feb. should be leap-year aware (but mxDateTime does catch that)
#    _monthDays = {
#        1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31,
#        9: 30, 10: 31, 11: 30, 12: 31}
#
#    messages = dict(
#        badFormat=_('Please enter the date in the form %(format)s'),
#        monthRange=_('Please enter a month from 1 to 12'),
#        invalidDay=_('Please enter a valid day'),
#        dayRange=_('That month only has %(days)i days'),
#        invalidDate=_('That is not a valid day (%(exception)s)'),
#        unknownMonthName=_('Unknown month name: %(month)s'),
#        invalidYear=_('Please enter a number for the year'),
#        fourDigitYear=_('Please enter a four-digit year after 1899'),
#        wrongFormat=_('Please enter the date in the form %(format)s'))
#
#    def __init__(self, *args, **kw):
#        super(DateConverter, self).__init__(*args, **kw)
#        if not self.month_style in ('dd/mm/yyyy', 'mm/dd/yyyy'):
#            raise TypeError('Bad month_style: %r' % self.month_style)
#
#    def _to_python(self, value, state):
#        if self.accept_day:
#            return self.convert_day(value, state)
#        else:
#            return self.convert_month(value, state)
#
#    def convert_day(self, value, state):
#        self.assert_string(value, state)
#        match = self._day_date_re.search(value)
#        if not match:
#            raise Invalid(
#                self.message('badFormat', state,
#                    format=self.month_style), value, state)
#        day = int(match.group(1))
#        try:
#            month = int(match.group(2))
#        except (TypeError, ValueError):
#            month = self.make_month(match.group(2), state)
#        else:
#            if self.month_style == 'mm/dd/yyyy':
#                month, day = day, month
#        year = self.make_year(match.group(3), state)
#        if not 1 <= month <= 12:
#            raise Invalid(self.message('monthRange', state), value, state)
#        if day < 1:
#            raise Invalid(self.message('invalidDay', state), value, state)
#        if self._monthDays[month] < day:
#            raise Invalid(
#                self.message('dayRange', state,
#                    days=self._monthDays[month]), value, state)
#        dt_mod = import_datetime(self.datetime_module)
#        try:
#            return datetime_makedate(dt_mod, year, month, day)
#        except ValueError, v:
#            raise Invalid(
#                self.message('invalidDate', state,
#                    exception=str(v)), value, state)
#
#    def make_month(self, value, state):
#        try:
#            return int(value)
#        except ValueError:
#            value = value.lower().strip()
#            if value in self._month_names:
#                return self._month_names[value]
#            else:
#                raise Invalid(
#                    self.message('unknownMonthName', state,
#                        month=value), value, state)
#
#    def make_year(self, year, state):
#        try:
#            year = int(year)
#        except ValueError:
#            raise Invalid(self.message('invalidYear', state), year, state)
#        if year <= 20:
#            year += 2000
#        elif 50 <= year < 100:
#            year += 1900
#        if 20 < year < 50 or 99 < year < 1900:
#            raise Invalid(self.message('fourDigitYear', state), year, state)
#        return year
#
#    def convert_month(self, value, state):
#        match = self._month_date_re.search(value)
#        if not match:
#            raise Invalid(
#                self.message('wrongFormat', state,
#                    format='mm/yyyy'), value, state)
#        month = self.make_month(match.group(1), state)
#        year = self.make_year(match.group(2), state)
#        if not 1 <= month <= 12:
#            raise Invalid(self.message('monthRange', state), value, state)
#        dt_mod = import_datetime(self.datetime_module)
#        return datetime_makedate(dt_mod, year, month, 1)
#
#    def _from_python(self, value, state):
#        if self.if_empty is not NoDefault and not value:
#            return ''
#        if self.accept_day:
#            return self.unconvert_day(value, state)
#        else:
#            return self.unconvert_month(value, state)
#
#    def unconvert_day(self, value, state):
#        # @@ ib: double-check, improve
#        if self.month_style == 'mm/dd/yyyy':
#            return value.strftime('%m/%d/%Y')
#        else:
#            return value.strftime('%d/%m/%Y')
#
#    def unconvert_month(self, value, state):
#        # @@ ib: double-check, improve
#        return value.strftime('%m/%Y')
#
#
#class TimeConverter(FancyValidator):
#    """
#    Converts times in the format HH:MM:SSampm to (h, m, s).
#    Seconds are optional.
#
#    For ampm, set use_ampm = True.  For seconds, use_seconds = True.
#    Use 'optional' for either of these to make them optional.
#
#    Examples::
#
#        >>> tim = TimeConverter()
#        >>> tim.to_python('8:30')
#        (8, 30)
#        >>> tim.to_python('20:30')
#        (20, 30)
#        >>> tim.to_python('30:00')
#        Traceback (most recent call last):
#            ...
#        Invalid: You must enter an hour in the range 0-23
#        >>> tim.to_python('13:00pm')
#        Traceback (most recent call last):
#            ...
#        Invalid: You must enter an hour in the range 1-12
#        >>> tim.to_python('12:-1')
#        Traceback (most recent call last):
#            ...
#        Invalid: You must enter a minute in the range 0-59
#        >>> tim.to_python('12:02pm')
#        (12, 2)
#        >>> tim.to_python('12:02am')
#        (0, 2)
#        >>> tim.to_python('1:00PM')
#        (13, 0)
#        >>> tim.from_python((13, 0))
#        '13:00:00'
#        >>> tim2 = tim(use_ampm=True, use_seconds=False)
#        >>> tim2.from_python((13, 0))
#        '1:00pm'
#        >>> tim2.from_python((0, 0))
#        '12:00am'
#        >>> tim2.from_python((12, 0))
#        '12:00pm'
#
#    Examples with ``datetime.time``::
#
#        >>> v = TimeConverter(use_datetime=True)
#        >>> a = v.to_python('18:00')
#        >>> a
#        datetime.time(18, 0)
#        >>> b = v.to_python('30:00')
#        Traceback (most recent call last):
#            ...
#        Invalid: You must enter an hour in the range 0-23
#        >>> v2 = TimeConverter(prefer_ampm=True, use_datetime=True)
#        >>> v2.from_python(a)
#        '6:00:00pm'
#        >>> v3 = TimeConverter(prefer_ampm=True,
#        ...                    use_seconds=False, use_datetime=True)
#        >>> a = v3.to_python('18:00')
#        >>> a
#        datetime.time(18, 0)
#        >>> v3.from_python(a)
#        '6:00pm'
#        >>> a = v3.to_python('18:00:00')
#        Traceback (most recent call last):
#            ...
#        Invalid: You may not enter seconds
#    """
#
#    use_ampm = 'optional'
#    prefer_ampm = False
#    use_seconds = 'optional'
#    use_datetime = False
#    # This can be set to make it prefer mxDateTime:
#    datetime_module = None
#
#    messages = dict(
#        noAMPM=_('You must indicate AM or PM'),
#        tooManyColon=_('There are too many :\'s'),
#        noSeconds=_('You may not enter seconds'),
#        secondsRequired=_('You must enter seconds'),
#        minutesRequired=_('You must enter minutes (after a :)'),
#        badNumber=_('The %(part)s value you gave is not a number: %(number)r'),
#        badHour=_('You must enter an hour in the range %(range)s'),
#        badMinute=_('You must enter a minute in the range 0-59'),
#        badSecond=_('You must enter a second in the range 0-59'))
#
#    def _to_python(self, value, state):
#        result = self._to_python_tuple(value, state)
#        if self.use_datetime:
#            dt_mod = import_datetime(self.datetime_module)
#            time_class = datetime_time(dt_mod)
#            return time_class(*result)
#        else:
#            return result
#
#    def _to_python_tuple(self, value, state):
#        time = value.strip()
#        explicit_ampm = False
#        if self.use_ampm:
#            last_two = time[-2:].lower()
#            if last_two not in ('am', 'pm'):
#                if self.use_ampm != 'optional':
#                    raise Invalid(self.message('noAMPM', state), value, state)
#                else:
#                    offset = 0
#            else:
#                explicit_ampm = True
#                if last_two == 'pm':
#                    offset = 12
#                else:
#                    offset = 0
#                time = time[:-2]
#        else:
#            offset = 0
#        parts = time.split(':')
#        if len(parts) > 3:
#            raise Invalid(self.message('tooManyColon', state), value, state)
#        if len(parts) == 3 and not self.use_seconds:
#            raise Invalid(self.message('noSeconds', state), value, state)
#        if (len(parts) == 2
#                and self.use_seconds and self.use_seconds != 'optional'):
#            raise Invalid(self.message('secondsRequired', state), value, state)
#        if len(parts) == 1:
#            raise Invalid(self.message('minutesRequired', state), value, state)
#        try:
#            hour = int(parts[0])
#        except ValueError:
#            raise Invalid(
#                self.message('badNumber', state,
#                    number=parts[0], part='hour'), value, state)
#        if explicit_ampm:
#            if not 1 <= hour <= 12:
#                raise Invalid(
#                    self.message('badHour', state,
#                        number=hour, range='1-12'), value, state)
#            if hour == 12 and offset == 12:
#                # 12pm == 12
#                pass
#            elif hour == 12 and offset == 0:
#                # 12am == 0
#                hour = 0
#            else:
#                hour += offset
#        else:
#            if not 0 <= hour < 24:
#                raise Invalid(
#                    self.message('badHour', state,
#                        number=hour, range='0-23'), value, state)
#        try:
#            minute = int(parts[1])
#        except ValueError:
#            raise Invalid(
#                self.message('badNumber', state,
#                    number=parts[1], part='minute'), value, state)
#        if not 0 <= minute < 60:
#            raise Invalid(
#                self.message('badMinute', state, number=minute),
#                value, state)
#        if len(parts) == 3:
#            try:
#                second = int(parts[2])
#            except ValueError:
#                raise Invalid(
#                    self.message('badNumber', state,
#                        number=parts[2], part='second'), value, state)
#            if not 0 <= second < 60:
#                raise Invalid(
#                    self.message('badSecond', state, number=second),
#                    value, state)
#        else:
#            second = None
#        if second is None:
#            return (hour, minute)
#        else:
#            return (hour, minute, second)
#
#    def _from_python(self, value, state):
#        if isinstance(value, basestring):
#            return value
#        if hasattr(value, 'hour'):
#            hour, minute = value.hour, value.minute
#            second = value.second
#        elif len(value) == 3:
#            hour, minute, second = value
#        elif len(value) == 2:
#            hour, minute = value
#            second = 0
#        ampm = ''
#        if (self.use_ampm == 'optional' and self.prefer_ampm) or (
#                self.use_ampm and self.use_ampm != 'optional'):
#            ampm = 'am'
#            if hour > 12:
#                hour -= 12
#                ampm = 'pm'
#            elif hour == 12:
#                ampm = 'pm'
#            elif hour == 0:
#                hour = 12
#        if self.use_seconds:
#            return '%i:%02i:%02i%s' % (hour, minute, second, ampm)
#        else:
#            return '%i:%02i%s' % (hour, minute, ampm)
#
#
#def PostalCode(*kw, **kwargs):
#    warnings.warn("please use formencode.national.USPostalCode",
#        DeprecationWarning, stacklevel=2)
#    from formencode.national import USPostalCode
#    return USPostalCode(*kw, **kwargs)
#
#
#class StripField(FancyValidator):
#    """
#    Take a field from a dictionary, removing the key from the dictionary.
#
#    ``name`` is the key.  The field value and a new copy of the dictionary
#    with that field removed are returned.
#
#    >>> StripField('test').to_python({'a': 1, 'test': 2})
#    (2, {'a': 1})
#    >>> StripField('test').to_python({})
#    Traceback (most recent call last):
#        ...
#    Invalid: The name 'test' is missing
#
#    """
#
#    __unpackargs__ = ('name',)
#
#    messages = dict(
#        missing=_('The name %(name)s is missing'))
#
#    def _to_python(self, valueDict, state):
#        v = valueDict.copy()
#        try:
#            field = v.pop(self.name)
#        except KeyError:
#            raise Invalid(
#                self.message('missing', state, name=repr(self.name)),
#                valueDict, state)
#        return field, v
#
#    def is_empty(self, value):
#        # empty dictionaries don't really apply here
#        return False
#
#
#
#
#class SignedString(FancyValidator):
#    """
#    Encodes a string into a signed string, and base64 encodes both the
#    signature string and a random nonce.
#
#    It is up to you to provide a secret, and to keep the secret handy
#    and consistent.
#    """
#
#    messages = dict(
#        malformed=_('Value does not contain a signature'),
#        badsig=_('Signature is not correct'))
#
#    secret = None
#    nonce_length = 4
#
#    def _to_python(self, value, state):
#        global sha1
#        if not sha1:
#            try:
#                from hashlib import sha1
#            except ImportError: # Python < 2.5
#                from sha import sha as sha1
#        assert self.secret is not None, (
#            "You must give a secret")
#        parts = value.split(None, 1)
#        if not parts or len(parts) == 1:
#            raise Invalid(self.message('malformed', state), value, state)
#        sig, rest = parts
#        sig = sig.decode('base64')
#        rest = rest.decode('base64')
#        nonce = rest[:self.nonce_length]
#        rest = rest[self.nonce_length:]
#        expected = sha1(str(self.secret)+nonce+rest).digest()
#        if expected != sig:
#            raise Invalid(self.message('badsig', state), value, state)
#        return rest
#
#    def _from_python(self, value, state):
#        global sha1
#        if not sha1:
#            try:
#                from hashlib import sha1
#            except ImportError:
#                from sha import sha as sha1
#        nonce = self.make_nonce()
#        value = str(value)
#        digest = sha1(self.secret+nonce+value).digest()
#        return self.encode(digest)+' '+self.encode(nonce+value)
#
#    def encode(self, value):
#        return value.encode('base64').strip().replace('\n', '')
#
#    def make_nonce(self):
#        global random
#        if not random:
#            import random
#        return ''.join([
#            chr(random.randrange(256))
#            for i in range(self.nonce_length)])
#
#
#class IPAddress(FancyValidator):
#    """
#    Formencode validator to check whether a string is a correct IP address.
#
#    Examples::
#
#        >>> ip = IPAddress()
#        >>> ip.to_python('127.0.0.1')
#        '127.0.0.1'
#        >>> ip.to_python('299.0.0.1')
#        Traceback (most recent call last):
#            ...
#        Invalid: The octets must be within the range of 0-255 (not '299')
#        >>> ip.to_python('192.168.0.1/1')
#        Traceback (most recent call last):
#            ...
#        Invalid: Please enter a valid IP address (a.b.c.d)
#        >>> ip.to_python('asdf')
#        Traceback (most recent call last):
#            ...
#        Invalid: Please enter a valid IP address (a.b.c.d)
#    """
#
#    messages = dict(
#        badFormat=_('Please enter a valid IP address (a.b.c.d)'),
#        illegalOctets=_('The octets must be within the range of 0-255'
#            ' (not %(octet)r)'))
#
#    def validate_python(self, value, state):
#        try:
#            octets = value.split('.')
#            # Only 4 octets?
#            if len(octets) != 4:
#                raise Invalid(
#                    self.message('badFormat', state, value=value),
#                    value, state)
#            # Correct octets?
#            for octet in octets:
#                if not 0 <= int(octet) < 256:
#                    raise Invalid(
#                        self.message('illegalOctets', state, octet=octet),
#                        value, state)
#        # Splitting faild: wrong syntax
#        except ValueError:
#            raise Invalid(self.message('badFormat', state), value, state)
#
#
#
### DEBUG & TEST ###
#
#if __name__ == "__main__":
#	import doctest
#	doctest.testmod()
#
