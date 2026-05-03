from yconf import parse


def test_parser():
    assert parse('foo: bar').foo == 'bar'
    assert parse('foo: 1').foo == 1
    assert parse('foo: [1, 2]').foo == [1, 2]
