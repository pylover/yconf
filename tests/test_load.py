# import pytest
#
# from yconf import load, errors
#
#
# def test_load(mktmpfile, fileio):
#     file = mktmpfile(content='''
#       foo: bar
#       bar:
#         - baz
#         - baz
#     ''')
#
#     m = load(file)
#     assert m.foo == 'bar'
#     assert m.bar == ['baz', 'baz']
#
#     file = fileio(content='''
#       foo:
#         - bar
#         - baz
#     ''')
#     m = load(file)
#     assert m.foo == ['bar', 'baz']
#
#     file = mktmpfile(content='!foobar:')
#     with pytest.raises(errors.UnknownTagError) as e:
#         load(file)
#
#     assert e.exconly() == \
#         f'yconf.errors.UnknownTagError: {file}:0:0: Unknown tag: ' \
#         'foobar: tag `foobar`'
