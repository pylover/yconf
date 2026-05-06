import re
from typing import NamedTuple, Iterable
from enum import StrEnum, auto


class Kind(StrEnum):
    COMMENT = auto()
    SKIP = auto()
    MISMATCH = auto()
    INDENT = auto()
    NEWLINE = auto()
    KEY = auto()
    DASH = auto()
    COLON = auto()
    STRING = auto()
    FLOAT = auto()


class Token(NamedTuple):
    type: Kind
    value: str
    line: int
    column: int


patterns = [
    (Kind.COMMENT, r'#.*'),
    (Kind.INDENT, r'^ +'),
    (Kind.DASH, r'-(?=\s|$)'),
    (Kind.COLON, r':'),
    (Kind.KEY, r'[\w.-]+(?=:)'),
    (Kind.FLOAT, r'\b(\.\d*|\d+\.\d+)\b'),
    (Kind.STRING, r'"[^"]*"|\'[^\']*\'|[^\s].*'),
    (Kind.SKIP,  r'[ \t]+'),
    (Kind.MISMATCH, r'.'),
    (Kind.NEWLINE, r'\n'),
    # (Kind.INT, r'\b\d+(\.\d*)?\b'),
]


def tokenize(code: str) -> Iterable[Token]:

    # compile into one master regex
    pattern = '|'.join(f'(?P<{kind}>{pat})' for kind, pat in patterns)
    tok_regex = re.compile(pattern, re.MULTILINE | re.IGNORECASE)
    line_num = 0
    line_start = 0

    # iterate through matches
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start

        if kind == Kind.NEWLINE:
            line_start = mo.end()
            yield Token(kind, value, line_num, column)
            line_num += 1
            continue

        if kind == Kind.SKIP or kind == Kind.COMMENT:
            continue

        if kind == Kind.MISMATCH:
            raise RuntimeError(f'{value!r} unexpected on line {line_num}')

        if kind == Kind.INDENT:
            value = len(value)

        if kind == Kind.STRING:
            value = value.strip('"\'')

        yield Token(kind, value, line_num, column)
