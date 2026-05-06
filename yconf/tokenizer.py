import re
from typing import NamedTuple, Iterable
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


class Token(NamedTuple):
    kind: Kind
    value: str
    line: int
    column: int

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

        return cls(kind, value, line, column)


patterns = [
    (Kind.COMMENT, r'#.*'),
    (Kind.INDENT, r'^ +'),
    (Kind.DASH, r'-(?=\s|$)'),
    (Kind.KEY, r'[\w.-]+:'),
    (Kind.FLOAT, r'((?<=\s)|^)-?\d*\.\d+((?=\s)|$)'),
    (Kind.INT, r'((?<=\s)|^)-?\d+((?=\s)|$)'),
    (Kind.SKIP, r'[ \t]+'),
    (Kind.NEWLINE, r'\n'),
    (Kind.STRING, r'"[^"]*"|\'[^\']*\'|[^\s].*'),
]


def tokenize(code: str) -> Iterable[Token]:
    pattern = '|'.join(f'(?P<{kind}>{pat})' for kind, pat in patterns)
    tok_regex = re.compile(pattern, re.MULTILINE | re.IGNORECASE)
    line = 0
    charindex = 0

    for mo in tok_regex.finditer(code):
        kind = mo.lastgroup

        if kind == Kind.SKIP or kind == Kind.COMMENT:
            continue

        yield Token.new(kind, mo.group(), line, mo.start() - charindex)
        if kind == Kind.NEWLINE:
            charindex = mo.end()
            line += 1
