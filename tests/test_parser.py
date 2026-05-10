import pytest

from yconf import loads, Meld, errors


"""
                               Meld    list
                                ^       ^
                                |       |
      | CR | indt+ | indt-   | key   | dash  | value | None   | tag
--------------------------------------------------------------------------
New   | NC | New   | < None  | > new | > new | < val | < None | Meld/list
Meld  | NC | New > | < Meld  | > new | Error | Error | < None | Meld
list  | NC | New > | < list  | Error | > new | Error | < None | list


guide:
<       return
>       recurse
"""


def test_parser_unknowntag():
    with pytest.raises(errors.UnknownTagError) as e:
        loads('!foobar:')

    assert e.exconly() == \
        'yconf.errors.UnknownTagError: (stream):0:0: Unknown tag: ' \
        'foobar: tag `foobar`'


def test_parser_indentation_errors():
    with pytest.raises(errors.ImproperIndentationError) as e:
        loads('''
          foo:
         bar:
        ''')
    assert e.exconly() == \
        'yconf.errors.ImproperIndentationError: (stream):2:9: ' \
        'Improper indentation: key `bar`'

    with pytest.raises(errors.ImproperIndentationError) as e:
        loads('''
          foo:
            bar: 1
           baz: 2
        ''')
    assert e.exconly() == \
        'yconf.errors.ImproperIndentationError: (stream):3:11: ' \
        'Improper indentation: key `baz`'

    with pytest.raises(errors.ImproperIndentationError) as e:
        loads('''
          foo:
            bar: 1
             baz: 2
        ''')
    assert e.exconly() == \
        'yconf.errors.ImproperIndentationError: (stream):3:13: ' \
        'Improper indentation: key `baz`'


def test_parser_chain_errors():
    with pytest.raises(errors.InvalidTokenError) as e:
        loads('''
          - foo
          bar: 1
        ''')

    assert e.exconly() == \
        'yconf.errors.InvalidTokenError: (stream):2:10: Invalid token: ' \
        'key `bar`'

    with pytest.raises(errors.InvalidTokenError) as e:
        loads('''
          - foo
          bar
        ''')

    assert e.exconly() == \
        'yconf.errors.InvalidTokenError: (stream):2:10: Invalid token: ' \
        'string `bar`'


def test_parser_meld_errors():
    with pytest.raises(errors.InvalidTokenError) as e:
        loads('''
          foo: 2
          - baz
        ''')

    assert e.exconly() == \
        'yconf.errors.InvalidTokenError: (stream):2:10: Invalid token: ' \
        'dash `-`'

    with pytest.raises(errors.InvalidTokenError) as e:
        loads('''
          foo: bar
          baz
        ''')

    assert e.exconly() == \
        'yconf.errors.InvalidTokenError: (stream):2:10: Invalid token: ' \
        'string `baz`'


def test_parser_chain_meld():
    m = loads('''
      - foo
      - bar: 2
        baz: 3
      -
        qux: 4
    ''')

    assert isinstance(m, list)
    assert m[0] == 'foo'
    assert m[1].bar == 2
    assert m[1].baz == 3
    assert m[2].qux == 4


def test_parser_chain():
    m = loads('''
      - foo
      - .73
    ''')

    assert isinstance(m, list)
    assert m[0] == 'foo'
    assert m[1] == .73


def test_parser_meld():
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
      foo: bar: 1
           baz: 2
    ''')
    assert m.foo.bar == 1
    assert m.foo.baz == 2


def test_parser_literal():
    n = loads('')
    assert n is None

    n = loads('   ')
    assert n is None

    n = loads('\n\n\n')
    assert n is None

    n = loads('foo')
    assert n == 'foo'

    n = loads('"foo"')
    assert n == 'foo'

    n = loads('\'foo\'')
    assert n == 'foo'

    n = loads('foo\n\n\n')
    assert n == 'foo'

    n = loads('\nfoo')
    assert n == 'foo'

    n = loads('.73')
    assert n == .73
