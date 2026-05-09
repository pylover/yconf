import os


class YConfException(Exception):
    def __init__(self, tok, title, filename=None):
        file = (filename if filename.startswith('/')
                else os.path.relpath(filename)) if filename else '(stream)'
        super().__init__(
            f'{file}:{tok.line}:{tok.column}: {title}: {tok.kind} '
            f'`{tok.value}`'
        )


class InvalidTokenError(YConfException):
    def __init__(self, tok, filename=None):
        super().__init__(tok, 'Invalid token', filename)


class ImproperIndentationError(YConfException):
    def __init__(self, tok, filename=None):
        super().__init__(tok, 'Improper indentation', filename)


class ExpectedTokenError(YConfException):
    def __init__(self, tok, expected, filename=None):
        super().__init__(tok, f'Expected {expected}', filename)


class UnknownTagError(YConfException):
    def __init__(self, tok, filename=None):
        super().__init__(tok, f'Unknown tag: {tok.value}', filename)
