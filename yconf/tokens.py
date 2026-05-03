import abc


class Token(abc.ABC):
    def __init__(self, indent):
        self.indent = len(indent)


class KeyValuePair(Token):
    def __init__(self, key, value, **kw):
        super().__init__(**kw)
        self.key = key
        self.value = value


class Int(KeyValuePair):
    def __init__(self, value, **kw):
        super().__init__(value=int(value), **kw)


class String(KeyValuePair):
    pass
