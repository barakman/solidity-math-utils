from decimal import Decimal
from decimal import getcontext
from decimal import ROUND_HALF_DOWN


getcontext().prec = 100
getcontext().rounding = ROUND_HALF_DOWN


DEC_TWO = Decimal(2)
MAX_VAL = 2 ** 256 - 1


def checked(x):
    assert 0 <= x <= MAX_VAL
    return x
