from decimal import Decimal
from decimal import getcontext
from decimal import ROUND_HALF_DOWN


getcontext().prec = 100
getcontext().rounding = ROUND_HALF_DOWN


one = Decimal(1)
parse = lambda args: [Decimal(arg) for arg in args]


def pow(*args):
    a, b, c, d = parse(args)
    return (a / b) ** (c / d)


def log(*args):
    a, b = parse(args)
    return (a / b).ln()


def exp(*args):
    a, b = parse(args)
    return (a / b).exp()


def solve(*args):
    a, b, c, d, x, y = parse(args)
    return (c / d) / (a / b) ** (x / y)


def lambert(*args):
    x, factor = parse(args)
    return lambertRatio(x / factor) * factor


def mintGain(*args):
    supply, balance, weightT, weightB, amount = parse(args)
    return supply * ((one + amount / balance) ** (weightT / weightB) - one)


def mintCost(*args):
    supply, balance, weightT, weightB, amount = parse(args)
    return balance * ((one + amount / supply) ** (weightB / weightT) - one)


def burnGain(*args):
    supply, balance, weightT, weightB, amount = parse(args)
    return balance * (one - (one - amount / supply) ** (weightB / weightT))


def burnCost(*args):
    supply, balance, weightT, weightB, amount = parse(args)
    return supply * (one - (one - amount / balance) ** (weightT / weightB))


def swapGain(*args):
    balance1, balance2, weight1, weight2, amount = parse(args)
    return balance2 * (one - (balance1 / (balance1 + amount)) ** (weight1 / weight2))


def swapCost(*args):
    balance1, balance2, weight1, weight2, amount = parse(args)
    return balance1 * ((balance2 / (balance2 - amount)) ** (weight2 / weight1) - one)


def equalize(*args):
    staked1, balance1, balance2, rate1, rate2, weight1, weight2 = parse(args)
    amount1 = staked1 - balance1
    amount2 = swapGain(balance1, balance2, weight1, weight2, amount1)
    return ((balance1 + amount1) * rate1) / ((balance2 - amount2) * rate2)


def lambertRatio(x):
    y = x if x < 1 else x.ln()
    for _ in range(8):
        e = y.exp()
        f = y * e
        if f == x: break
        y = (y * f + x) / (f + e)
    return y / x
