from decimal import Decimal
from decimal import getcontext
from decimal import ROUND_HALF_DOWN


getcontext().prec = 100
getcontext().rounding = ROUND_HALF_DOWN


MAX_VAL = 2 ** 256 - 1
LOG_TWO = Decimal(2).ln()
INV_EXP = Decimal(-1).exp()


def two_pow(x):
    return Decimal(2) ** x


def checked(x):
    assert 0 <= x <= MAX_VAL
    return x


def bsearch(func, lo, hi, *args):
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        try:
            func(mid, *args)
            lo = mid
        except:
            hi = mid
    try:
        return func(hi, *args)
    except:
        return func(lo, *args)
