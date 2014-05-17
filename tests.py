from utils import to_unicode
from constants import MAPPING


def test_copyright():
    assert to_unicode('U+00A9') == u'\xa9'


def test_hourglass():
    assert to_unicode('U+231B') == u'\u231b'


def test_cyclone():
    assert to_unicode('U+1F300') == u'\U0001f300'


def test_z_rainbow():
    for code in MAPPING:
        print to_unicode(code),
