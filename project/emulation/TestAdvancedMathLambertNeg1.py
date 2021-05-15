import sys
import random
import FixedPoint
import FloatPoint


def test(x):
    fixedPoint = FixedPoint.lambertNeg(x)
    floatPoint = FloatPoint.lambertNeg(x, FixedPoint.fixedOne())
    if fixedPoint > floatPoint:
        error = ['Implementation Error:']
        error.append('x          = {}'.format(x         ))
        error.append('fixedPoint = {}'.format(fixedPoint))
        error.append('floatPoint = {}'.format(floatPoint))
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
    print('Test #{}: accuracy = {:.24f}, worst accuracy = {:.24f}'.format(n, accuracy, worstAccuracy))
