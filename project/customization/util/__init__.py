def hex_len(n):
    return 44 if 41 <= len(hex(n)) <= 44 else len(hex(n))


def dec_str(value, max_value):
    return '{0:0{1}d}'.format(value, len(str(max_value)))


def hex_str(value, max_value):
    return '{0:#0{1}x}'.format(value, hex_len(max_value))
