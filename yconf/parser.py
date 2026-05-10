import io
import os
import copy
import subprocess

from . import tokenizer, errors


class Meld(dict):
    def __init__(self, data=None, root=None):
        if isinstance(data, str):
            data = loads(data)
        elif not isinstance(data, Meld):
            data = data or {}

        if root:
            super().__init__()
            self[root] = data
        else:
            super().__init__(data)

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

            if isinstance(mine, Meld) and isinstance(other, dict):
                mine |= other

            else:
                self[k] = other

        return self

    def __ilshift__(self, file):
        self |= load(file)
        return self

    def __irshift__(self, file):
        dump(self, file)
        return self


class Parser(tokenizer.Tokenizer):
    def __init__(self, s, filename=None):
        self._indentoffset = None
        self._indentsize = None
        self._filename = filename
        super().__init__(s)

    def _tokindent(self, tok):
        return tok.value - self._indentoffset

    def _isindentout(self, tok, indent):
        return self._tokindent(tok) < indent

    def _isindentin(self, tok, indent):
        return self._tokindent(tok) > indent

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

    def parse(self, indent=0):
        this = None
        while True:
            if (nxtok := self.peek()) is None:
                return this

            if nxtok.isindent():
                if self._indentoffset is None:
                    if indent == 0:
                        self._indentoffset = nxtok.value
                    else:
                        self._indentoffset = 0

                if self._isindentin(nxtok, indent):
                    if self._indentsize is None:
                        indent = self._indentsize = self._tokindent(nxtok)

                elif self._isindentout(nxtok, indent):
                    if indent == 0:
                        self.pop()
                        if self.peek():
                            raise errors.ImproperIndentationError(
                                self.peek(), self._filename
                            )
                    return this

                self.pop()
                if self.peek():
                    if indent < 0 or (
                        self._indentsize
                        and self._tokindent(nxtok) % self._indentsize
                    ):
                        raise errors.ImproperIndentationError(
                            self.peek(), self._filename
                        )

            if (tok := self.pop()) is None:
                return this

            if tok.isnewline():
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

                this[tok.value] = self.parse(indent + (self._indentsize or 1))

            elif tok.isdash():
                if this is None:
                    this = list()
                elif not isinstance(this, list):
                    raise errors.InvalidTokenError(tok, self._filename)

                this.append(self.parse(indent + (self._indentsize or 1)))

            elif tok.istag():
                this = self._tag(this, tok)


def loads(s, filename=None):
    return Parser(s, filename).parse()


def load(file):
    if not isinstance(file, str):
        return loads(file.read())

    with open(file) as f:
        return loads(f.read(), file)


def _dump(obj, file, indent=0, indentsize=2):
    if isinstance(obj, list):
        for v in obj:
            if isinstance(v, (dict, list)):
                file.write(f'{" " * indent}-\n')
                _dump(v, file, indent + indentsize, indentsize)
            else:
                file.write(f'{" " * indent}- {v}\n')

    elif isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                file.write(f'{" " * indent}{k}:\n')
                _dump(v, file, indent + indentsize, indentsize)
            else:
                file.write(f'{" " * indent}{k}: {v}\n')
    else:
        file.write(f'{obj}\n')


def dump(obj, file, indent=0, indentsize=2):
    if isinstance(file, str):
        with open(file, 'w') as f:
            _dump(obj, f, indent, indentsize)

    else:
        _dump(obj, file, indent, indentsize)


def dumps(obj, indent=0, indentsize=2):
    with io.StringIO() as file:
        dump(obj, file, indent, indentsize)
        return file.getvalue()
