import re
from enum import Enum, auto


class Kind(Enum):
    INDENT = auto()
    KEY = auto()
    VALUE = auto()
    DASH = auto()
    NEWLINE = auto()
    COLON = auto()
    EOF = auto()


class Token:
    def __init__(self, kind, value, line, column):
        self.kind = kind
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.kind.name}, {repr(self.value)})"

    def isnewline(self):
        return self.kind == Kind.NEWLINE

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

    def iscolon(self):
        return self.kind == Kind.COLON

def _process_content(content, lno, col_offset):
    if not content:
        return

    if ':' == content:
        yield Token(Kind.COLON, ':', lno, col_offset)

    elif ':' in content:
        # Match key: value or key: (next line value)
        # We look for ':' followed by optional whitespace
        match = re.match(r'^([^:]+):\s*(.*)$', content)
        if match:
            key, val = match.groups()
            yield Token(Kind.KEY, key.strip(), lno, col_offset)
            yield Token(Kind.COLON, ':', lno, col_offset + len(key))
            if val.strip():
                yield Token(Kind.VALUE, val.strip(), lno, col_offset + len(key) + 2)
        else:
            # Fallback for weird cases
            yield Token(Kind.VALUE, content, lno, col_offset)
    else:
        yield Token(Kind.VALUE, content, lno, col_offset)


def tokenize(text):
    lines = text.splitlines()
    for lno, line in enumerate(lines):

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
        else:
            yield from _process_content(content, lno, indent)

        yield Token(Kind.NEWLINE, None, lno, len(line))

    yield Token(Kind.EOF, None, len(lines) + 1, 0)
