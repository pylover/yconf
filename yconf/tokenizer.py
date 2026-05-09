import re
from typing import NamedTuple
from enum import StrEnum, auto


class Kind(StrEnum):
    COMMENT = auto()
    SKIP = auto()
    INDENT = auto()
    NEWLINE = auto()
    KEY = auto()
    DASH = auto()
    STRING = auto()
    FLOAT = auto()
    INT = auto()
    TAG = auto()


patterns = [
    (Kind.COMMENT, r'#.*'),
    (Kind.INDENT, r'^ +'),
    (Kind.TAG, r'![\w-]+:'),
    (Kind.DASH, r'-(?=\s|$)'),
    (Kind.KEY, r'[\w-]+:'),
    (Kind.FLOAT, r'((?<=\s)|^)-?\d*\.\d+((?=\s)|$)'),
    (Kind.INT, r'((?<=\s)|^)-?\d+((?=\s)|$)'),
    (Kind.SKIP, r'[ \t]+'),
    (Kind.NEWLINE, r'\n'),
    (Kind.STRING, r'"[^"]*"|\'[^\']*\'|[^\s].*'),
]


class Token(NamedTuple):
    kind: Kind
    value: str
    line: int
    column: int

    def isliteral(self):
        return self.kind in (Kind.STRING, Kind.FLOAT, Kind.INT)

    def isindent(self):
        return self.kind == Kind.INDENT

    def iskey(self):
        return self.kind == Kind.KEY

    def isdash(self):
        return self.kind == Kind.DASH

    def isnewline(self):
        return self.kind == Kind.NEWLINE

    def istag(self):
        return self.kind == Kind.TAG

    @classmethod
    def new(cls, kind, value, line, column):
        if kind == Kind.INDENT:
            value = len(value)

        if kind == Kind.STRING:
            value = value.strip('"\'')

        if kind == Kind.FLOAT:
            value = float(value)

        if kind == Kind.INT:
            value = int(value)

        if kind == Kind.KEY:
            value = value[:-1]

        if kind == Kind.TAG:
            value = value[1:-1]

        return cls(kind, value, line, column)


class Tokenizer:
    def __init__(self, blob):
        pattern = '|'.join(f'(?P<{kind}>{pat})' for kind, pat in patterns)
        tok_regex = re.compile(pattern, re.MULTILINE | re.IGNORECASE)
        self._line = 0
        self._char = 0
        self._gen = tok_regex.finditer(blob)
        self._cache = []

    def _pop(self):
        while True:
            try:
                m = next(self._gen)
            except StopIteration:
                return None

            kind = m.lastgroup

            if kind == Kind.SKIP or kind == Kind.COMMENT:
                continue

            tok = Token.new(
                kind,
                m.group(),
                self._line,
                m.start() - self._char
            )

            if kind == Kind.NEWLINE:
                self._char = m.end()
                self._line += 1

            return tok

    def peek(self):
        if not self._cache:
            tok = self._pop()
            if tok is None:
                return None

            self._cache.append(tok)

            return tok

        return self._cache[0]

    def pop(self):
        if self._cache:
            return self._cache.pop(0)

        return self._pop()
