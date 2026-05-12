import os

import pytest

from yconf import Meld


def test_meld_exportfile(tmpdir):
    filename = os.path.join(tmpdir, 'foo.yml')
    m = Meld('''
      foo: bar
    ''')

    m >>= filename
    with open(filename) as f:
        assert f.read() == 'foo: bar\n'


def test_meld_mergefile(mktmpfile):
    file = mktmpfile(content='''
       foo: BAR
       bar:
         baz:
           a: 1
           b: 2
    ''')

    m = Meld('''
      foo: bar
      bar:
        qux: 73
    ''')

    m <<= file
    assert m.foo == 'BAR'
    assert m.bar.qux == 73
    assert m.bar.baz.a == 1
    assert m.bar.baz.b == 2


def test_meld_merge():
    m = Meld('''
      foo: bar
      bar:
        qux: 73
    ''')

    m |= '''
       foo: BAR
       bar:
         baz:
           a: 1
           b: 2
    '''

    assert m.foo == 'BAR'
    assert m.bar.qux == 73
    assert m.bar.baz.a == 1
    assert m.bar.baz.b == 2
    assert isinstance(m.bar, Meld)
    assert isinstance(m.bar.baz, Meld)

    with pytest.raises(TypeError):
        m |= 73

    m = Meld('bar: baz', root='foo')
    assert m.foo.bar == 'baz'


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
