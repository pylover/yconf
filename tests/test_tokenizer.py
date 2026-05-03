from yconf.tokenizer import tokenize
from yconf import tokens as t


def test_tokenizer_keyvaluepair():
    tokens = tokenize('''
      foo: abC
      bar: 123
      BAZ: .2
    ''')

    tok = next(tokens)
    assert isinstance(tok, t.String)
    assert tok.indent == 6
    assert tok.key == 'foo'
    assert tok.value == 'abC'

    tok = next(tokens)
    assert isinstance(tok, t.Int)
    assert tok.indent == 6
    assert tok.key == 'bar'
    assert tok.value == 123

    tok = next(tokens)
    assert isinstance(tok, t.Float)
    assert tok.indent == 6
    assert tok.key == 'BAZ'
    assert tok.value == .2


def test_tokenizer_dict():
    tokens = tokenize('''
      foo:
        bar: BAR
    ''')

    tok = next(tokens)
    assert isinstance(tok, t.Key)
