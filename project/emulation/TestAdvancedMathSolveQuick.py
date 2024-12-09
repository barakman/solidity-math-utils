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
    x, y = FixedPoint.solveQuick(a, b, c, d)
    z = FloatPoint.solve(a, b, c, d, x, y)
    return 1, z, True


TestScheme.run(getInput, getOutput)