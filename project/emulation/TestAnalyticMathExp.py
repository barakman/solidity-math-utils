import random
import FixedPoint
import FloatPoint
import TestScheme


class Test(TestScheme.Run):
    def getInput(self):
        a = random.randrange(10, 10 ** 26)
        b = random.randrange(a // 10, a * 10)
        return dict(a=a, b=b)
    def getOutput(self, a, b):
        fixedPoint = FixedPoint.exp(a, b)
        floatPoint = FloatPoint.exp(a, b)
        return fixedPoint, floatPoint
    def isValid(self, ratio):
        return ratio <= 1


Test()