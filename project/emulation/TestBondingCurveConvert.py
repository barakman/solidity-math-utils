import sys
import random
import FixedPoint
import FloatPoint


MAX_WEIGHT = FloatPoint.MAX_WEIGHT = FixedPoint.BondingCurve.MAX_WEIGHT


def test(balance1, weight1, balance2, weight2, amount):
    fixedPoint = FixedPoint.convert(balance1, weight1, balance2, weight2, amount)
    floatPoint = FloatPoint.convert(balance1, weight1, balance2, weight2, amount)
    if fixedPoint > floatPoint:
        error = ['Implementation Error:']
        error.append(f'balance1   = {balance1  }')
        error.append(f'weight1    = {weight1   }')
        error.append(f'balance2   = {balance2  }')
        error.append(f'weight2    = {weight2   }')
        error.append(f'amount     = {amount    }')
        error.append(f'fixedPoint = {fixedPoint}')
        error.append(f'floatPoint = {floatPoint}')
        raise Exception('\n'.join(error))
    return fixedPoint / floatPoint


size = int(sys.argv[1] if len(sys.argv) > 1 else input('How many test-cases would you like to execute? '))


worstAccuracy = 1
numOfFailures = 0


for n in range(size):
    balance1 = random.randrange(1, 10 ** 23)
    weight1  = random.randrange(1, MAX_WEIGHT + 1)
    balance2 = random.randrange(1, 10 ** 23)
    weight2  = random.randrange(1, MAX_WEIGHT + 1)
    amount   = random.randrange(1, balance1 * 10)
    try:
        accuracy = test(balance1, weight1, balance2, weight2, amount)
        worstAccuracy = min(worstAccuracy, accuracy)
    except AssertionError as error:
        accuracy = 0
        numOfFailures += 1
    except Exception as error:
        print(error)
        break
    print(f'Test #{n}: accuracy = {accuracy:.24f}, worstAccuracy = {worstAccuracy:.24f}, numOfFailures = {numOfFailures}')
