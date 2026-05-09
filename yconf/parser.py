import os
import copy
import subprocess

from . import tokenizer, errors


class Meld(dict):
    def __init__(self, data=None):
        if isinstance(data, str):
            super().__init__()
            self |= data

        else:
            super().__init__(data or [])

    def __getattr__(self, key):
        if key not in self:
            raise AttributeError(key)

        return self[key]

    def __setattr__(self, key, value):
        super().__setitem__(key, value)

    def __delattr__(self, key):
        if key not in self:
            raise AttributeError(key)

        del self[key]

    def __ior__(self, data):
        if isinstance(data, str):
            data = loads(data)
        elif not isinstance(data, dict):
            raise TypeError(
                'Only dict and or it\'s subclasses are allowed, '
                f'given: {type(data)}')
        else:
            data = copy.deepcopy(data)

        for k, other in data.items():
            mine = self.get(k)

            if isinstance(mine, Meld):
                mine |= other

            else:
                self[k] = other

        return self


class Parser(tokenizer.Tokenizer):
    def __init__(self, s, filename=None):
        self._indentoffset = None
        self._indent = None
        self._indentsize = None
        self._filename = filename
        super().__init__(s)

    def _tokindent(self, tok):
        indent = (tok.value - self._indentoffset)
        if self.peek():
            if indent < 0 or (self._indentsize and indent % self._indentsize):
                raise errors.ImproperIndentationError(
                    self.peek(), self._filename
                )

        return indent

    def _isindentout(self, tok):
        return self._tokindent(tok) < self._indent

    def _isindentin(self, tok):
        return self._tokindent(tok) > self._indent

    def _include(self, this, tok):
        m = load(tok.value)
        if this is None:
            return m

        if isinstance(this, dict):
            this |= m

        elif isinstance(this, list):
            this.extend(m)

        return this

    def _environ(self, this, tok):
        return os.environ.get(tok.value)

    def _shell(self, this, tok):
        result = subprocess.run(
            tok.value,
            shell=True,
            check=True,
            text=True,
            capture_output=True,
        )

        return result.stdout.strip()

    def _tag(self, this, tok):
        if tok.value == 'include':
            if self.peek() is None:
                raise errors.ExpectedTokenError(
                    tok, 'filename', self._filename
                )

            return self._include(this, self.pop())

        if tok.value == 'env':
            if self.peek() is None:
                raise errors.ExpectedTokenError(
                    tok, 'environment variable', self._filename
                )

            return self._environ(this, self.pop())

        if tok.value == 'shell':
            if self.peek() is None:
                raise errors.ExpectedTokenError(
                    tok, 'shell command', self._filename
                )

            return self._shell(this, self.pop())

        raise errors.UnknownTagError(tok, self._filename)

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
                    raise errors.InvalidTokenError(tok, self._filename)

                return tok.value

            if tok.iskey():
                if this is None:
                    this = Meld()
                elif not isinstance(this, dict):
                    raise errors.InvalidTokenError(tok, self._filename)

                this[tok.value] = self.parse()

            elif tok.isdash():
                if this is None:
                    this = list()
                elif not isinstance(this, list):
                    raise errors.InvalidTokenError(tok, self._filename)

                this.append(self.parse())

            elif tok.istag():
                this = self._tag(this, tok)


def loads(s, filename=None):
    return Parser(s, filename).parse()


def load(file):
    if not isinstance(file, str):
        return loads(file.read())

    with open(file) as f:
        return loads(f.read(), file)
