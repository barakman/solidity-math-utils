import random
import FixedPoint
import FloatPoint
import TestScheme


def getInput():
    a = random.randrange(2, 10 ** 26)
    b = random.randrange(1, a)
    return dict(a=a, b=b)


def getOutput(a, b):
    fixedPoint = FixedPoint.log(a, b)
    floatPoint = FloatPoint.log(a, b)
    return fixedPoint, floatPoint


def isValid(ratio):
    return ratio <= 1


TestScheme.run(getInput, getOutput, isValid)