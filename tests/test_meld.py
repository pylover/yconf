import pytest

from yconf import Meld


def test_meld_merge():
    m = Meld('foo: bar')
    m |= '''
       foo: qux
       bar: baz
       baz:
         a: 1
         b: 2
    '''

    assert m.foo == 'qux'
    assert m.bar == 'baz'
    assert m.baz.a == 1
    assert m.baz.b == 2
    assert isinstance(m.baz, Meld)


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
