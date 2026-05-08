from .parser import loads


class Chain(list):
    pass


class Meld(dict):
    def __init__(self, data=None):
        if isinstance(data, str):
            data = loads(data)

        super().__init__(data or [])

    def __getattr__(self, key):
        if key not in self:
            raise AttributeError(key)

        return self[key]

    def __setattr__(self, key, value):
        super().__setitem__(key, value)

    def __delattr__(self, key):
        if key not in self:
            raise AttributeError(key)

        del self[key]

    def __ior__(self, other):
        if isinstance(other, str):
            other = loads(other)

        return super().__ior__(other)
