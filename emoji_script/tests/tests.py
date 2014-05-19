import sys
import os
import six
from glob import glob
from subprocess import Popen, PIPE, STDOUT

from nose_parameterized import parameterized

from ..utils import to_unicode, to_html, escape
from ..constants import MAPPING, EXT_UNICODE
from ..compiler import from_file, decompile

DEC_EXT = MAPPING['U+1F640']['unicode']


@parameterized([
    ('U+00A9', '\xA9', '&#x00A9;'),  # copyright
    ('U+231B', '\u231B', '&#x231B;'),  # hourglass
    ('U+1F300', '\U0001F300', '&#x1F300;'),  # cyclone
])
def test_conversion(code, text, html):
    try:
        text = six.text_type(text, 'ISO-8859-1')
    except (UnicodeDecodeError, TypeError):
        text = six.text_type(text)
    text = escape(text)
    assert to_unicode(code) == text, six.text_type('{!r} != {!r}').format(to_unicode(code), text)
    assert to_html(code) == html, six.text_type('{!r} != {!r}').format(to_html(code), html)


def test_compile():
    samples = os.path.join(os.path.dirname(__file__), 'samples', '*.py')
    for filename in glob(samples):
        if six.PY2:
            filename = filename.decode('utf8')
        if EXT_UNICODE in filename or DEC_EXT in filename:
            continue
        from_file(filename)


def test_decompile():
    samples = os.path.join(os.path.dirname(__file__), 'samples', '*.*.py')
    for filename in glob(samples):
        if six.PY2:
            filename = filename.decode('utf8')
        if not EXT_UNICODE in filename:
            continue
        with open(filename.replace(EXT_UNICODE, DEC_EXT), 'w') as outfile:
            outfile.write(decompile(filename))


def test_functional():
    samples = os.path.join(os.path.dirname(__file__), 'samples', '*.*.py')
    for filename in glob(samples):
        if six.PY2:
            filename = filename.decode('utf8')
        if EXT_UNICODE in filename:
            continue
        original = filename.replace(six.text_type('.') + DEC_EXT, '')
        out1, err1 = Popen([sys.executable, original], stdout=PIPE, stderr=PIPE).communicate()
        out2, err2 = Popen([sys.executable, filename], stdout=PIPE, stderr=PIPE).communicate()
        assert out1 == out2, out2
        assert err1 == err2, err2
