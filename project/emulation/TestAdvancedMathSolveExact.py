import random
import FixedPoint
import FloatPoint
import TestScheme


def getInput():
    a = random.randrange(1, 1000)
    b = random.randrange(1, 1000)
    c = random.randrange(1, 1000)
    d = random.randrange(1, 1000)
    return dict(a=a, b=b, c=c, d=d)


def getOutput(a, b, c, d):
    fixedPoint = FixedPoint.solveExact(a, b, c, d)
    floatPoint = FloatPoint.solve(a, b, c, d, *fixedPoint)
    return fixedPoint, floatPoint


def isValid(ratio):
    return True


TestScheme.run(getInput, getOutput, isValid)