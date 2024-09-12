def len_str(n):
    return len(str(n))


def len_hex(n):
    length = len(hex(n))
    return 44 if 41 <= length <= 43 else length
