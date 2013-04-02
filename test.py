import konval
from konval.meta.standard import IsName

schema = {u'name': IsName()}

result = konval.validate(schema, {u'name': 'Peter M. Elias'})

print result.is_valid() # True

result = konval.validate(schema, {u'name': 'Not a real name...4342398!!*#'})

print result.is_valid() # False
print result.get_errors()
