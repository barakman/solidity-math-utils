import sys
import random
import FixedPoint
import FloatPoint


def test(a, b, c, d):
    p, q = FixedPoint.solve(a, b, c, d)
    a, b, c, d, p, q = [FloatPoint.Decimal(value) for value in [a, b, c, d, p, q]]
    return (p / q) * (a / b) ** (p / q) / (c / d)


size = int(sys.argv[1] if len(sys.argv) > 1 else input('How many test-cases would you like to execute? '))


minRatio = float('+inf')
maxRatio = float('-inf')
numOfFailures = 0


for n in range(size):
    a = random.randrange(1, 1000)
    b = random.randrange(1, 1000)
    c = random.randrange(1, 1000)
    d = random.randrange(1, 1000)
    try:
        ratio = test(a, b, c, d)
        minRatio = min(minRatio, ratio)
        maxRatio = max(maxRatio, ratio)
    except AssertionError as error:
        ratio = 0
        numOfFailures += 1
    print('Test #{}: ratio = {:.24f}, minRatio = {:.24f}, maxRatio = {:.24f}, num of failures = {}'.format(n, ratio, minRatio, maxRatio, numOfFailures))
