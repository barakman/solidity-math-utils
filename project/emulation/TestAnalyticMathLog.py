import random
import FixedPoint
import FloatPoint
import TestScheme


class Test(TestScheme.Run):
    def getInput(self):
        a = random.randrange(2, 10 ** 26)
        b = random.randrange(1, a)
        return dict(a=a, b=b)
    def getOutput(self, a, b):
        fixedPoint = FixedPoint.log(a, b)
        floatPoint = FloatPoint.log(a, b)
        return fixedPoint, floatPoint
    def isValid(self, ratio):
        return ratio <= 1


Test()