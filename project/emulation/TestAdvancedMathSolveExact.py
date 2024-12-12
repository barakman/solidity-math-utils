import random
import FixedPoint
import FloatPoint
import TestScheme


class Test(TestScheme.Run):
    def getInput(self):
        a = random.randrange(1, 1000)
        b = random.randrange(1, 1000)
        c = random.randrange(1, 1000)
        d = random.randrange(1, 1000)
        return dict(a=a, b=b, c=c, d=d)
    def getOutput(self, a, b, c, d):
        fixedPoint = FixedPoint.solveExact(a, b, c, d)
        floatPoint = FloatPoint.solve(a, b, c, d, *fixedPoint)
        return fixedPoint, floatPoint
    def isValid(self, ratio):
        return True


Test()