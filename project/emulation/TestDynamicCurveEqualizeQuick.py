import random
import FixedPoint
import FloatPoint
import TestScheme


def getInput():
    rate     = random.randrange(10 ** 18, 10 ** 21)
    staked1  = random.randrange(10 ** 24, 10 ** 27)
    balance1 = staked1 * random.randrange(75, 150) // 100
    balance2 = staked1 * random.randrange(75, 150) // 100
    rate1    = rate * random.randrange(75, 150) // 100
    rate2    = rate * random.randrange(75, 150) // 100
    return dict(staked1=staked1, balance1=balance1, balance2=balance2, rate1=rate1, rate2=rate2)


def getOutput(staked1, balance1, balance2, rate1, rate2):
    fixedPoint = FixedPoint.equalizeQuick(staked1, balance1, balance2, rate1, rate2)
    floatPoint = FloatPoint.equalize(staked1, balance1, balance2, rate1, rate2, *fixedPoint)
    return fixedPoint, floatPoint


def isValid(ratio):
    return True


TestScheme.run(getInput, getOutput, isValid)