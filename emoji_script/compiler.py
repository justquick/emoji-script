import six
from ast import Str, Num, Name, NodeTransformer, copy_location, parse

from meta.asttools import python_source

from .utils import to_unicode
from .constants import CHAR_MAPPING


def emojify(node):
    if not type(node) in (Str, Num):
        return node
    iterable = node.s if type(node) == Str else str(node.n)
    newstr = six.text_type()
    for char in iterable:
        newstr += to_unicode(CHAR_MAPPING[char]) + six.text_type(' ')
    return copy_location(Name(id=newstr), node)


class EmojiTransformer(NodeTransformer):
    def generic_visit(self, node):
        return emojify(NodeTransformer.generic_visit(self, node))


def main(filename):
    if filename.endswith('.pyc'):
        filename = filename[:-1]
    transformer = EmojiTransformer()
    node = transformer.visit(parse(open(filename).read(), filename))
    return python_source(node)
