import random
import FixedPoint
import FloatPoint
import TestScheme


def getInput():
    supply  = random.randrange(2, 10 ** 26)
    balance = random.randrange(1, 10 ** 23)
    weightT = random.randrange(1, 1000001)
    weightB = random.randrange(weightT, 1000001)
    amount  = random.randrange(1, supply)
    return dict(supply=supply, balance=balance, weightT=weightT, weightB=weightB, amount=amount)


def getOutput(supply, balance, weightT, weightB, amount):
    fixedPoint = FixedPoint.burnGain(supply, balance, weightT, weightB, amount)
    floatPoint = FloatPoint.burnGain(supply, balance, weightT, weightB, amount)
    return fixedPoint, floatPoint


def isValid(ratio):
    return ratio <= 1


TestScheme.run(getInput, getOutput, isValid)