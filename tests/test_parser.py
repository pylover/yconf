import pytest

from snam import loads, Meld, errors


def test_parse_inline_python_objects():
    m = loads('''
      - {'FOO': 73}
      - foo: ['foo', 'bar']
    ''')
    assert m[0].FOO == 73
    assert m[1].foo == ['foo', 'bar']

    assert loads('[1, 2, 3]', [1, 2, 3])
    assert loads('{1, 2, 3}') == {1, 2, 3}
    assert loads('{"foo": "bar"}', dict(foo="bar"))
    assert loads('{"foo": 73}', dict(foo=73))
    assert loads('[foo]') == '[foo]'


def test_parse_comment():
    m = loads('''
      # lorem ipsum
      - :  # abjad hovvaz
        bar: # ghareshat
        baz: 2
    ''')
    assert m[0].bar is None
    assert m[0].baz == 2


def test_parse_unknowntag():
    with pytest.raises(errors.ExpectedTokenError) as e:
        loads('!')

    assert e.exconly() == \
        'snam.errors.ExpectedTokenError: (stream):0:0: Expected TAG, ' \
        'found: EOF `None`'

    with pytest.raises(errors.UnknownTagError) as e:
        loads('!foobar')

    assert e.exconly() == \
        'snam.errors.UnknownTagError: (stream):0:0: Unknown: ' \
        'TAG `foobar`'


def test_parse_list():
    m = loads('''
      - :
        bar: 1
        baz: 2
    ''')
    assert m[0].bar == 1
    assert m[0].baz == 2

    m = loads('''
      -:
        bar: 1
        baz: 2
    ''')
    assert m['-'].bar == 1
    assert m['-'].baz == 2

    m = loads('''
      - foo:
          bar: 1
    ''')
    assert m[0].foo.bar == 1

    m = loads('''
      - foo:
        bar: 1
    ''')
    assert m[0].foo is None
    assert m[0].bar == 1

    m = loads('''
      - foo
      - .73
    ''')

    assert isinstance(m, list)
    assert m[0] == 'foo'
    assert m[1] == .73

    m = loads('''
      - foo
      -
        bar: 2
        baz: 3
      -
        qux: 4
    ''')

    assert isinstance(m, list)
    assert m[0] == 'foo'
    assert m[1].bar == 2
    assert m[1].baz == 3
    assert m[2].qux == 4


def test_parse_errors():
    with pytest.raises(errors.InvalidTokenError) as e:
        loads('''
          foo: bar
          baz
        ''')
    assert e.exconly() == \
        'snam.errors.InvalidTokenError: (stream):2:10: Invalid token: ' \
        'VALUE `baz`'

    with pytest.raises(errors.InvalidTokenError) as e:
        loads(':')
    assert e.exconly() == \
        'snam.errors.InvalidTokenError: (stream):0:0: Invalid token: ' \
        'COLON `:`'

    with pytest.raises(errors.InvalidTokenError) as e:
        loads('''
          foo: 2
          - baz
        ''')
    assert e.exconly() == \
        'snam.errors.InvalidTokenError: (stream):2:10: Invalid token: ' \
        'DASH `-`'

    with pytest.raises(errors.InvalidTokenError) as e:
        loads('''
          - foo
          bar
        ''')
    assert e.exconly() == \
        'snam.errors.InvalidTokenError: (stream):2:10: Invalid token: ' \
        'VALUE `bar`'

    with pytest.raises(errors.InvalidTokenError) as e:
        loads('''
          - foo
          bar: 1
        ''')
    assert e.exconly() == \
        'snam.errors.InvalidTokenError: (stream):2:10: Invalid token: ' \
        'KEY `bar`'


def test_parse_meld():
    m = loads('foo: postgresql://:@/foo')
    assert m.foo == 'postgresql://:@/foo'

    m = loads('foo:')
    assert m.foo is None

    m = loads('''
      foo: FOO
      bar: 1
      baz:
        a: 11
        b: 22
      qux: quux
    ''')

    assert isinstance(m, Meld)
    assert m.foo == 'FOO'
    assert m.bar == 1
    assert m.baz.a == 11
    assert m.baz.b == 22
    assert m.qux == 'quux'

    m = loads('''
      foo:
        bar: 1
        baz: 2
    ''')
    assert m.foo.bar == 1
    assert m.foo.baz == 2

    m = loads('''
      foo:
      bar: baz
    ''')
    assert m.foo is None
    assert m.bar == 'baz'


def test_parse_literal():
    assert loads('') is None
    assert loads('   ') is None
    assert loads('\n\n\n') is None
    assert loads('None') is None
    assert loads('none') is None
    assert loads('null') is None

    assert loads('yes') is True
    assert loads('true') is True
    assert loads('on') is True
    assert loads('no') is False
    assert loads('false') is False
    assert loads('off') is False

    assert loads('foo') == 'foo'
    assert loads('"foo"') == 'foo'
    assert loads('\'foo\'') == 'foo'
    assert loads('foo\n\n\n') == 'foo'
    assert loads('\nfoo') == 'foo'
    assert loads(':foo') == ':foo'
    assert loads('.73') == .73


def test_parse_indentation():
    m = loads('\n'.join([
        'foo:',
        '  bar: baz',
        'qux: thud',
    ]))
    assert m.foo.bar == 'baz'
    assert m.qux == 'thud'

    m = loads('''
      foo:
        bar:
      baz:
        qux: false
    ''')
    assert m.baz.qux is False

    m = loads('''
      foo:
       a: 1
    ''')
    assert m.foo.a == 1

    m = loads('''
      foo:
            a: 1
    ''')
    assert m.foo.a == 1
