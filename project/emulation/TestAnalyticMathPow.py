import random
import FixedPoint
import FloatPoint
import TestScheme


class Test(TestScheme.Run):
    def getInput(self):
        a = random.randrange(2, 10 ** 26)
        b = random.randrange(1, a)
        c = random.randrange(2, 10 ** 26)
        d = random.randrange(c // 2, 10 ** 26)
        return dict(a=a, b=b, c=c, d=d)
    def getOutput(self, a, b, c, d):
        fixedPoint = FixedPoint.pow(a, b, c, d)
        floatPoint = FloatPoint.pow(a, b, c, d)
        return fixedPoint, floatPoint
    def isValid(self, ratio):
        return ratio <= 1


Test()