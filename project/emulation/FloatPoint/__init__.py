from decimal import Decimal
from decimal import getcontext
from decimal import ROUND_HALF_DOWN


getcontext().prec = 100
getcontext().rounding = ROUND_HALF_DOWN


def pow(*args):
    a, b, c, d, factor = [Decimal(arg) for arg in args]
    return (a / b) ** (c / d) * factor


def log(*args):
    a, b, factor = [Decimal(arg) for arg in args]
    return (a / b).ln() * factor


def exp(*args):
    a, b, factor = [Decimal(arg) for arg in args]
    return (a / b).exp() * factor


def lambert(*args):
    x, factor = [Decimal(arg) for arg in args]
    return lambertRatio(x / factor) * factor


def solve(*args):
    a, b, c, d, x, y = [Decimal(arg) for arg in args]
    return (x / y) * (a / b) ** (x / y) / (c / d)


def buy(*args):
    supply, balance, weight, amount, max_weight = [Decimal(arg) for arg in args]
    return supply * ((1 + amount / balance) ** (weight / max_weight) - 1)


def sell(*args):
    supply, balance, weight, amount, max_weight = [Decimal(arg) for arg in args]
    return balance * (1 - (1 - amount / supply) ** (max_weight / weight))


def convert(*args):
    balance1, weight1, balance2, weight2, amount = [Decimal(arg) for arg in args]
    return balance2 * (1 - (balance1 / (balance1 + amount)) ** (weight1 / weight2))


def deposit(*args):
    supply, balance, weights, amount, max_weight = [Decimal(arg) for arg in args]
    return supply * ((amount / balance + 1) ** (weights / max_weight) - 1)


def withdraw(*args):
    supply, balance, weights, amount, max_weight = [Decimal(arg) for arg in args]
    return balance * (1 - ((supply - amount) / supply) ** (max_weight / weights))


def invest(*args):
    supply, balance, weights, amount, max_weight = [Decimal(arg) for arg in args]
    return balance * (((supply + amount) / supply) ** (max_weight / weights) - 1)


def lambertRatio(x):
    y = x if x < 1 else x.ln()
    for _ in range(8):
        e = y.exp()
        f = y * e
        if f == x: break
        y = (y * f + x) / (f + e)
    return y / x
