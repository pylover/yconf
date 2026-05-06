# import abc
#
# from .tokenizer import tokenize, Colon, Dash
# from .errors import IndentationError
#
#
# class Eater(abc.ABC):
#
#     @abc.abstractmethod
#     def _eat(self, token):
#         raise NotImplementedError()
#
#
# class Chain(list, Eater):
#     def _eat(self, token):
#         self.append(token.value)
#
#
# class Meld(dict, Eater):
#     def __init__(self, value):
#         if isinstance(value, str):
#             self._parse(value)
#
#     def __getattr__(self, key):
#         if key not in self:
#             raise AttributeError(key)
#
#         return self[key]
#
#     def __setattr__(self, key, value):
#         if isinstance(value, dict):
#             super().__setitem__(key, Meld(value))
#             return
#
#         super().__setitem__(key, value)
#
#     def __delattr__(self, key):
#         if key not in self:
#             raise AttributeError(key)
#
#         del self[key]
#
#     def _eat(self, token):
#         self[token.key] = token.value
