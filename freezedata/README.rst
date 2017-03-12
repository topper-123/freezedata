Recursively convert ``list`` to ``tuple``, ``set`` to ``frozenset``,
``dict`` to ``mappingproxy`` etc.

Example usage:

.. code-block:: python

    import freezedata

    data = [{'a': [1,2,3], 'b': {1,2,3}}, {1:1, 2:2, 3:3}]
    frozendata = freezedata.freeze_data(data)
    print(frozendata)
    >> (mappingproxy({'a': (1, 2, 3), 'b': frozenset({1, 2, 3})}),
 mappingproxy({1: 1, 2: 2, 3: 3}))

This is a read-only data structure, that is; there is no direct way to alter this
data structure from within ``frozendata`` itself (without using some special modules (``gc``,
``inspect``)).

For example:

.. code-block:: python

    frozendata[0]['a'][0] = 4
    >> TypeError: 'tuple' object does not support item assignment
    del frozendata[1][1]
    >> TypeError: 'mappingproxy' object does not support item deletion

*Notice*: Since a ``mappingproxy`` is not hashable, frozen data
structures containing ``mappingproxy`` (i.e. based on ``dict``) will not be
hashable either:

.. code-block:: python

    hash(frozendata)
    >> TypeError: unhashable type: 'mappingproxy'

On the other hand, if the frozen data structure contains only hashable elements, the whole
structure will be hashable (and immutable) as well:

.. code-block:: python

    frozendata = freezedata.freeze_data([[1,2,3], {4,5,6}])
    print(frozendata)
    >> ((1, 2, 3), frozenset({4, 5, 6}))
    hash(frozendata)
    >> -11948691520864899

Relaxing requirements (accepting functions, modules, classes and instances):
----------------------------------------------------------------------------

Functions, modules, (user-created) classes and instances are mutable in Python, and therefore
neither immutable or read-only. By default, using these will result in errors, but setting
parameter ``allow`` as one, several or all of ``functions``, ``modules`` , ``classes``
and ``instances``, these can be used in the new new data structure.

**Functions** are mutable in Python, but sometimes you still want a function in a
new data structure that won't affect the parent data structure / parent function.
By setting ``allow='functions'`` or ``allow=['functions']``, the new data structure will
contain  a *copy* of the included functions:

.. code-block:: python

    def func(n):
        return n*2
    func.a = 'a'
    data = [func]
    frozendata = freezedata.freeze_data(data, allow='functions')
    data[0] == frozendata[0]
    >> False
    frozendata[0].a = 'b'
    print(data[0].a, frozendata[0].a)
    >> a b

**modules** will be converted to a ``namedtuple``, if you're freezing a module.
If a module is in the data structure, but it's not top level, an error will by default be raised.
If ``allow={'modules'}`` is set, non-top-level modules will be allowed and kept *unchanged*.

**classes and class instances** may be converted into ``namedtuple`` and used in the
frozen data structure by setting ``allow={'classes', 'instances}`` or only one, e.g.
``allow={'classes'}``, as needed. By converting to ``namedtuple``, information may be lost, as
attributes with leading underscores will be ignored:

.. code-block:: python

    class Test:
        a = 1
        def __init__(self, a):
            self.a = a
    test = Test(2)
    frozendata = freezedata.freeze_data([Test, test], allow={'classes', 'instances'})
    print(frozendata)
    >> (Test(a=1), Test(a=2))
    print(type(frozendata[0]), type(frozendata[1]))
    >> <class 'freezedata.freezedata.Test'> <class 'freezedata.freezedata.Test'>  # two namedtuples

