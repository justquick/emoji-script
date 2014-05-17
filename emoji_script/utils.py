import six


def escape(s):
    if '\\' in s:
        return s.encode('utf_8').decode('unicode-escape')
    return s


def to_unicode(code):
    """
    Converts a code point (eg "U+1F446") to a unicode string (eg u"\U0001f446")
    """
    code = code[2:].upper()
    value = int(code, 16)
    if value <= 65535:
        return six.unichr(value)
    return escape(six.text_type(r'\U' + code.zfill(8)).upper())


def to_html(code):
    """
    Converts a code point (eg "U+1F446") to an HTML entity (eg "&#x1F446;")
    """
    return six.text_type("&#x{0};".format(code[2:].upper()))
