class Chain(list):
    def _eat(self, token):
        self.append(token.value)


class Meld(dict):
    def __getattr__(self, key):
        if key not in self:
            raise AttributeError(key)

        return self[key]

    def __setattr__(self, key, value):
        if isinstance(value, dict):
            super().__setitem__(key, Meld(value))
            return

        super().__setitem__(key, value)

    def __delattr__(self, key):
        if key not in self:
            raise AttributeError(key)

        del self[key]
