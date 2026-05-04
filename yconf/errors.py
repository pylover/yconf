class YConfException(Exception):
    pass


class InvalidTokenError(Exception):
    def __init__(self, line, lineno, col):
        self.line = line
        self.lineno = lineno
        super().__init__(f'Invalid token:{lineno}:{col}: {line}')


class IndentationError(Exception):
    def __init__(self, token):
        self.token = token
        super().__init__(f'Improper indentation :{token.lineno}: {token}')
