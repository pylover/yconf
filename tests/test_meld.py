import pytest

from yconf import Meld


# def test_meld_merge():
#


def test_meld_constructor():
    m = Meld('foo: bar')
    assert m.foo == 'bar'

    m = Meld(dict(foo='bar'))
    assert m.foo == 'bar'


def test_meld_attributes():
    m = Meld()

    m.foo = 'bar'
    assert m.foo == 'bar'
    del m.foo

    with pytest.raises(AttributeError):
        m.foo

    with pytest.raises(AttributeError):
        del m.foo
