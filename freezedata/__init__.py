import os
from .freezedata import freeze_data

DIR = os.path.dirname(__file__)
README = os.path.join(DIR, 'README.rst')

__doc__ = """
Recursively convert lists to tuples, sets to frozensets, dicts to mappingproxy etc.

Example usage::

   import freezedata

   data = {'a': [1,2,3], 'b': {1,2,3}, 'c': {1:1, 2:2, 3:3}}
   frozendata = freezedata.freeze_data(data)
   print(frozendata)
   >> {'a': (1, 2, 3), 'b': frozenset({1, 2, 3}), 'c': mappingproxy({1: 1, 2: 2, 3: 3})}

This is an immutable data structure, that is; there is no direct way to alter this
data structure (without using some special modules(gc, inspect)). For example::

   frozendata[c'][4] = 4
   >> TypeError: 'mappingproxy' object does not support item assignment
   del frozendata['b']
   >> TypeError: 'mappingproxy' object does not support item deletion

**Notice**: Since a `mappingproxy` is not hashable, frozen data
structures containing `mappingproxy`s (i.e. based on `dict`s) will not be
hashable either::

   hash(frozendata)
   >> TypeError: unhashable type: 'mappingproxy'
"""

del os, DIR, README
del freezedata
