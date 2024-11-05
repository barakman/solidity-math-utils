import sys
import random
import FixedPoint
import FloatPoint


FIXED_1 = FixedPoint.AdvancedMath.FIXED_1
MIN_VAL = FixedPoint.AdvancedMath.LAMBERT_NEG1_MAXVAL + 1
MAX_VAL = FixedPoint.AdvancedMath.LAMBERT_NEG2_MAXVAL + 1


def test(x):
    fixedPoint = FixedPoint.lambertNeg(x)
    floatPoint = FloatPoint.lambertNeg(x, FIXED_1)
    if fixedPoint > floatPoint:
        error = ['Implementation Error:']
        error.append(f'x          = {x         }')
        error.append(f'fixedPoint = {fixedPoint}')
        error.append(f'floatPoint = {floatPoint}')
        raise Exception('\n'.join(error))
    return fixedPoint / floatPoint


size = int(sys.argv[1] if len(sys.argv) > 1 else input('How many test-cases would you like to execute? '))


worstAccuracy = 1


for n in range(size):
    x = random.randrange(MIN_VAL, MAX_VAL)
    try:
        accuracy = test(x)
        worstAccuracy = min(worstAccuracy, accuracy)
    except Exception as error:
        print(error)
        break
    print(f'Test #{n}: accuracy = {accuracy:.24f}, worstAccuracy = {worstAccuracy:.24f}')
