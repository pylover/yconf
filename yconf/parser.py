from .tokenizer import Tokenizer
from .models import Meld, Chain
from .errors import InvalidTokenError


class Parser(Tokenizer):
    def __init__(self, s):
        self._indentoffset = None
        self._indent = 0
        self._indentsize = None
        super().__init__(s)

    def _isindentout(self, tok):
        return (tok.value - self._indentoffset) < self._indent

    def _isindentin(self, tok):
        return (tok.value - self._indentoffset) > self._indent

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
                elif self._isindentin(tok):
                    self._indent = tok.value - self._indentoffset
                elif self._isindentout(tok):
                    return this

                continue

            if tok.isliteral():
                return tok.value

            if tok.iskey():
                if this is None:
                    this = Meld()
                elif not isinstance(this, Meld):
                    raise InvalidTokenError(tok)

                this[tok.value] = self.parse()

            elif tok.isdash():
                if this is None:
                    this = Dash()
                elif not isinstance(this, Dash):
                    raise InvalidTokenError(tok)

                this.append(self.parse())


def loads(s):
    parser = Parser(s)
    node = parser.parse()
    return node
