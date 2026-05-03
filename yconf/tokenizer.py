
from . import tokens as t
from .errors import InvalidTokenError


def token_parse(line, lineno):
    for typ, pattern in t.knowntokens:
        m = pattern.match(line)
        if m:
            return typ(lineno=lineno, **m.groupdict()) if typ else None

    else:
        raise InvalidTokenError(line, lineno)


def tokenize(s):
    for i, line in enumerate(s.splitlines()):
        tok = token_parse(line, i + 1)
        if tok is None:
            continue

        yield tok
