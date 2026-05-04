from yconf.tokenizer import tokenize, Colon, Dash, Literal


def test_tokenizer_comment():
    assert not list(tokenize('# foo'))
    assert not list(tokenize('  # foo'))


def test_tokenizer_literal():
    assert not list(tokenize(''))
    assert not list(tokenize(' '))

    tok = next(tokenize('foo'))
    assert isinstance(tok, Literal)
    assert tok.indent == 0
    assert tok.value == 'foo'


def test_tokenizer_colon():
    tokens = tokenize('''
      foo: abC
      bar: 123
      BAZ: .2
        thud: false
    ''')

    tok = next(tokens)
    assert isinstance(tok, Colon)
    assert tok.indent == 6
    assert tok.key == 'foo'
    assert tok.value == 'abC'

    tok = next(tokens)
    assert tok.key == 'bar'
    assert tok.value == 123

    tok = next(tokens)
    assert tok.key == 'BAZ'
    assert tok.value == .2

    tok = next(tokens)
    assert tok.key == 'thud'
    assert tok.indent == 8
    assert tok.value is False


def test_tokenizer_dash():
    tokens = tokenize('''
      - foo
      - 1
      - .3
    ''')

    tok = next(tokens)
    assert isinstance(tok, Dash)
    assert tok.indent == 6
    assert tok.value == 'foo'

    tok = next(tokens)
    assert tok.value == 1

    tok = next(tokens)
    assert tok.value == .3
