class YConfException(Exception):
    def __init__(self, tok, title):
        super().__init__(
            f'(stream):{tok.line}:{tok.column}: {title}: {tok.kind} '
            f'`{tok.value}`'
        )


class InvalidTokenError(YConfException):
    def __init__(self, tok):
        super().__init__(tok, 'Invalid token')


class ImproperIndentationError(YConfException):
    def __init__(self, tok):
        super().__init__(tok, 'Improper indentation')


class ExpectedTokenError(YConfException):
    def __init__(self, tok, expected):
        super().__init__(tok, f'Expected {expected}')


class UnknownTagError(YConfException):
    def __init__(self, tok):
        super().__init__(tok, f'Unknown tag: {tok.value}')
