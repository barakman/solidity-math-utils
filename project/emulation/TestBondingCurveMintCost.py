import random
import FixedPoint
import FloatPoint
import TestScheme


def getInput():
    supply  = random.randrange(1, 10 ** 26)
    balance = random.randrange(1, 10 ** 23)
    weight  = random.randrange(1, 1000001)
    weights = random.randrange(weight, 1000001)
    amount  = random.randrange(1, balance * 10)
    return dict(supply=supply, balance=balance, weight=weight, weights=weights, amount=amount)


def getOutput(supply, balance, weight, weights, amount):
    fixedPoint = FixedPoint.mintCost(supply, balance, weight, weights, amount)
    floatPoint = FloatPoint.mintCost(supply, balance, weight, weights, amount)
    return fixedPoint, floatPoint


def isValid(ratio):
    return True


TestScheme.run(getInput, getOutput, isValid)