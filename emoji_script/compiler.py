import os
import six
import codecs
from ast import Str, Num, Name, NodeTransformer, copy_location, parse

from meta.asttools import dump_python_source, python_source, print_ast

from .constants import MAPPING, CHAR_MAPPING, CHAR_MAPPING_REVERSE, EXT_UNICODE, TYPES, TYPES_LOOLUP


def emojify(node, pad=False):
    if not type(node) in (Str, Num):
        return node
    value = node.s if type(node) == Str else node.n
    for type_class, code in TYPES.items():
        if isinstance(value, type_class):
            boundary = MAPPING[code]['unicode']
            break
    if type(node) == Num:
        value = six.text_type(value)
    newstr = boundary
    for char in value:
        newstr += MAPPING[CHAR_MAPPING[char]]['unicode']
        if pad:
            newstr += six.text_type(' ')
    newstr += boundary
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
    fname, ext = os.path.splitext(filename)[0], EXT_UNICODE
    with open(six.text_type('{}.{}.py').format(fname, ext), 'w') as fcompile:
        if six.PY2:
            src = src.encode('utf8')
        fcompile.write(src)
    return src


def from_string(string):
    transformer = EmojiTransformer()
    node = transformer.visit(parse(string))
    return dump_python_source(node)


def decompile(filename):
    def convert(type_class, buff):
        value = six.text_type('').join([CHAR_MAPPING_REVERSE[charcode] for charcode in buff])
        return repr(type_class(value))
    with codecs.open(filename, encoding='utf-8') as filein:
        mode, buff, src = None, [], six.text_type()
        while True:
            char = filein.read(1)
            if not char:
                break
            if char in TYPES_LOOLUP:
                if mode == char:
                    src += convert(TYPES_LOOLUP[char], buff)
                    mode, buff = None, []
                elif mode is None:
                    mode = char
            elif mode:
                buff.append(char)
            else:
                src += char
    return src
