from collections import OrderedDict

from yconf import dumps, loads


def test_dumps_meld():
    out = dumps({})
    assert out == ''

    d = OrderedDict(foo='bar', baz=3, qux=.73)
    assert d == loads(dumps(d))

    out = dumps(d)
    assert out == '\n'.join([
        'foo: bar',
        'baz: 3',
        'qux: 0.73',
        ''
    ])


    yml = '''
      foo: FOO
        bar:
          a: 1
          b: 2
        baz:
          - first
          - .73
    '''

    assert yml == dumps(loads(yml), indent=6)

    # out = dumps(m)


def test_dumps_list():
    out = dumps([1, 2])
    assert out == \
        '- 1\n' \
        '- 2\n'

    out = dumps([])
    assert out == ''
