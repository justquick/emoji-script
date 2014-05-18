import six
from ast import Str, Num, Name, NodeTransformer, copy_location, parse

from meta.asttools import dump_python_source, python_source

from .utils import to_unicode
from .constants import CHAR_MAPPING, EXT_CODE


def emojify(node, pad=False):
    if not type(node) in (Str, Num):
        return node
    iterable = node.s if type(node) == Str else str(node.n)
    newstr = six.text_type()
    for char in iterable:
        newstr += to_unicode(CHAR_MAPPING[char])
        if pad:
            newstr += six.text_type(' ')
    return copy_location(Name(id=newstr), node)


class EmojiTransformer(NodeTransformer):
    def generic_visit(self, node):
        return emojify(NodeTransformer.generic_visit(self, node))


def from_file(filename):
    if filename.endswith('.pyc'):
        filename = filename[:-1]
    transformer = EmojiTransformer()
    node = transformer.visit(parse(open(filename).read(), filename))
    src = dump_python_source(node)
    with open(six.text_type('{}{}').format(filename, to_unicode(EXT_CODE)), 'w') as f:
        if six.PY2:
            src = src.encode('utf8')
        f.write(src)
    return src


def from_string(string):
    transformer = EmojiTransformer()
    node = transformer.visit(parse(string))
    return dump_python_source(node)
