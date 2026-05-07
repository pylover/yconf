class YConfException(Exception):
    pass


class InvalidTokenError(Exception):
    def __init__(self, tok):
        super().__init__(
            f'Invalid token:{tok.line}:{tok.column}: {tok.kind}: {tok.value}')


class IndentationError(Exception):
    def __init__(self, token):
        self.token = token
        super().__init__(f'Improper indentation :{token.lineno}: {token}')
