import re
import abc
import functools

from .errors import InvalidTokenError


cipatt = functools.partial(re.compile, flags=re.I)


def bool_(value):
    return value[0] in 'ty'


knowntypes = [
    (float, cipatt(r'^\s*([+-]?[0-9]*\.[0-9]+)\s*$')),
    (int, cipatt(r'^\s*([+-]?\d+)\s*$')),
    (bool_, cipatt(r'^\s*(false|true|yes|no)\s*$')),
]


def parse_literal(value):
    for typ, pattern in knowntypes:
        m = pattern.match(value)
        if not m:
            continue

        return typ(m.group(1))

    # threat string
    return value.strip()


class Token(abc.ABC):
    def __init__(self, lineno, indent, value):
        self.lineno = lineno
        self.indent = indent
        self.value = parse_literal(value)


class Literal(Token):
    def __init__(self, lineno, indent, value):
        super().__init__(lineno, indent, value)


class Colon(Token):
    def __init__(self, lineno, indent, key, value):
        super().__init__(lineno, indent, value)
        self.key = key


class Dash(Token):
    def __init__(self, lineno, indent, value):
        super().__init__(lineno, indent, value)


knowntokens = [
    (Colon, cipatt(r'^([_\w]+):\s*(.*)\s*$')),
    (Dash, cipatt(r'^-\s*(.*)\s*$')),
]
COMMENT = re.compile(r'^\s*#.*$')
INDPAT = re.compile(r'^(\s*)(.*)\s*$')


def tokenize(s):
    for i, line in enumerate(s.splitlines()):
        if COMMENT.match(line):
            continue

        m = INDPAT.match(line)
        indent, line = m.groups()
        indent = len(indent)

        line = line.strip()
        if not line:
            continue

        for typ, pattern in knowntokens:
            m = pattern.match(line)
            if m:
                if typ:
                    yield typ(i + 1, indent, *m.groups())
                break

        else:
            # threat as literal
            yield Literal(i + 1, indent, line)
