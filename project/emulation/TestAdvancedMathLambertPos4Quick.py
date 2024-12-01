import random
import FixedPoint
import FloatPoint
import TestScheme


FIXED_1 = FixedPoint.AdvancedMath.FIXED_1
MIN_VAL = FixedPoint.AdvancedMath.LAMBERT_EXACT_LIMIT + 1
MAX_VAL = 2 ** 256


def getInput():
    x = random.randrange(MIN_VAL, MAX_VAL)
    return dict(x=x)


def getOutput(x):
    fixedPoint = FixedPoint.lambertPosQuick(x)
    floatPoint = FloatPoint.lambertPos(x, FIXED_1)
    return fixedPoint, floatPoint, True


TestScheme.run(getInput, getOutput)