def to_unicode(code):
    """
    Converts a code point (eg "U+1F446") to a unicode string (eg u"\U0001f446")
    """
    code = code[2:]
    value = int(code, 16)
    if value <= 65535:
        return unichr(value)
    return (r'\U' + code.zfill(8)).decode('unicode-escape')