import re
from enum import Enum, auto


KEYPATTERN = re.compile(r'^([^\{\}\[\]\(\)\'":]+):\s*(.*)$')
TAGPATTERN = re.compile(r'(\w+)(\s+)(.+)')
LINEPATTERN = re.compile(r'^.*$', re.MULTILINE)


class Kind(Enum):
    INDENT = auto()
    KEY = auto()
    VALUE = auto()
    DASH = auto()
    COLON = auto()
    EOF = auto()
    INCLUDE = auto()
    EXCLAM = auto()
    TAG = auto()


class Token:
    def __init__(self, kind, value, line, column):
        self.kind = kind
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f'{self.kind.name} `{self.value}`'

    def iseof(self):
        return self.kind == Kind.EOF

    def isindent(self):
        return self.kind == Kind.INDENT

    def isdash(self):
        return self.kind == Kind.DASH

    def iskey(self):
        return self.kind == Kind.KEY

    def isvalue(self):
        return self.kind == Kind.VALUE

    def isexclam(self):
        return self.kind == Kind.EXCLAM

    def iscolon(self):
        return self.kind == Kind.COLON


def _process_tag(content, lno, col):
    yield Token(Kind.EXCLAM, '!', lno, col)
    content = content[1:]
    if not content:
        return

    m = TAGPATTERN.match(content)
    if not m:
        # Fallback single word tag
        yield Token(Kind.TAG, content, lno, col)
        return

    tag, spaces, value = m.groups()
    yield Token(Kind.TAG, tag, lno, col + 1)
    yield Token(Kind.VALUE, value, lno, col + 1 + len(spaces) + len(tag))


def _process_value(content, lno, col):
    if content.startswith('!'):
        yield from _process_tag(content, lno, col)
    else:
        yield Token(Kind.VALUE, content, lno, col)


def _process_content(content, lno, col):
    if content == ':':
        yield Token(Kind.COLON, ':', lno, col)

    elif ':' in content:
        # match key: value or key: (next line value)
        # we look for ':' followed by optional whitespace
        m = KEYPATTERN.match(content)
        if m:
            key, val = m.groups()
            yield Token(Kind.KEY, key.strip(), lno, col)
            yield Token(Kind.COLON, ':', lno, col + len(key))
            val = val.strip()
            if val:
                yield from _process_value(val, lno, col + len(key) + 2)
        else:
            # Fallback for weird cases
            yield Token(Kind.VALUE, content, lno, col)
    else:
        yield from _process_value(content, lno, col)


def tokenize(text):
    lno = -1
    for m in LINEPATTERN.finditer(text):
        line = m.group()

        # line number
        lno += 1

        # Skip empty lines or pure comments
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue

        # Indentation
        indent = len(line) - len(line.lstrip())
        yield Token(Kind.INDENT, indent, lno, 0)

        # Content without trailing comment
        content = stripped
        if '#' in content:
            content = content.split('#', 1)[0].strip()

        if content.startswith('- '):
            yield Token(Kind.DASH, '-', lno, indent)
            remaining = content[2:].strip()
            yield from _process_content(remaining, lno, indent + 2)
        elif content == '-':
            yield Token(Kind.DASH, '-', lno, indent)
        elif content.startswith('!'):
            yield from _process_tag(content, lno, indent)
        else:
            yield from _process_content(content, lno, indent)

    yield Token(Kind.EOF, None, lno, 0)
