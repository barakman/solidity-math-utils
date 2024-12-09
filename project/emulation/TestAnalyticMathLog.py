import random
import FixedPoint
import FloatPoint
import TestScheme


def getInput():
    a = random.randrange(2, 10 ** 26)
    b = random.randrange(1, a)
    return dict(a=a, b=b)


def getOutput(a, b):
    fixedPointN, fixedPointD = FixedPoint.log(a, b)
    floatPoint = FloatPoint.log(a, b) * fixedPointD
    return fixedPointN, floatPoint, fixedPointN <= floatPoint


TestScheme.run(getInput, getOutput)