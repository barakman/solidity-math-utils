import random
import FixedPoint
import FloatPoint
import TestScheme


def getInput():
    a = random.randrange(2, 10 ** 26)
    b = random.randrange(1, a)
    return dict(a=a, b=b)


def getOutput(a, b):
    fixedPoint, factor = FixedPoint.log(a, b)
    floatPoint = FloatPoint.log(a, b, factor)
    return dict(actual=fixedPoint, expected=floatPoint, success=fixedPoint<=floatPoint)


TestScheme.run(getInput, getOutput)