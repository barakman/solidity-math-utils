import random
import FixedPoint
import FloatPoint
import TestScheme


FIXED_1 = FixedPoint.AdvancedMath.FIXED_1
MAX_VAL = FixedPoint.AdvancedMath.LAMBERT_NEG1_MAXVAL + 1


def getInput():
    x = random.randrange(1, MAX_VAL)
    return dict(x=x)


def getOutput(x):
    fixedPoint = FixedPoint.lambertNegExact(x)
    floatPoint = FloatPoint.lambertNeg(x, FIXED_1)
    return dict(actual=fixedPoint, expected=floatPoint, success=fixedPoint<=floatPoint)


TestScheme.run(getInput, getOutput)