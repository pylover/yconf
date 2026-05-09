import os
import pytest

from yconf import loads, errors


def test_env(mktmpfile):
    m = loads('foo: !env: USER')
    assert m.foo == os.environ['USER']

    with pytest.raises(errors.ExpectedTokenError) as e:
        loads('!env:')

    assert e.exconly() == \
        'yconf.errors.ExpectedTokenError: (stream):0:0: Expected ' \
        'environment variable: tag `env`'
