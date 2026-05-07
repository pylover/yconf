from yconf.tokenizer import Tokenizer, Kind


def test_tokenizer_newline_indent_comment():
    t = Tokenizer('''
        foo
        bar baz
        # comment
    ''')

    assert t.pop() == (Kind.NEWLINE, '\n', 0, 0)
    assert t.pop() == (Kind.INDENT, 8, 1, 0)
    assert t.pop() == (Kind.STRING, 'foo', 1, 8)
    assert t.pop() == (Kind.NEWLINE, '\n', 1, 11)
    assert t.pop() == (Kind.INDENT, 8, 2, 0)
    assert t.pop() == (Kind.STRING, 'bar baz', 2, 8)
    assert t.pop() == (Kind.NEWLINE, '\n', 2, 15)
    assert t.pop() == (Kind.INDENT, 8, 3, 0)
    assert t.pop() == (Kind.NEWLINE, '\n', 3, 17)
    assert t.pop() == (Kind.INDENT, 4, 4, 0)
    assert t.pop() is None


def test_tokenizer_string():
    assert Tokenizer('foo').pop() == (Kind.STRING, 'foo', 0, 0)
    assert Tokenizer('foo ').pop() == (Kind.STRING, 'foo ', 0, 0)
    assert Tokenizer('"foo"').pop() == (Kind.STRING, 'foo', 0, 0)
    assert Tokenizer('\'foo\'').pop() == (Kind.STRING, 'foo', 0, 0)
    assert Tokenizer('3.').pop() == (Kind.STRING, '3.', 0, 0)

    t = Tokenizer('foo: bar')
    assert t.pop() == (Kind.KEY, 'foo', 0, 0)
    assert t.pop() == (Kind.STRING, 'bar', 0, 5)


def test_tokenizer_colon_dash():
    t = Tokenizer('''\
      foo:
        - bar
        -
    ''')

    assert t.pop() == (Kind.INDENT, 6, 0, 0)
    assert t.pop() == (Kind.KEY, 'foo', 0, 6)
    assert t.pop() == (Kind.NEWLINE, '\n', 0, 10)
    assert t.pop() == (Kind.INDENT, 8, 1, 0)
    assert t.pop() == (Kind.DASH, '-', 1, 8)
    assert t.pop() == (Kind.STRING, 'bar', 1, 10)
    assert t.pop() == (Kind.NEWLINE, '\n', 1, 13)
    assert t.pop() == (Kind.INDENT, 8, 2, 0)
    assert t.pop() == (Kind.DASH, '-', 2, 8)
    assert t.pop() == (Kind.NEWLINE, '\n', 2, 9)
    assert t.pop() == (Kind.INDENT, 4, 3, 0)
    assert t.pop() is None


def test_tokenizer_float():
    assert Tokenizer('.1').pop() == (Kind.FLOAT, .1, 0, 0)
    assert Tokenizer('3.1').pop() == (Kind.FLOAT, 3.1, 0, 0)
    assert Tokenizer('-3.1').pop() == (Kind.FLOAT, -3.1, 0, 0)
    assert Tokenizer('-.1').pop() == (Kind.FLOAT, -0.1, 0, 0)


def test_tokenizer_int():
    assert Tokenizer('1').pop() == (Kind.INT, 1, 0, 0)
    assert Tokenizer('-73').pop() == (Kind.INT, -73, 0, 0)


def test_tokenizer_exceptions():
    t = Tokenizer('''\
      foo::::
    ''')

    assert t.pop() == (Kind.INDENT, 6, 0, 0)
    assert t.pop() == (Kind.KEY, 'foo', 0, 6)
    assert t.pop() == (Kind.STRING, ':::', 0, 10)


def test_tokenizer_peek():
    t = Tokenizer('foo: bar')
    assert t.peek().value == 'foo'
    assert t.pop().value == 'foo'

    assert t.peek().value == 'bar'
    assert t.peek().value == 'bar'
    assert t.pop().value == 'bar'

    assert t.peek() is None
    assert t.pop() is None
