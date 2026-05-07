from .tokenizer import Tokenizer
from .models import Meld, Chain
from .errors import InvalidTokenError


class Parser:
    def __init__(self, s):
        self._indentoffset = None
        self._indent = None
        self._indentsize = None
        self._tokz = Tokenizer(s)

    def _assertnext_none_or_newline(self):
        nxtok = self._tokz.peek()
        if nxtok is None or nxtok.isnewline():
            return

        raise InvalidTokenError(self._tokz.peek())

    def parse(self):
        tok = self._tokz.pop()
        if tok is None:
            return None

        if tok.isliteral():
            self._assertnext_none_or_newline()
            return tok.value

        # if tok.isindent():
        #     if self._indentoffset is None:
        #         self._indentoffset = tok.value
        #         self._indent = 0
        #     if not (tok := tokenizer.pop()):
        #         return None

        # if tok.iskey():
        #     this = Meld()
        # elif tok.isdash():
        #     this = Chain()
        # else:
        #     raise InvalidTokenError(tok)

        # return this
#
#     while True:
#
#     nxtok = tokenizer.peek()

def loads(s):
    parser = Parser(s)
    node = parser.parse()
    return node
