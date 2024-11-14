import sys
import random
import FixedPoint
import FloatPoint


FIXED_1 = FixedPoint.AdvancedMath.FIXED_1
MIN_VAL = FixedPoint.AdvancedMath.LAMBERT_NEG1_MAXVAL + 1
MAX_VAL = FixedPoint.AdvancedMath.LAMBERT_NEG2_MAXVAL + 1


def test(x):
    fixedPoint = FixedPoint.lambertNegExact(x)
    floatPoint = FloatPoint.lambertNeg(x, FIXED_1)
    return fixedPoint / floatPoint


size = int(sys.argv[1] if len(sys.argv) > 1 else input('How many test-cases would you like to execute? '))


worstAccuracy = 1


for n in range(size):
    x = random.randrange(MIN_VAL, MAX_VAL)
    accuracy = test(x)
    assert accuracy <= 1, str(x)
    worstAccuracy = min(worstAccuracy, accuracy)
    print(f'Test #{n}: accuracy = {accuracy:.24f}, worstAccuracy = {worstAccuracy:.24f}')
