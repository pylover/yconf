import pytest

from yconf import loads, errors


def test_include_error(mktmpfile):
    dictfile = mktmpfile(name='qux.yml', content='''
      foo: bar
    ''')
    listfile = mktmpfile(name='qux.yml', content='''
      - foo
      - bar
    ''')

    # test_include_list_inside_dict
    with pytest.raises(errors.IncludeMismatchError) as e:
        loads(f'''
          foo: bar
          !include {listfile}
        ''')
    assert e.exconly() == \
        'yconf.errors.IncludeMismatchError: (stream):2:19: Trying to ' \
        'include `<class \'list\'>` inside `<class \'yconf.parser.Meld\'>`: ' \
        f'VALUE `{listfile}`'

    # test_include_dict_inside_chain
    with pytest.raises(errors.IncludeMismatchError) as e:
        loads(f'''
          - baz
          !include {dictfile}
        ''')
    assert e.exconly() == \
        'yconf.errors.IncludeMismatchError: (stream):2:19: Trying to ' \
        'include `<class \'yconf.parser.Meld\'>` inside `<class \'list\'>`: ' \
        f'VALUE `{dictfile}`'

    with pytest.raises(errors.ExpectedTokenError) as e:
        loads('!include')

    assert e.exconly() == \
        'yconf.errors.ExpectedTokenError: (stream):0:0: Expected VALUE, ' \
        'found: EOF `None`'


def test_include_emptydocument(mktmpfile):
    dictfile = mktmpfile(name='qux.yml', content='''
      foo: BAR
    ''')
    listfile = mktmpfile(name='qux.yml', content='''
      - foo
      - bar
    ''')
    literalfile = mktmpfile(name='qux.yml', content='foo')

    m = loads(f'!include {dictfile}')
    assert m.foo == 'BAR'

    m = loads(f'!include {listfile}')
    assert m == ['foo', 'bar']

    m = loads(f'!include {literalfile}')
    assert m == 'foo'


def test_include_chain(mktmpfile):
    qux = mktmpfile(name='qux.yml', content='''
      - foo
      - bar
    ''')

    m = loads(f'''
      - baz
      !include {qux}
    ''')

    assert m == ['baz', 'foo', 'bar']


def test_include_literal(mktmpfile):
    qux = mktmpfile(name='qux.yml', content='FOO')

    m = loads(f'- !include {qux}')
    assert m[0] == 'FOO'

    m = loads(f'foo: !include {qux}')
    assert m.foo == 'FOO'


def test_include_meld(mktmpfile):
    qux = mktmpfile(name='qux.yml', content='''
      foo: BAR
      bar: FOO
      baz:
       a: 1
    ''')

    thud = mktmpfile(name='thud.yml', content='''
      d: 4
    ''')

    m = loads(f'''
      foo: bar
      baz:
        b: 2
        c: 3
        !include {thud}

      !include {qux}
    ''')

    assert m.foo == 'BAR'
    assert m.bar == 'FOO'
    assert m.baz.a == 1
    assert m.baz.b == 2
    assert m.baz.c == 3
    assert m.baz.d == 4
