from . import AnalyticMath
from . import AdvancedMath
from . import BondingCurve
from . import DynamicCurve


[module.init() for module in [AnalyticMath, AdvancedMath, BondingCurve, DynamicCurve]]


def pow(a, b, c, d):
    return AnalyticMath.pow(a, b, c, d)


def log(a, b):
    return AnalyticMath.log(a, b)


def exp(a, b):
    return AnalyticMath.exp(a, b)


def solve(a, b, c, d):
    return AdvancedMath.solve(a, b, c, d)


def lambertNeg(x):
    return AdvancedMath.lambertNeg(x)


def lambertPos(x):
    return AdvancedMath.lambertPos(x)


def buy(supply, balance, weight, amount):
    return BondingCurve.buy(supply, balance, weight, amount)


def sell(supply, balance, weight, amount):
    return BondingCurve.sell(supply, balance, weight, amount)


def convert(balance1, weight1, balance2, weight2, amount):
    return BondingCurve.convert(balance1, weight1, balance2, weight2, amount)


def deposit(supply, balance, weights, amount):
    return BondingCurve.deposit(supply, balance, weights, amount)


def withdraw(supply, balance, weights, amount):
    return BondingCurve.withdraw(supply, balance, weights, amount)


def invest(supply, balance, weights, amount):
    return BondingCurve.invest(supply, balance, weights, amount)


def equalize(staked1, balance1, balance2, rate1, rate2):
    return DynamicCurve.equalize(staked1, balance1, balance2, rate1, rate2)


def fixedOne():
    return 1<<AnalyticMath.MAX_PRECISION


def lambertRange(n):
    return [1, AdvancedMath.LAMBERT_CONV_RADIUS+1, AdvancedMath.LAMBERT_POS2_MAXVAL+1, AdvancedMath.LAMBERT_POS3_MAXVAL+1][n-1:n+1]
