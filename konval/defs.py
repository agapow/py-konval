"""
Various module-wide constants.

"""

__docformat__ = "restructuredtext en"

import re

__all__ = [
	'TRUE_FALSE_DICT',
	'CANON_SPACE_RE',
]


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

CANON_SPACE_RE = re.compile (r'[\-_\s]+')