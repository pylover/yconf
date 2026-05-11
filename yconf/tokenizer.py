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


class Tokenizer:
    def __init__(self, text):
        self.text = text
        self.tokens = []

    def tokenize(self):
        lines = self.text.splitlines()
        for i, line in enumerate(lines):
            line_num = i

            # Skip empty lines or pure comments
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue

            # Indentation
            indent = len(line) - len(line.lstrip())
            self.tokens.append(Token(Kind.INDENT, indent, line_num, 0))

            # Content without trailing comment
            content = stripped
            if '#' in content:
                content = content.split('#', 1)[0].strip()

            if content.startswith('- '):
                self.tokens.append(Token(Kind.DASH, '-', line_num, indent))
                remaining = content[2:].strip()
                self._process_content(remaining, line_num, indent + 2)
            elif content == '-':
                 self.tokens.append(Token(Kind.DASH, '-', line_num, indent))
            else:
                self._process_content(content, line_num, indent)

            self.tokens.append(Token(Kind.NEWLINE, None, line_num, len(line)))

        self.tokens.append(Token(Kind.EOF, None, len(lines) + 1, 0))
        return self.tokens

    def _process_content(self, content, line_num, col_offset):
        if not content:
            return

        if ':' in content:
            # Match key: value or key: (next line value)
            # We look for ':' followed by optional whitespace
            match = re.match(r'^([^:]+):\s*(.*)$', content)
            if match:
                key, val = match.groups()
                self.tokens.append(Token(Kind.KEY, key.strip(), line_num, col_offset))
                self.tokens.append(Token(Kind.COLON, ':', line_num, col_offset + len(key)))
                if val.strip():
                    self.tokens.append(Token(Kind.VALUE, val.strip(), line_num, col_offset + len(key) + 2))
            else:
                # Fallback for weird cases
                self.tokens.append(Token(Kind.VALUE, content, line_num, col_offset))
        else:
            self.tokens.append(Token(Kind.VALUE, content, line_num, col_offset))
