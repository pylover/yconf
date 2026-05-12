import os
import pytest

from snam import loads, errors


def test_env(mktmpfile):
    m = loads('foo: !env USER')
    assert m.foo == os.environ['USER']

    with pytest.raises(errors.ExpectedTokenError) as e:
        loads('!env')

    assert e.exconly() == \
        'snam.errors.ExpectedTokenError: (stream):0:0: Expected ' \
        'VALUE, found: EOF `None`'
