from .tokenizer import tokenize, Colon, Dash
from .errors import IndentationError


class Meld(dict):
    def __init__(self, value):
        if isinstance(value, str):
            self._parse(value)

    def __getattr__(self, key):
        if key not in self:
            raise AttributeError(key)

        return self[key]

    def __setattr__(self, key, value):
        if isinstance(value, dict):
            super().__setitem__(key, Meld(value))
            return

        super().__setitem__(key, value)

    def __delattr__(self, key):
        if key not in self:
            raise AttributeError(key)

        del self[key]

    def _eatone(self, token):
        if isinstance(token, Colon):
            self[token.key] = token.value

    def _eatall(self, tokens):
        first = next(tokens)
        idntoff = first.indent
        idntsz = 0
        curidnt = 0

        self._eatone(first)
        while True:
            tok = next(tokens)
            idnt = tok.indent - idntoff - curidnt
            if not idnt:
                self._eatone(tok)
                continue

            # new block
            if not idntsz:
                # preserve the indent size
                idntsz = idnt

            if idnt != idntsz:
                raise errors.IndentationError(tok)

            try:
                nt = next(tokens)
            except StopIteration:
                # threat an None keyvalue token
                self._eatone(tok)
            # elif isinstance(nt, Dash):

    def _parse(self, s):
        try:
            self._eatall(tokenize(s))
        except StopIteration:
            return
