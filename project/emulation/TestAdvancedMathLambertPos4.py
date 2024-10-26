import sys
import random
import FixedPoint
import FloatPoint


FIXED_1 = FixedPoint.AdvancedMath.FIXED_1
MIN_VAL = FixedPoint.AdvancedMath.LAMBERT_POS3_MAXVAL + 1
MAX_VAL = FixedPoint.AdvancedMath.LAMBERT_POS3_MAXVAL * 100 + 1


def test(x):
    fixedPoint = FixedPoint.lambertPos(x)
    floatPoint = FloatPoint.lambertPos(x, FIXED_1)
    return fixedPoint / floatPoint


size = int(sys.argv[1] if len(sys.argv) > 1 else input('How many test-cases would you like to execute? '))


minRatio = float('+inf')
maxRatio = float('-inf')


for n in range(size):
    x = random.randrange(MIN_VAL, MAX_VAL)
    ratio = test(x)
    minRatio = min(minRatio, ratio)
    maxRatio = max(maxRatio, ratio)
    print(f'Test #{n}: ratio = {ratio:.24f}, minRatio = {minRatio:.24f}, maxRatio = {maxRatio:.24f}')
