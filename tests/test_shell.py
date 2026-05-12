import pytest

from yconf import loads, errors


def test_shell():
    m = loads('foo: !shell echo hello')
    assert m.foo == 'hello'

    with pytest.raises(errors.ExpectedTokenError) as e:
        loads('!shell')

    assert e.exconly() == \
        'yconf.errors.ExpectedTokenError: (stream):0:0: Expected ' \
        'VALUE, found: EOF `None`'
