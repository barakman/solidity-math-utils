import sys
import random
import FixedPoint
import FloatPoint


Decimal = FloatPoint.Decimal


def test(staked1, balance1, balance2, rate1, rate2):
    weights = FixedPoint.equalize(staked1, balance1, balance2, rate1, rate2)
    weight1 = weights[0];
    weight2 = weights[1];
    amount1 = staked1 - balance1
    amount2 = FloatPoint.convert(balance1, weight1, balance2, weight2, amount1)
    return Decimal((balance1 + amount1) * rate1 * weight2) / Decimal((balance2 - amount2) * rate2 * weight1)


size = int(sys.argv[1] if len(sys.argv) > 1 else input('How many test-cases would you like to execute? '))


minRatio = float('+inf')
maxRatio = float('-inf')
numOfFailures = 0


for n in range(size):
    rate     = random.randrange(10 ** 18, 10 ** 21)
    staked1  = random.randrange(10 ** 24, 10 ** 27)
    balance1 = staked1 * random.randrange(75, 150) // 100
    balance2 = staked1 * random.randrange(75, 150) // 100
    rate1    = rate * random.randrange(75, 150) // 100
    rate2    = rate * random.randrange(75, 150) // 100
    try:
        ratio = test(staked1, balance1, balance2, rate1, rate2)
        minRatio = min(minRatio, ratio)
        maxRatio = max(maxRatio, ratio)
    except AssertionError as error:
        ratio = 0
        numOfFailures += 1
    print('Test #{}: ratio = {:.24f}, minRatio = {:.24f}, maxRatio = {:.24f}, num of failures = {}'.format(n, ratio, minRatio, maxRatio, numOfFailures))
