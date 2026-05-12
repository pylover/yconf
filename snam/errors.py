import os


class YConfException(Exception):
    def __init__(self, tok, title, filename=None):
        file = (filename if filename.startswith('/')
                else os.path.relpath(filename)) if filename else '(stream)'
        super().__init__(
            f'{file}:{tok.line}:{tok.column}: {title}: {tok}'
        )


class InvalidTokenError(YConfException):
    def __init__(self, tok, filename=None):
        super().__init__(tok, 'Invalid token', filename)


class ExpectedTokenError(YConfException):
    def __init__(self, tok, expected, filename=None):
        super().__init__(tok, f'Expected {expected}, found', filename)


class UnknownTagError(YConfException):
    def __init__(self, tok, filename=None):
        super().__init__(tok, 'Unknown', filename)


class IncludeMismatchError(YConfException):
    def __init__(self, tok, expectedtype, giventype, filename=None):
        super().__init__(
            tok,
            f'Trying to include `{giventype}` inside `{expectedtype}`',
            filename
        )
