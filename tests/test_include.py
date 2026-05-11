# import pytest
#
# from yconf import loads, errors
#
#
# def test_include_error(mktmpfile):
#     with pytest.raises(errors.ExpectedTokenError) as e:
#         loads('!include')
#
#     assert e.exconly() == \
#         'yconf.errors.ExpectedTokenError: (stream):0:0: Expected filename: ' \
#         'tag `include`'
#
#
# def test_include_literal(mktmpfile):
#     qux = mktmpfile(name='qux.yml', content='FOO')
#
#     m = loads(f'foo: !include {qux}')
#     assert m.foo == 'FOO'
#
#     m = loads(f'- !include {qux}')
#     assert m[0] == 'FOO'
#
#
# def test_include_chain(mktmpfile):
#     qux = mktmpfile(name='qux.yml', content='''
#       - foo
#       - bar
#     ''')
#
#     m = loads(f'''
#       - baz
#       !include {qux}
#     ''')
#
#     assert m == ['baz', 'foo', 'bar']
#
#
# def test_include_emptymeld(mktmpfile):
#     qux = mktmpfile(name='qux.yml', content='''
#       foo: BAR
#     ''')
#
#     m = loads(f'!include {qux}')
#
#     assert m.foo == 'BAR'
#
#
# def test_include_meld(mktmpfile):
#     qux = mktmpfile(name='qux.yml', content='''
#       foo: BAR
#       bar: FOO
#       baz:
#        a: 1
#     ''')
#
#     thud = mktmpfile(name='thud.yml', content='''
#       d: 4
#     ''')
#
#     corge = mktmpfile(content='''
#       zero: 0
#       a: a
#       b: b
#     ''')
#
#     m = loads(f'''
#       foo: bar
#       baz: !include {corge}
#         b: 2
#         c: 3
#         !include {thud}
#
#       !include {qux}
#     ''')
#
#     assert m.foo == 'BAR'
#     assert m.bar == 'FOO'
#     assert m.baz.zero == 0
#     assert m.baz.a == 1
#     assert m.baz.b == 2
#     assert m.baz.c == 3
#     assert m.baz.d == 4
