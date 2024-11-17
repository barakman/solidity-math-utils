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
    weights = FixedPoint.equalizeExact(staked1, balance1, balance2, rate1, rate2)
    weight1 = weights[0]
    weight2 = weights[1]
    amount1 = staked1 - balance1
    amount2 = FloatPoint.convert(balance1, weight1, balance2, weight2, amount1)
    return (balance1 + amount1) * rate1 * weight2, (balance2 - amount2) * rate2 * weight1, True


TestScheme.run(getInput, getOutput)