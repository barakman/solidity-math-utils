import random
import FixedPoint
import FloatPoint
import TestScheme


MAX_WEIGHT = FixedPoint.BondingCurve.MAX_WEIGHT


def getInput():
    balance1 = random.randrange(1, 10 ** 23)
    weight1  = random.randrange(1, MAX_WEIGHT + 1)
    balance2 = random.randrange(1, 10 ** 23)
    weight2  = random.randrange(1, MAX_WEIGHT + 1)
    amount   = random.randrange(1, balance1 * 10)
    return dict(balance1=balance1, weight1=weight1, balance2=balance2, weight2=weight2, amount=amount)


def getOutput(balance1, weight1, balance2, weight2, amount):
    fixedPoint = FixedPoint.convert(balance1, weight1, balance2, weight2, amount)
    floatPoint = FloatPoint.convert(balance1, weight1, balance2, weight2, amount)
    return fixedPoint, floatPoint, TestScheme.Assert.lte


TestScheme.run(getInput, getOutput)