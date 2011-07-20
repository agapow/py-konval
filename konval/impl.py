#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Internal implementation utilities and details.

This module contains various odds and ends to make development easier. None of
code within should be relied upon as it is subject to change at a whim.
"""

__docformat__ = 'restructuredtext en'


### IMPORTS ###

import defs
import impl

__all__ = [
	'make_list',
]


### CONSTANTS & DEFINES ###

### IMPLEMENTATION ###	

def make_list (x):
	"""
	If this isn't a list, make it one.
	
	Syntactic sugar for allowing method calls to be single elements or lists of
	elements.
	"""
	# TODO: should be a more general way of doing this
	if (type (x) in (type.ListType, type.TupleType)):
		x = [x]
	return x


def make_canonical (value):
	new_val = value.strip().upper()
	new_val = defs.CANON_SPACE_RE.sub ('_', value)
	return new_val


### END #######################################################################
