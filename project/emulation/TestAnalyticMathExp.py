import random
import FixedPoint
import FloatPoint
import TestScheme


def getInput():
    a = random.randrange(10, 10 ** 26)
    b = random.randrange(a // 10, a * 10)
    return dict(a=a, b=b)


def getOutput(a, b):
    fixedPoint = FixedPoint.exp(a, b)
    floatPoint = FloatPoint.exp(a, b)
    return fixedPoint, floatPoint, TestScheme.Assert.lte


TestScheme.run(getInput, getOutput)