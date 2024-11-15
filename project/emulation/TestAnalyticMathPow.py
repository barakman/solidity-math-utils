import random
import FixedPoint
import FloatPoint
import TestScheme


def getInput():
    a = random.randrange(2, 10 ** 26)
    b = random.randrange(1, a)
    c = random.randrange(2, 10 ** 26)
    d = random.randrange(c // 2, 10 ** 26)
    return dict(a=a, b=b, c=c, d=d)


def getOutput(a, b, c, d):
    fixedPoint, factor = FixedPoint.pow(a, b, c, d)
    floatPoint = FloatPoint.pow(a, b, c, d, factor)
    return dict(actual=fixedPoint, expected=floatPoint, success=fixedPoint<=floatPoint)


TestScheme.run(getInput, getOutput)