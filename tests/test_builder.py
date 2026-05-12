import os
from collections import OrderedDict

from snam import dump, dumps, loads


def test_dump(tmpdir):
    yml = '''\
      foo: !env USER
    '''
    filename = os.path.join(tmpdir, 'foo.yml')
    with open(filename, 'w') as f:
        dump(loads(yml), f)

    with open(filename) as f:
        assert f.read() == f'foo: {os.environ["USER"]}\n'


def test_dumps_tags():
    yml = '''\
      foo: !env USER
    '''
    assert dumps(loads(yml), indent=6) == f'''\
      foo: {os.environ['USER']}\n'''


def test_dumps_list():
    out = dumps([])
    assert out == ''

    yml = '''\
      - foo
      -
        b: 2
        c: 3\n'''
    assert yml == dumps(loads(yml), indent=6)

    out = dumps([1, 2])
    assert out == \
        '- 1\n' \
        '- 2\n'

    out = dumps([])
    assert out == ''


def test_dumps_meld():
    out = dumps({})
    assert out == ''

    yml = '''\
      foo: FOO
      bar:
        a: 1
        b:
          b1: B1
          b2: B2\n'''

    assert yml == dumps(loads(yml), indent=6)

    d = OrderedDict(foo='bar', baz=3, qux=.73, quux=True)
    out = dumps(d)
    assert out == '\n'.join([
        'foo: bar',
        'baz: 3',
        'qux: 0.73',
        'quux: True',
        ''
    ])


def test_dumps_literal():
    out = dumps('foo')
    assert out == 'foo\n'
