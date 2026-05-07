from yconf import loads


# TODO: error on duplicate tokens
def test_parser_literal():
    n = loads('')
    assert n == None

    n = loads('foo')
    assert n == 'foo'

    n = loads('foo\n')
    assert n == 'foo'

    n = loads('.73')
    assert n == .73


# def test_parser_meld():
#     m = loads('''
#       foo: FOO
#       bar: 1
#     ''')
#
#     assert isinstance(m, Meld)
#
#     # assert m.foo == 'FOO'
#     # assert m.bar == 1
