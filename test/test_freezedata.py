from freezedata import freeze_data
import types
from collections import namedtuple

import pytest

def test_freeze_data_lists_sets_dicts():
    data = [1, [1, {1, 2, 3}], {1: 2, 2: [1, 2]},
            types.MappingProxyType({1: 2, 2: (1, 2)})]
    control_data = (1, (1, frozenset((1, 2, 3))), types.MappingProxyType({1: 2, 2: (1, 2)}),
                    types.MappingProxyType({1: 2, 2: (1, 2)}))

    assert freeze_data(data) == control_data


def test_freeze_data_namedtuples_simplenamespaces():
    TestNamedTuple = namedtuple('TestNamedTuple', list('abc'))
    data = types.SimpleNamespace(a=1, b=TestNamedTuple(a=1, b=2, c=3))

    control_tuple = namedtuple('SimpleNamespace', list('ab'))
    control_data = control_tuple(a=1, b=TestNamedTuple(a=1, b=2, c=3))

    assert freeze_data(data) == control_data


def test_freeze_data_functions():

    def test_func(n):
        return n*2
    data = [test_func]
    frozendata = freeze_data(data, allow='functions')

    with pytest.raises(ValueError):
        frozendata2 = freeze_data(data)

    from freezedata.freezedata import copy_function
    control_data = (copy_function(test_func),)

    assert frozendata[0](2) == test_func(2)

    assert type(frozendata) == tuple

    assert type(frozendata[0]) == types.FunctionType

    assert frozendata[0] != control_data[0]


def test_freeze_data_class_instance():
    from . import data_module

    with pytest.raises(ValueError):
        frozendata2 = freeze_data(data_module)
    frozendata = freeze_data(data_module, allow={'classes', 'instances'})