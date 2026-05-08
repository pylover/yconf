from .tokenizer import Tokenizer
from .models import Meld, Chain
from .errors import InvalidTokenError


class Parser(Tokenizer):
    def __init__(self, s):
        self._indentoffset = None
        self._indent = None
        self._indentsize = None
        super().__init__(s)

    def _tokindent(self, tok):
        return (tok.value - self._indentoffset)

    def _isindentout(self, tok):
        return self._tokindent(tok) < self._indent

    def _isindentin(self, tok):
        return self._tokindent(tok) > self._indent

    def parse(self):
        this = None
        while True:
            tok = self.pop()

            if tok is None:
                return this

            if tok.isnewline():
                continue

            if tok.isindent():
                if self._indentoffset is None:
                    self._indentoffset = tok.value
                    self._indent = 0
                elif self._isindentin(tok):
                    self._indent = self._tokindent(tok)
                elif self._isindentout(tok):
                    return this

                continue

            if tok.isliteral():
                if this is not None:
                    raise InvalidTokenError(tok)

                return tok.value

            if tok.iskey():
                if this is None:
                    this = Meld()
                elif not isinstance(this, Meld):
                    raise InvalidTokenError(tok)

                this[tok.value] = self.parse()

            elif tok.isdash():
                if this is None:
                    this = Chain()
                elif not isinstance(this, Chain):
                    raise InvalidTokenError(tok)

                this.append(self.parse())


def loads(s):
    return Parser(s).parse()
