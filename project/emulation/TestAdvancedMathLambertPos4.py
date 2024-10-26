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
    if floatPoint > fixedPoint:
        error = ['Implementation Error:']
        error.append(f'x          = {x         }')
        error.append(f'fixedPoint = {fixedPoint}')
        error.append(f'floatPoint = {floatPoint}')
        raise Exception('\n'.join(error))
    return floatPoint / fixedPoint


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
