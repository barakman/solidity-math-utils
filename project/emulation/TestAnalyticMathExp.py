import sys
import random
import FixedPoint
import FloatPoint


def test(a, b):
    fixedPoint, factor = FixedPoint.exp(a, b)
    floatPoint = FloatPoint.exp(a, b, factor)
    if fixedPoint > floatPoint:
        error = ['Implementation Error:']
        error.append(f'a          = {a         }')
        error.append(f'b          = {b         }')
        error.append(f'fixedPoint = {fixedPoint}')
        error.append(f'floatPoint = {floatPoint}')
        raise Exception('\n'.join(error))
    return fixedPoint / floatPoint


size = int(sys.argv[1] if len(sys.argv) > 1 else input('How many test-cases would you like to execute? '))


worstAccuracy = 1
numOfFailures = 0


for n in range(size):
    a = random.randrange(10, 10 ** 26)
    b = random.randrange(a // 10, a * 10)
    try:
        accuracy = test(a, b)
        worstAccuracy = min(worstAccuracy, accuracy)
    except AssertionError as error:
        accuracy = 0
        numOfFailures += 1
    except Exception as error:
        print(error)
        break
    print(f'Test #{n}: accuracy = {accuracy:.24f}, worstAccuracy = {worstAccuracy:.24f}, numOfFailures = {numOfFailures}')
