import six

from nose_parameterized import parameterized

from .utils import to_unicode, to_html, escape
from .constants import MAPPING


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
    assert to_unicode(code) == text, '{0!r} != {1!r}'.format(to_unicode(code), text)
    assert to_html(code) == html, '{0!r} != {1!r}'.format(to_html(code), html)


def test_z_rainbow():
    six.print_()
    for code in MAPPING:
        six.print_(to_unicode(code), end='')
    six.print_()
