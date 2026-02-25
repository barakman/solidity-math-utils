import random
import FixedPoint
import FloatPoint
import TestScheme


def getInput():
    balance1 = random.randrange(1, 10 ** 23)
    balance2 = random.randrange(1, 10 ** 23)
    weight1  = random.randrange(1, 1000001)
    weight2  = random.randrange(1, 1000001)
    amount   = random.randrange(1, balance2)
    return dict(balance1=balance1, balance2=balance2, weight1=weight1, weight2=weight2, amount=amount)


def getOutput(balance1, balance2, weight1, weight2, amount):
    fixedPoint = FixedPoint.swapCost(balance1, balance2, weight1, weight2, amount)
    floatPoint = FloatPoint.swapCost(balance1, balance2, weight1, weight2, amount)
    return fixedPoint, floatPoint


def isValid(ratio):
    return ratio >= 1


TestScheme.run(getInput, getOutput, isValid)