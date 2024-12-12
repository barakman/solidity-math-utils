import random
import FixedPoint
import FloatPoint
import TestScheme


MAX_WEIGHT = FixedPoint.BondingCurve.MAX_WEIGHT


class Test(TestScheme.Run):
    def getInput(self):
        supply  = random.randrange(2, 10 ** 26)
        balance = random.randrange(1, 10 ** 23)
        weights = random.randrange(MAX_WEIGHT // 100, MAX_WEIGHT * 2 + 1)
        amount  = random.randrange(1, balance * 10)
        return dict(supply=supply, balance=balance, weights=weights, amount=amount)
    def getOutput(self, supply, balance, weights, amount):
        fixedPoint = FixedPoint.deposit(supply, balance, weights, amount)
        floatPoint = FloatPoint.deposit(supply, balance, weights, amount, MAX_WEIGHT)
        return fixedPoint, floatPoint
    def isValid(self, ratio):
        return ratio <= 1


Test()