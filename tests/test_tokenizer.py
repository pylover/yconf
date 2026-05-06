import pytest

from yconf.tokenizer import tokenize, Token, Kind


def test_tokenizer_newline_indent_comment():
    tokens = tokenize('''
        foo
        bar baz
        # comment
    ''')

    assert next(tokens) == (Kind.NEWLINE, '\n', 0, 0)
    assert next(tokens) == (Kind.INDENT, 8, 1, 0)
    assert next(tokens) == (Kind.STRING, 'foo', 1, 8)
    assert next(tokens) == (Kind.NEWLINE, '\n', 1, 11)
    assert next(tokens) == (Kind.INDENT, 8, 2, 0)
    assert next(tokens) == (Kind.STRING, 'bar baz', 2, 8)
    assert next(tokens) == (Kind.NEWLINE, '\n', 2, 15)
    assert next(tokens) == (Kind.INDENT, 8, 3, 0)
    assert next(tokens) == (Kind.NEWLINE, '\n', 3, 17)
    assert next(tokens) == (Kind.INDENT, 4, 4, 0)
    with pytest.raises(StopIteration):
        next(tokens)


def test_tokenizer_string():
    assert next(tokenize('foo')) == (Kind.STRING, 'foo', 0, 0)
    assert next(tokenize('"foo"')) == (Kind.STRING, 'foo', 0, 0)
    assert next(tokenize('\'foo\'')) == (Kind.STRING, 'foo', 0, 0)


def test_tokenizer_colon_dash():
    tokens = tokenize('''\
      foo:
        - bar
        -
    ''')

    assert next(tokens) == (Kind.INDENT, 6, 0, 0)
    assert next(tokens) == (Kind.KEY, 'foo', 0, 6)
    assert next(tokens) == (Kind.COLON, ':', 0, 9)
    assert next(tokens) == (Kind.NEWLINE, '\n', 0, 10)
    assert next(tokens) == (Kind.INDENT, 8, 1, 0)
    assert next(tokens) == (Kind.DASH, '-', 1, 8)
    assert next(tokens) == (Kind.STRING, 'bar', 1, 10)
    assert next(tokens) == (Kind.NEWLINE, '\n', 1, 13)
    assert next(tokens) == (Kind.INDENT, 8, 2, 0)
    assert next(tokens) == (Kind.DASH, '-', 2, 8)
    assert next(tokens) == (Kind.NEWLINE, '\n', 2, 9)
    assert next(tokens) == (Kind.INDENT, 4, 3, 0)
    with pytest.raises(StopIteration):
        next(tokens)


# def test_tokenizer_float():
#     assert next(tokenize('.1')) == (Kind.STRING, .1, 0, 0)
#     assert not list(tokenize('# foo'))
#     assert not list(tokenize('  # foo'))
#
#
# def test_tokenizer_literal():
#     assert not list(tokenize(''))
#     assert not list(tokenize(' '))
#
#     tok = next(tokenize('foo'))
#     assert isinstance(tok, Literal)
#     assert tok.indent == 0
#     assert tok.value == 'foo'
#
#
# def test_tokenizer_colon():
#     tokens = tokenize('''
#       foo: abC
#       bar: 123
#       BAZ: .2
#         thud: false
#     ''')
#
#     tok = next(tokens)
#     assert isinstance(tok, Colon)
#     assert tok.indent == 6
#     assert tok.key == 'foo'
#     assert tok.value == 'abC'
#
#     tok = next(tokens)
#     assert tok.key == 'bar'
#     assert tok.value == 123
#
#     tok = next(tokens)
#     assert tok.key == 'BAZ'
#     assert tok.value == .2
#
#     tok = next(tokens)
#     assert tok.key == 'thud'
#     assert tok.indent == 8
#     assert tok.value is False
#
#
# def test_tokenizer_dash():
#     tokens = tokenize('''
#       - foo
#       - 1
#       - .3
#     ''')
#
#     tok = next(tokens)
#     assert isinstance(tok, Dash)
#     assert tok.indent == 6
#     assert tok.value == 'foo'
#
#     tok = next(tokens)
#     assert tok.value == 1
#
#     tok = next(tokens)
#     assert tok.value == .3
