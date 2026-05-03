from yconf.tokenizer import tokenize
from yconf import tokens as t


# TODO: capital letters
# TODO: error on duplicate tokens
def test_tokenizer():
    tokens = tokenize('''
      foo: abc
      bar: 123
      baz: .2
    ''')

    tok = next(tokens)
    assert isinstance(tok, t.String)
    assert tok.indent == 6
    assert tok.key == 'foo'
    assert tok.value == 'abc'

    tok = next(tokens)
    assert isinstance(tok, t.Int)
    assert tok.indent == 6
    assert tok.key == 'bar'
    assert tok.value == 123

    tok = next(tokens)
    assert isinstance(tok, t.Float)
    assert tok.indent == 6
    assert tok.key == 'baz'
    assert tok.value == .2
