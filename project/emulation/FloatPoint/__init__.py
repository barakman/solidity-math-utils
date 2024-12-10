from decimal import Decimal
from decimal import getcontext
from decimal import ROUND_HALF_DOWN


getcontext().prec = 100
getcontext().rounding = ROUND_HALF_DOWN


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
    return (c / d), (a / b) ** (x / y)


def lambert(*args):
    x, factor = parse(args)
    return lambertRatio(x / factor) * factor


def buy(*args):
    supply, balance, weight, amount, max_weight = parse(args)
    return supply * ((1 + amount / balance) ** (weight / max_weight) - 1)


def sell(*args):
    supply, balance, weight, amount, max_weight = parse(args)
    return balance * (1 - (1 - amount / supply) ** (max_weight / weight))


def convert(*args):
    balance1, weight1, balance2, weight2, amount = parse(args)
    return balance2 * (1 - (balance1 / (balance1 + amount)) ** (weight1 / weight2))


def deposit(*args):
    supply, balance, weights, amount, max_weight = parse(args)
    return supply * ((amount / balance + 1) ** (weights / max_weight) - 1)


def withdraw(*args):
    supply, balance, weights, amount, max_weight = parse(args)
    return balance * (1 - ((supply - amount) / supply) ** (max_weight / weights))


def invest(*args):
    supply, balance, weights, amount, max_weight = parse(args)
    return balance * (((supply + amount) / supply) ** (max_weight / weights) - 1)


def equalize(*args):
    staked1, balance1, balance2, rate1, rate2, weight1, weight2 = parse(args)
    amount1 = staked1 - balance1
    amount2 = convert(balance1, weight1, balance2, weight2, amount1)
    return (balance1 + amount1) * rate1, (balance2 - amount2) * rate2


def lambertRatio(x):
    y = x if x < 1 else x.ln()
    for _ in range(8):
        e = y.exp()
        f = y * e
        if f == x: break
        y = (y * f + x) / (f + e)
    return y / x
