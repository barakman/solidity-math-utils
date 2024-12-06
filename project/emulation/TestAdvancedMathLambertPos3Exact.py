import random
import FixedPoint
import FloatPoint
import TestScheme


FIXED_1 = FixedPoint.AdvancedMath.FIXED_1
MIN_VAL = FixedPoint.AdvancedMath.LAMBERT_POS2_MAXVAL + 1
MAX_VAL = FixedPoint.AdvancedMath.LAMBERT_EXACT_LIMIT + 1


def getInput():
    x = random.randrange(MIN_VAL, MAX_VAL)
    return dict(x=x)


def getOutput(x):
    fixedPoint = FixedPoint.lambertPosExact(x)
    floatPoint = FloatPoint.lambertPos(x, FIXED_1)
    return fixedPoint, floatPoint, fixedPoint <= floatPoint


TestScheme.run(getInput, getOutput)