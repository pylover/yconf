from .tokenizer import Tokenizer


def _parse(tokens, indent=0, indentsize=0):
    pass


def loads(s):
    tokens = Tokenizer(s)
    node = _parse(tokens)
    return node
