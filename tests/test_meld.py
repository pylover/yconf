import pytest

from yconf import Meld


def test_meld():
    m = Meld()

    m.foo = 'bar'
    assert m.foo == 'bar'
    del m.foo

    with pytest.raises(AttributeError):
        m.foo

    with pytest.raises(AttributeError):
        del m.foo
