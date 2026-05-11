import io
import os
import copy
import subprocess

from .tokenizer import tokenize
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
            try:
                while len(self._tokq) <= index:
                    tok = next(self._tokgen)
                    if tok.isnewline():
                        continue

                    self._tokq.append(tok)

            except StopIteration:
                return None

        return self._tokq[index]

    def consume(self):
        if not self._tokq:
            self.peek()

        tok = self._tokq.pop(0)
        self._consumed.append(tok)
        return tok

    def _parse_listitem(self):
        self.consume() # INDENT
        self.consume() # DASH

        nxtok = self.peek()
        if nxtok.isvalue():
            return self._parse_primitive(self.consume().value)
        elif nxtok.isindent():
            # Nested structure
            return self._parse_block(nxtok.value - 1)
        elif nxtok.iskey():
             # Inline map after dash
             # same indent level conceptually
             return self._parse_block(self._consumed[-2].value)

        return None

    def _parse_mappingitem(self, indent):
        self.consume() # INDENT
        keytok = self.consume() # KEY
        self.consume() # COLON

        nxtok = self.peek()
        if nxtok.isvalue():
            return keytok.value, self._parse_primitive(self.consume().value)
        elif nxtok.isindent():
            # Nested
            if nxtok.value > indent:
                return keytok.value, self._parse_block(indent)
            else:
                return keytok.value, None

        elif nxtok.iseof():
            return keytok.value, None

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

    def _parse_block(self, min_indent):
        this = None

        while not self.peek().iseof():
            tok = self.peek()

            # Check indentation to see if we've exited this block
            indent = 0
            if tok.isindent():
                indent = tok.value
                if indent <= min_indent:
                    break
            else:
                # If no indent token, assume 0
                if min_indent >= 0:
                    break

            # Decide list or map
            # Advance to see what's after indent
            nxtok = self.peek(1)

            if nxtok and nxtok.isdash():
                if this is None:
                    this = []

                if not isinstance(this, list):
                    raise errors.InvalidTokenError(nxtok)

                this.append(self._parse_listitem())

            elif nxtok and nxtok.iskey():
                if this is None:
                    this = Meld()

                if not isinstance(this, dict):
                    raise errors.InvalidTokenError(nxtok)

                key, val = self._parse_mappingitem(indent)
                if key is not None:
                    this[key] = val
            else:
                if this is not None:
                    raise errors.InvalidTokenError(nxtok)

                # Just a scalar?
                if nxtok and nxtok.isvalue():
                    self.consume() # indent
                    return self._parse_primitive(self.consume().value)
                break

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
