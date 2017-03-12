import types
from collections import namedtuple


def freeze_data(obj, *, allow=frozenset()):
    """Convert 'obj' recursively to a read-only object but selectively
    allow functions, modules and other hashables, which may not be read-only.
    This means that recursively:
    - ints, floats, strings, bytes, None and bools are kept unchanged
    - lists are converted to tuples
    - dicts are converted to types.MappingProxyType
    - sets are converted to frozensets
    - modules (if allowed) will unchanged. If root object s a module, it will be converted to
      a namedtuple
    - classes and instances (if allowed) are converted to namedtuples
    - namedtuples are created anew and values recursively made read-only

    If 'obj' is a function, a ValueError is raised, as functions are not read-only
    (e.g. the function's .__globals__ will be accessible). However, functions are often useful
    to retain in the data structures, so if string 'functions' is found in 'allow',
    functions are *copied* to new functions. The user of the data structure *will* be
    allowed access to the original function's .__globals__ attributes etc., so keep this in mind.

    class objects are also not necessarily read-only and will by default raise ValueErrors.
    However, if a string 'classes' is in 'allow', the class objects will be converted to
    namedtuple instances.

    class instances (beside from built-in immutables like 9, "er", 9.7 etc.) will raise
    ValueError by default. If a string 'instances' is set in 'allow', instances will
    be converted to namedtuple instances.

    If other objects than lists, sets, instances etc mentioned above are found, a ValueError
    will be raised.

    Notice: The created read-only objects is not hashable if the original object contains dicts, as
    types.MappingProxyType is not hashable.

    """

    allowed_ = {'functions', 'modules', 'classes', 'instances'}
    if isinstance(allow, (str)):
        allow = frozenset((allow,))
    elif not isinstance(allow, (set, frozenset)):
        allow = frozenset(allow)
    if not allow <= allowed_:
        raise ValueError("'allow' must be in %r" % (allowed_))

    if isinstance(obj, types.ModuleType):
        return freeze_class_or_istance_or_module(obj, allow=allow)
    else:
        print(123)
        return freeze_data_inner(obj, allow=allow)


def freeze_data_inner(obj, *, allow=frozenset()):
    # check type and recursively return a new read-only object
    if isinstance(obj, (str, int, float, bytes, type(None), bool)):
        return obj
    elif isinstance(obj, tuple) and not type(obj) == tuple:  # assumed namedtuple
        return type(obj)(
            *(freeze_data_inner(i, allow=allow) for i in obj))
    elif isinstance(obj, (tuple, list)):
        return tuple(freeze_data_inner(i, allow=allow) for i in obj)
    elif isinstance(obj, (dict, types.MappingProxyType)):
        return types.MappingProxyType(
            {k: freeze_data_inner(v, allow=allow) for k, v in
             obj.items()})
    elif isinstance(obj, (set, frozenset)):
        return frozenset(
            freeze_data_inner(i, allow=allow) for i in obj)
    elif isinstance(obj, types.FunctionType):
        if 'functions' not in allow:
            raise ValueError(("Functions not allowed, %s used. "
                              "To allow functions, set allow = {'functions'}") % (
                                 obj,))
        func = copy_function(obj)
        for i in (j for j in dir(obj) if not j.startswith('__')):
            val = getattr(obj, i)
            setattr(func, i, freeze_data_inner(val, allow=allow))
        return func
    elif isinstance(obj, types.SimpleNamespace):
        return freeze_class_or_istance_or_module(obj, allow=allow)
    elif isinstance(obj, types.ModuleType):
        if 'modules' not in allow:
            raise ValueError(("Modules not allowed, %s used. "
                              "To allow functions, set allow = {'modules'}") % (
                                 obj,))
        return obj
    elif isinstance(obj, type):
        if 'classes' not in allow:
            raise ValueError(("classes not allowed, %s used. "
                              "To allow classes, set allow = {'classes'}") % (
                                 obj,))
        return freeze_class_or_istance_or_module(obj, allow=allow)
    elif isinstance(type(obj), type):
        if 'instances' not in allow:
            raise ValueError(("class instances not allowed, %s used. "
                              "To allow class instances, set allow = {'instances'}") % (
                                 obj,))
        return freeze_class_or_istance_or_module(obj, allow=allow)
    raise ValueError(obj)


def freeze_class_or_istance_or_module(obj, allow=frozenset()):
    """Convert a class, instanced or module to a collections.namedtuple.

    Note: collections.namedtuple does not allow single underscore in attributes"""
    obj_name = obj.__name__ if hasattr(obj, '__name__') else obj.__class__.__name__
    obj_name = obj_name.replace('.', '_')
    obj_tuple = namedtuple(obj_name, [i for i in dir(obj) if not i.startswith('_')])
    return obj_tuple(
        **{i: freeze_data(getattr(obj, i), allow=allow) for
           i in dir(obj) if not i.startswith('_')})


def copy_function(obj):
    """Copy function 'obj' into new new function.

    Note: functions leak data, so a function copy is only a partial copy.
    In particular, avoid resetting dunder-attributes, e.g. don't reset .__kwdefaults__ """
    import functools

    func = types.FunctionType(obj.__code__, obj.__globals__, name=obj.__name__,
                              argdefs=obj.__defaults__,
                              closure=obj.__closure__)
    func = functools.update_wrapper(func, obj)
    func.__kwdefaults__ = obj.__kwdefaults__

    return func
