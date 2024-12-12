import random
import FixedPoint
import FloatPoint
import TestScheme


FIXED_1 = FixedPoint.AdvancedMath.FIXED_1
MAX_VAL = FixedPoint.AdvancedMath.LAMBERT_NEG1_MAXVAL + 1


class Test(TestScheme.Run):
    def getInput(self):
        x = random.randrange(1, MAX_VAL)
        return dict(x=x)
    def getOutput(self, x):
        fixedPoint = FixedPoint.lambertNegExact(x)
        floatPoint = FloatPoint.lambert(-x, FIXED_1)
        return fixedPoint, floatPoint
    def isValid(self, ratio):
        return ratio <= 1


Test()