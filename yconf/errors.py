class InvalidTokenError(Exception):
    def __init__(self, token, lineno):
        self.token = token
        self.lineno = lineno
        super().__init__(f'Invalid token:{lineno}: {token}')
