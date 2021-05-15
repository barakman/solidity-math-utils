import sys
import random
import FixedPoint
import FloatPoint


def test(x):
    fixedPoint = FixedPoint.lambertPos(x)
    floatPoint = FloatPoint.lambertPos(x, FixedPoint.fixedOne())
    return fixedPoint / floatPoint


size = int(sys.argv[1] if len(sys.argv) > 1 else input('How many test-cases would you like to execute? '))


minRatio = float('+inf')
maxRatio = float('-inf')


for n in range(size):
    x = random.randrange(*FixedPoint.lambertRange(3))
    ratio = test(x)
    minRatio = min(minRatio, ratio)
    maxRatio = max(maxRatio, ratio)
    print('Test #{}: ratio = {:.24f}, minRatio = {:.24f}, maxRatio = {:.24f}'.format(n, ratio, minRatio, maxRatio))
