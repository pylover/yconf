import re
import abc
import functools


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


class Float(KeyValuePair):
    def __init__(self, value, **kw):
        super().__init__(value=float(value), **kw)


class String(KeyValuePair):
    pass


patt = functools.partial(re.compile, flags=re.I)
KEYPAT = r'^(?P<indent>\s*)(?P<key>[_\w]+):\s*'


def patt_keyval(valpat):
    return re.compile(
        fr'^{KEYPAT}(?P<value>{valpat})\s*$',
        re.I
    )


knowntokens = [
    (None, patt(r'^\s*#.*$')),
    (None, patt(r'^\s*$')),
    (Int, patt_keyval(r'\d*')),
    (Float, patt_keyval(r'[\.\d]*')),
    (String, patt_keyval(r'.*')),
]
