from . import AnalyticMath
from . import AdvancedMath
from . import BondingCurve
from . import DynamicCurve


def pow(a, b, c, d):
    return AnalyticMath.pow(a, b, c, d)


def log(a, b):
    return AnalyticMath.log(a, b)


def exp(a, b):
    return AnalyticMath.exp(a, b)


def solveExact(a, b, c, d):
    return AdvancedMath.solveExact(a, b, c, d)


def solveQuick(a, b, c, d):
    return AdvancedMath.solveQuick(a, b, c, d)


def lambertNegExact(x):
    return AdvancedMath.lambertNegExact(x)


def lambertPosExact(x):
    return AdvancedMath.lambertPosExact(x)


def lambertNegQuick(x):
    return AdvancedMath.lambertNegQuick(x)


def lambertPosQuick(x):
    return AdvancedMath.lambertPosQuick(x)


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


def equalizeExact(staked1, balance1, balance2, rate1, rate2):
    return DynamicCurve.equalizeExact(staked1, balance1, balance2, rate1, rate2)


def equalizeQuick(staked1, balance1, balance2, rate1, rate2):
    return DynamicCurve.equalizeQuick(staked1, balance1, balance2, rate1, rate2)
