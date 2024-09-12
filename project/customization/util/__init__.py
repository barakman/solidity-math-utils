def len_str(n):
    return len(str(n))


def len_hex(n):
    length = len(hex(n))
    return 42 if 39 <= length <= 41 else length
