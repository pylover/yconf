__version__ = '0.1.0a'


from .errors import InvalidTokenError, ImproperIndentationError
from .parser import Parser
from .models import Meld, Chain


def loads(s):
    return Parser(s).parse()
