from decimal import Decimal
from decimal import getcontext
from decimal import ROUND_HALF_DOWN


getcontext().prec = 100
getcontext().rounding = ROUND_HALF_DOWN


def pow(a, b, c, d, factor):
    a, b, c, d, factor = [Decimal(value) for value in vars().values()]
    return (a / b) ** (c / d) * factor


def log(a, b, factor):
    a, b, factor = [Decimal(value) for value in vars().values()]
    return (a / b).ln() * factor


def exp(a, b, factor):
    a, b, factor = [Decimal(value) for value in vars().values()]
    return (a / b).exp() * factor


def lambert(x, factor):
    x, factor = [Decimal(value) for value in vars().values()]
    return lambertRatio(x / factor) * factor


def buy(supply, balance, weight, amount, max_weight):
    supply, balance, weight, amount, max_weight = [Decimal(value) for value in vars().values()]
    return supply * ((1 + amount / balance) ** (weight / max_weight) - 1)


def sell(supply, balance, weight, amount, max_weight):
    supply, balance, weight, amount, max_weight = [Decimal(value) for value in vars().values()]
    return balance * (1 - (1 - amount / supply) ** (max_weight / weight))


def convert(balance1, weight1, balance2, weight2, amount):
    balance1, weight1, balance2, weight2, amount = [Decimal(value) for value in vars().values()]
    return balance2 * (1 - (balance1 / (balance1 + amount)) ** (weight1 / weight2))


def deposit(supply, balance, weights, amount, max_weight):
    supply, balance, weights, amount, max_weight = [Decimal(value) for value in vars().values()]
    return supply * ((amount / balance + 1) ** (weights / max_weight) - 1)


def withdraw(supply, balance, weights, amount, max_weight):
    supply, balance, weights, amount, max_weight = [Decimal(value) for value in vars().values()]
    return balance * (1 - ((supply - amount) / supply) ** (max_weight / weights))


def invest(supply, balance, weights, amount, max_weight):
    supply, balance, weights, amount, max_weight = [Decimal(value) for value in vars().values()]
    return balance * (((supply + amount) / supply) ** (max_weight / weights) - 1)


def lambertRatio(x):
    y = x if x < 1 else x.ln()
    for _ in range(8):
        e = y.exp()
        f = y * e
        if f == x: break
        y = (y * f + x) / (f + e)
    return y / x
