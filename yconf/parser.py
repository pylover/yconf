from . import tokenizer, errors


class Parser(tokenizer.Tokenizer):
    def __init__(self, s):
        from .registry import constructors

        self._indentoffset = None
        self._indent = None
        self._indentsize = None
        self._constructors = constructors
        super().__init__(s)

    def _tokindent(self, tok):
        indent = (tok.value - self._indentoffset)
        if self.peek():
            if indent < 0 or (self._indentsize and indent % self._indentsize):
                raise errors.ImproperIndentationError(self.peek())

        return indent

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
                    if self._indentsize is None:
                        self._indentsize = self._indent
                elif self._isindentout(tok):
                    return this

                continue

            if tok.isliteral():
                if this is not None:
                    raise errors.InvalidTokenError(tok)

                return tok.value

            if tok.iskey():
                if this is None:
                    this = self._constructors['dict']()
                elif not isinstance(this, dict):
                    raise errors.InvalidTokenError(tok)
                elif tok.value in this:
                    raise errors.KeyAlreadyExistsError(tok)

                this[tok.value] = self.parse()

            elif tok.isdash():
                if this is None:
                    this = self._constructors['list']()
                elif not isinstance(this, list):
                    raise errors.InvalidTokenError(tok)

                this.append(self.parse())
