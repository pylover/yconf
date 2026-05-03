import re
import functools

from . import tokens as t
from .errors import InvalidTokenError


pat = functools.partial(re.compile, flags=re.I)
knowntokens = [
    (None, pat(r'^\s*#.*$')),
    (None, pat(r'^\s*$')),
    (t.Int, pat(r'^(?P<indent>\s*)(?P<key>[_\w]+):\s*(?P<value>\d*)\s*$')),
    (t.String, pat(r'^(?P<indent>\s*)(?P<key>[_\w]+):\s*(?P<value>.*)\s*$')),
]


def token_parse(line, lineno):
    for typ, pattern in knowntokens:
        m = pattern.match(line)
        if m:
            return typ(**m.groupdict()) if typ else None

    else:
        raise InvalidTokenError(line, lineno)


def tokenize(s):
    for i, line in enumerate(s.splitlines()):
        tok = token_parse(line, i + 1)
        if tok is None:
            continue

        yield tok
