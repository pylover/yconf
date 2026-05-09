import copy

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

    def __ior__(self, data):
        if isinstance(data, str):
            data = loads(data)
        elif not isinstance(data, dict):
            raise TypeError(
                'Only dict and or it\'s subclasses are allowed, '
                f'given: {type(data)}')
        else:
            data = copy.deepcopy(data)

        for k, other in data.items():
            mine = self.get(k)

            if isinstance(mine, Meld):
                mine |= other

            else:
                self[k] = other

        return self
