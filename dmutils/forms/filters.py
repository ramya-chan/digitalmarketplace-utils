'''
Functions that can be used as filters on WTForms fields.
'''


def strip_whitespace(value):
    if value is not None and hasattr(value, 'strip'):
        return value.strip()
    return value


def to_upper(value):
    if value is not None:
        return value.upper()
    return value
