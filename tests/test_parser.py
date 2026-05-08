from yconf import loads, Meld, Chain


"""
                                          Meld     Chain
                                           ^        ^
                                           |        |
      | newline | indent-in | indent-out | key   | dash  | literal | None
------------------------------------------------------------------------------
New   | NC      | New       | ret None   | > new | > new | ret val | ret None
Meld  | NC      | New ->    | ret Meld   | > new | Error | Error   | ret None
Chain | NC      | New ->    | ret Chain  | Error | > new | Error   | ret None
"""




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

# TODO: error on duplicate tokens
def test_parser_literal():
    n = loads('')
    assert n == None

    n = loads('\n\n\n')
    assert n == None

    n = loads('foo')
    assert n == 'foo'

    n = loads('foo\n')
    assert n == 'foo'

    n = loads('\nfoo')
    assert n == 'foo'

    n = loads('.73')
    assert n == .73
