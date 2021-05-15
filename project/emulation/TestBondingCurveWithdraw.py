import sys
import random
import FixedPoint
import FloatPoint


MAX_WEIGHT = FloatPoint.MAX_WEIGHT = FixedPoint.BondingCurve.MAX_WEIGHT


def test(supply, balance, weights, amount):
    fixedPoint = FixedPoint.withdraw(supply, balance, weights, amount)
    floatPoint = FloatPoint.withdraw(supply, balance, weights, amount)
    if fixedPoint > floatPoint:
        error = ['Implementation Error:']
        error.append('supply     = {}'.format(supply    ))
        error.append('balance    = {}'.format(balance   ))
        error.append('weights    = {}'.format(weights   ))
        error.append('amount     = {}'.format(amount    ))
        error.append('fixedPoint = {}'.format(fixedPoint))
        error.append('floatPoint = {}'.format(floatPoint))
        raise Exception('\n'.join(error))
    return fixedPoint / floatPoint


size = int(sys.argv[1] if len(sys.argv) > 1 else input('How many test-cases would you like to execute? '))


worstAccuracy = 1
numOfFailures = 0


for n in range(size):
    supply  = random.randrange(2, 10 ** 26)
    balance = random.randrange(1, 10 ** 23)
    weights = random.randrange(MAX_WEIGHT // 100, MAX_WEIGHT * 2 + 1)
    amount  = random.randrange(1, supply // 10)
    try:
        accuracy = test(supply, balance, weights, amount)
        worstAccuracy = min(worstAccuracy, accuracy)
    except AssertionError as error:
        accuracy = 0
        numOfFailures += 1
    except Exception as error:
        print(error)
        break
    print('Test #{}: accuracy = {:.24f}, worst accuracy = {:.24f}, num of failures = {}'.format(n, accuracy, worstAccuracy, numOfFailures))
