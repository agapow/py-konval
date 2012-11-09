#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Internal implementation utilities and details.

This module contains various odds and ends to make development easier. None of
code within should be relied upon as it is subject to change at a whim.
"""

__docformat__ = 'restructuredtext en'


### IMPORTS ###

import types

import defs

__all__ = [
	'make_list',
	'make_canonical',
]


### CONSTANTS & DEFINES ###

### IMPLEMENTATION ###	

def make_list (x):
	"""
	If this isn't a list, make it one.
	
	:Parameters:
		x : list, tuple, other
			a sequence, or a single element to be placed in a sequence
			
	:Returns:
		Either the original a parameter if a sequence, or the parameter placed in
		a list.
	
	Syntactic sugar for allowing method calls to be single elements or lists of
	elements.
	
	For example::
	
		>>> make_list (1)
		[1]
		>>> make_list ('1')
		['1']
		>>> make_list ([1, 2])
		[1, 2]
		>>> make_list ((1, 2))
		(1, 2)
		
	"""
	# TODO: should be a more general way of doing this
	if (type (x) not in (types.ListType, types.TupleType)):
		x = [x]
	return x


def make_canonical (value):
	"""
	Clean-up minor string variants to a single form.
	
	:Parameters:
		value : string
			the string to be sanitized
			
	:Returns:
		The parameter cleaned up
	
	This is syntactic sugar for mapping minor string variants (mostly
	whitespace and punctuation flourishes, as you expect in user input or free
	text) to a single canonical from. This consists of trimming flanking spaces,
	making the string uppercase, and collapsing all internal spaces / hyphens /
	underscores to a single underscore.
	
	For example::
	
		>>> make_canonical ('abc')
		'ABC'
		>>> make_canonical ('  CD-EF  ')
		'CD_EF'
		>>> make_canonical ('H-IJ- _K')
		'H_IJ_K'
		
	"""
	# TODO: all internal punctuation
	# TODO: trim flanking punctuation
	new_val = value.strip().upper()
	new_val = defs.CANON_SPACE_RE.sub ('_', new_val)
	return new_val