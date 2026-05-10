from yconf.tokenizer import Tokenizer, Kind


def test_tokenizer_include():
    t = Tokenizer('!include foo')
    assert t.pop() == (Kind.TAG, 'include', 0, 0)
    assert t.pop() == (Kind.STRING, 'foo', 0, 9)

    t = Tokenizer('''
      !include foo
    ''')
    t.pop()
    t.pop()
    assert t.pop() == (Kind.TAG, 'include', 1, 6)
    assert t.pop() == (Kind.STRING, 'foo', 1, 15)


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


def test_tokenizer_bool():
    assert Tokenizer('false').pop() == (Kind.BOOL, False, 0, 0)
    assert Tokenizer('False').pop() == (Kind.BOOL, False, 0, 0)
    assert Tokenizer('no').pop() == (Kind.BOOL, False, 0, 0)
    assert Tokenizer('true').pop() == (Kind.BOOL, True, 0, 0)
    assert Tokenizer('yes').pop() == (Kind.BOOL, True, 0, 0)


def test_tokenizer_key():
    t = Tokenizer('bar: postgres://:@/foo')
    assert t.pop() == (Kind.KEY, 'bar', 0, 0)
    assert t.pop() == (Kind.STRING, 'postgres://:@/foo', 0, 5)

    t = Tokenizer('''\
      foo: :::
    ''')

    assert t.pop() == (Kind.INDENT, 6, 0, 0)
    assert t.pop() == (Kind.KEY, 'foo', 0, 6)
    assert t.pop() == (Kind.STRING, ':::', 0, 11)


def test_tokenizer_peek():
    t = Tokenizer('foo: bar')
    assert t.peek().value == 'foo'
    assert t.pop().value == 'foo'

    assert t.peek().value == 'bar'
    assert t.peek().value == 'bar'
    assert t.pop().value == 'bar'

    assert t.peek() is None
    assert t.pop() is None


def test_tokenizer_isliteral():
    t = Tokenizer('foo')
    tok = t.pop()
    assert tok.isliteral()
