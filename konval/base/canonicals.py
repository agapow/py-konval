import re

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

TRUE_FALSE_DICT = dict([(k, True) for k in TRUE_STRS] + [(k, False) for k in FALSE_STRS])

CANON_SPACE_RE = re.compile (r'[\-_\s]+')

SLUG_RE = re.compile(r'\W+')

PUNCTUATION_RE = re.compile(r'[!\@#\$\%\^\&\*\(\)\.,\/\\\?\-_\`\~<>;:'"\[\]\{\}\+\= \|]+')