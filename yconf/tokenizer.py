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
    COLON = auto()
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

        return cls(kind, value, line, column)


patterns = [
    (Kind.COMMENT, r'#.*'),
    (Kind.INDENT, r'^ +'),
    (Kind.DASH, r'-(?=\s|$)'),
    (Kind.COLON, r':'),
    (Kind.KEY, r'[\w.-]+(?=:)'),
    (Kind.FLOAT, r'((?<=\s)|^)-?\d*\.\d+((?=\s)|$)'),
    (Kind.INT, r'((?<=\s)|^)-?\d+((?=\s)|$)'),
    (Kind.SKIP, r'[ \t]+'),
    (Kind.NEWLINE, r'\n'),
    (Kind.STRING, r'"[^"]*"|\'[^\']*\'|[^\s].*'),
]


def tokenize(code: str) -> Iterable[Token]:
    pattern = '|'.join(f'(?P<{kind}>{pat})' for kind, pat in patterns)
    tok_regex = re.compile(pattern, re.MULTILINE | re.IGNORECASE)
    line_num = 0
    line_start = 0

    for mo in tok_regex.finditer(code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start

        if kind == Kind.SKIP or kind == Kind.COMMENT:
            continue

        if kind == Kind.NEWLINE:
            line_start = mo.end()
            yield Token.new(kind, value, line_num, column)
            line_num += 1
            continue

        yield Token.new(kind, value, line_num, column)
