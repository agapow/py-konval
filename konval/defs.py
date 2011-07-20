"""
Various module-wide constants.

"""

__docformat__ = "restructuredtext en"


### IMPORTS

### CONSTANTS & DEFINES

TRUE_STRS = [
	'TRUE',
	'T',
	'ON',
	'YES',
	'Y',
	'+',
]

FALSE_STRS = [
	'FALSE',
	'F',
	'OFF',
	'NO',
	'N',
	'-',
]

TRUE_FALSE_DICT = {}
for v in TRUE_STRS:
	TRUE_FALSE_DICT[v] = True
for v in FALSE_STRS:
	TRUE_FALSE_DICT[v] = False

CANON_SPACE = re.compile (r'[\-_\s]+')


### IMPLEMENTATION ###

### END #######################################################################
