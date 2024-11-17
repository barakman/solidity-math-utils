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
    p, q = FixedPoint.solveExact(a, b, c, d)
    a, b, c, d, p, q = [FloatPoint.Decimal(value) for value in [a, b, c, d, p, q]]
    return (p / q) * (a / b) ** (p / q), (c / d), True


TestScheme.run(getInput, getOutput)