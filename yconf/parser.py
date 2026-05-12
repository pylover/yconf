import io
import os
import copy
import subprocess

from .tokenizer import tokenize, Token, Kind
from . import errors


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


class Parser:
    def __init__(self, text, filename=None):
        self._filename = filename
        self._tokgen = tokenize(text)
        self._tokq = []
        self._consumed = []

    def peek(self, index=0):
        if len(self._tokq) <= index:
            while len(self._tokq) <= index:
                tok = next(self._tokgen)
                if tok.isnewline():
                    continue

                self._tokq.append(tok)

        return self._tokq[index]

    def consume(self, kind=None):
        if not self._tokq:
            self.peek()

        tok = self._tokq.pop(0)
        self._consumed.append(tok)
        while len(self._consumed) > 1:
            self._consumed.pop(0)

        if kind and tok.kind != kind:
            raise errors.ExpectedTokenError(tok, kind.name, self._filename)

        return tok

    def _parse_listitem(self):
        self.consume(Kind.INDENT)
        dash = self.consume(Kind.DASH)

        nxtok = self.peek()
        if nxtok.isindent():
            # Nested structure
            return self._parse_block(nxtok.value - 1)

        elif nxtok.iskey():
             # Inline map after dash
             # just ineject an indetat into the self._tokq
             self._tokq.insert(
                 0,
                 Token(Kind.INDENT, nxtok.column, nxtok.line, 0)
             )
             return self._parse_block(dash.column)

        elif nxtok.isexclam():
            return self._parse_tag()

        elif nxtok.iscolon():
            self.consume(Kind.COLON)
            return self._parse_block(dash.column)

        else:
            return self._parse_primitive(self.consume().value)

    def _parse_mappingitem(self, indent):
        self.consume(Kind.INDENT)
        keytok = self.consume(Kind.KEY)
        self.consume(Kind.COLON)

        nxtok = self.peek()
        if nxtok.isvalue():
            return keytok.value, self._parse_primitive(self.consume().value)

        elif nxtok.isexclam():
            val = self._parse_tag()
            return keytok.value, val

        elif nxtok.isindent() and nxtok.value > indent:
            # Nested
            return keytok.value, self._parse_block(indent)

        else:
            return keytok.value, None

    def _parse_primitive(self, val: str):
        # Strip quotes
        if (val.startswith('"') and val.endswith('"')) \
                or (val.startswith("'") and val.endswith("'")):
            return val[1:-1]

        v_lower = val.lower()
        if v_lower == 'true': return True
        if v_lower == 'false': return False
        if v_lower == 'null': return None

        try:
            if '.' in val: return float(val)
            return int(val)
        except ValueError:
            return val

    def _parse_tag(self):
        self.consume(Kind.EXCLAM)
        tagtok = self.consume(Kind.TAG)
        if tagtok.value == 'include':
            filenametok = self.consume(Kind.VALUE)
            return load(filenametok.value)

        if tagtok.value == 'env':
            return os.environ.get(self.consume(Kind.VALUE).value)

        if tagtok.value == 'shell':
            result = subprocess.run(
                self.consume(Kind.VALUE).value,
                shell=True,
                check=True,
                text=True,
                capture_output=True,
            )

            return result.stdout.strip()


        raise errors.UnknownTagError(tagtok, self._filename)

    def _parse_block(self, min_indent):
        this = None

        while True:
            tok = self.peek()
            if tok.iseof():
                return this

            # Check indentation to see if we've exited this block
            indent = tok.value
            if indent <= min_indent:
                break

            # Decide list or map
            # Advance to see what's after indent
            nxtok = self.peek(1)
            if nxtok.isdash():
                if this is None:
                    this = []

                if not isinstance(this, list):
                    raise errors.InvalidTokenError(nxtok, self._filename)

                this.append(self._parse_listitem())

            elif nxtok.iskey():
                if this is None:
                    this = Meld()

                if not isinstance(this, Meld):
                    raise errors.InvalidTokenError(nxtok, self._filename)

                key, val = self._parse_mappingitem(indent)
                if key is not None:
                    this[key] = val

            elif nxtok.isexclam():
                self.consume(Kind.INDENT)
                val = self._parse_tag()
                if this is None:
                    if isinstance(val, Meld):
                        this = val

                    elif isinstance(val, list):
                        this = val

                    else:
                        return val

                elif isinstance(this, Meld):
                    if isinstance(val, list):
                        raise errors.IncludeMismatchError(
                            self._consumed[-1],
                            Meld,
                            type(val),
                            self._filename
                        )

                    this |= val

                else:
                    # list
                    if not isinstance(val, list):
                        raise errors.IncludeMismatchError(
                            self._consumed[-1],
                            list,
                            type(val),
                            self._filename
                        )

                    this.extend(val)

            else:
                if this is not None:
                    raise errors.InvalidTokenError(nxtok, self._filename)

                # Just a scalar?
                if nxtok and nxtok.isvalue():
                    self.consume() # indent
                    return self._parse_primitive(self.consume().value)

                else:
                    raise errors.InvalidTokenError(nxtok, self._filename)

        return this

    def parse(self):
        # Initial empty YAML check
        if self.peek().iseof():
            return None

        return self._parse_block(-1)


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
