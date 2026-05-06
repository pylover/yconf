import pytest

from yconf.tokenizer import tokenize, Kind


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
    assert next(tokenize('foo ')) == (Kind.STRING, 'foo ', 0, 0)
    assert next(tokenize('"foo"')) == (Kind.STRING, 'foo', 0, 0)
    assert next(tokenize('\'foo\'')) == (Kind.STRING, 'foo', 0, 0)
    assert next(tokenize('3.')) == (Kind.STRING, '3.', 0, 0)

    tokens = tokenize('foo: bar')
    assert next(tokens) == (Kind.KEY, 'foo', 0, 0)
    assert next(tokens) == (Kind.COLON, ':', 0, 3)
    assert next(tokens) == (Kind.STRING, 'bar', 0, 5)


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


def test_tokenizer_float():
    assert next(tokenize('.1')) == (Kind.FLOAT, .1, 0, 0)
    assert next(tokenize('3.1')) == (Kind.FLOAT, 3.1, 0, 0)
    assert next(tokenize('-3.1')) == (Kind.FLOAT, -3.1, 0, 0)
    assert next(tokenize('-.1')) == (Kind.FLOAT, -0.1, 0, 0)


def test_tokenizer_int():
    assert next(tokenize('1')) == (Kind.INT, 1, 0, 0)
    assert next(tokenize('-73')) == (Kind.INT, -73, 0, 0)
