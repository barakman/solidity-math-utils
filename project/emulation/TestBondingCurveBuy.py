import random
import FixedPoint
import FloatPoint
import TestScheme


MAX_WEIGHT = FixedPoint.BondingCurve.MAX_WEIGHT


def getInput():
    supply  = random.randrange(2, 10 ** 26)
    balance = random.randrange(1, 10 ** 23)
    weight  = random.randrange(1, MAX_WEIGHT + 1)
    amount  = random.randrange(1, balance * 10)
    return dict(supply=supply, balance=balance, weight=weight, amount=amount)


def getOutput(supply, balance, weight, amount):
    fixedPoint = FixedPoint.buy(supply, balance, weight, amount)
    floatPoint = FloatPoint.buy(supply, balance, weight, amount, MAX_WEIGHT)
    return fixedPoint, floatPoint, fixedPoint <= floatPoint


TestScheme.run(getInput, getOutput)