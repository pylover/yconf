class YConfException(Exception):
    def __init__(self, tok, title):
        super().__init__(
            f'{title}:{tok.line}:{tok.column}: {tok.kind}: {tok.value}')


class InvalidTokenError(YConfException):
    def __init__(self, tok):
        super().__init__(tok, 'Invalid token')


class ImproperIndentationError(YConfException):
    def __init__(self, tok):
        super().__init__(tok, 'Improper indentation')
