def hex_len(n):
    length = len(hex(n))
    return 44 if 41 <= length <= 43 else length


def dec_str(value, max_value):
    return '{0:0{1}d}'.format(value, len(str(max_value)))


def hex_str(value, max_value):
    return '{0:#0{1}x}'.format(value, hex_len(max_value))
