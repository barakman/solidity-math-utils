import sys
import random
import FixedPoint
import FloatPoint


def test(x):
    fixedPoint = FixedPoint.lambertNeg(x)
    floatPoint = FloatPoint.lambertNeg(x, FixedPoint.fixedOne())
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
    x = random.randrange(*FixedPoint.lambertRange(1))
    try:
        accuracy = test(x)
        worstAccuracy = min(worstAccuracy, accuracy)
    except Exception as error:
        print(error)
        break
    print(f'Test #{n}: accuracy = {accuracy:.24f}, worstAccuracy = {worstAccuracy:.24f}')
