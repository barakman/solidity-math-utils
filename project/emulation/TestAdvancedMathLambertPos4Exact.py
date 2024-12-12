import random
import FixedPoint
import FloatPoint
import TestScheme


FIXED_1 = FixedPoint.AdvancedMath.FIXED_1
MIN_VAL = FixedPoint.AdvancedMath.LAMBERT_EXACT_LIMIT + 1
MAX_VAL = 2 ** 256


class Test(TestScheme.Run):
    def getInput(self):
        x = random.randrange(MIN_VAL, MAX_VAL)
        return dict(x=x)
    def getOutput(self, x):
        fixedPoint = FixedPoint.lambertPosExact(x)
        floatPoint = FloatPoint.lambert(+x, FIXED_1)
        return fixedPoint, floatPoint
    def isValid(self, ratio):
        return ratio <= 1


Test()