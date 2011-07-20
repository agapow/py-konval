"""
Various module-wide constants.

"""

__docformat__ = "restructuredtext en"


### IMPORTS

import re


### CONSTANTS & DEFINES

TRUE_STRS = [
	'TRUE',
	'T',
	'ON',
	'YES',
	'Y',
	'+',
	'1',
	1,
]

FALSE_STRS = [
	'FALSE',
	'F',
	'OFF',
	'NO',
	'N',
	'-',
	'0',
	0,
]

TRUE_FALSE_DICT = {}
for v in TRUE_STRS:
	TRUE_FALSE_DICT[v] = True
for v in FALSE_STRS:
	TRUE_FALSE_DICT[v] = False

CANON_SPACE = re.compile (r'[\-_\s]+')


### IMPLEMENTATION ###

### END #######################################################################
