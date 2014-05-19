import os
import six
import codecs
from ast import Str, Num, Name, NodeTransformer, copy_location, parse

from meta.asttools import dump_python_source

from .constants import MAPPING, CHAR_MAPPING, CHAR_MAPPING_REVERSE, EXT_UNICODE, TYPES, TYPES_LOOLUP

encoding = six.text_type('# -*- coding: utf-8 -*-\n')


def get_boundary(value):
    for type_class, code in TYPES.items():
        if isinstance(value, type_class):
            return MAPPING[code]['unicode']
    raise ValueError('No boundary found for type {}'.format(type(value)))


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
    def doStr(self, node):
        return get_boundary(node.s), node.s

    def doNum(self, node):
        return get_boundary(node.n), six.text_type(node.n)

    def generic_visit(self, node):
        name = 'do{}'.format(type(node).__name__)
        node = NodeTransformer.generic_visit(self, node)
        if hasattr(self, name):
            boundary, value = getattr(self, name)(node)
            newstr = boundary
            for char in value:
                newstr += MAPPING[CHAR_MAPPING[char]]['unicode']
            newstr += boundary
            return copy_location(Name(id=newstr), node)
        return node


def from_file(filename):
    if filename.endswith('.pyc'):
        filename = filename[:-1]
    src = from_string(open(filename).read())
    filename = six.text_type('{}.{}.py').format(os.path.splitext(filename)[0], EXT_UNICODE)
    with open(filename, 'w') as fcompile:
        if six.PY2:
            src = src.encode('utf8')
        fcompile.write(src)
    return src


def from_string(string, filename=''):
    node = EmojiTransformer().visit(parse(string, filename))
    return encoding + dump_python_source(node)


def decompile(filename):
    def convert(type_class, buff):
        value = six.text_type('').join([CHAR_MAPPING_REVERSE[charcode] for charcode in buff])
        return repr(type_class(value))
    with codecs.open(filename, encoding='utf-8') as filein:
        mode, buff, src = None, [], encoding
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
