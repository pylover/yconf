import re
import abc
import functools


class Token(abc.ABC):
    def __init__(self, lineno, indent):
        self.lineno = lineno
        self.indent = len(indent)


class Key(Token, metaclass=abc.ABCMeta):
    def __init__(self, key, **kw):
        super().__init__(**kw)
        self.key = key


class KeyValue(Key):
    def __init__(self, value, **kw):
        super().__init__(**kw)
        self.value = value


class Int(KeyValue):
    def __init__(self, value, **kw):
        super().__init__(value=int(value), **kw)


class Float(KeyValue):
    def __init__(self, value, **kw):
        super().__init__(value=float(value), **kw)


class String(KeyValue):
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
    (Key, patt(fr'{KEYPAT}$')),
    (Int, patt_keyval(r'\d*')),
    (Float, patt_keyval(r'[\.\d]*')),
    (String, patt_keyval(r'.*')),
]
