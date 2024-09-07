import sys
import random
import FixedPoint
import FloatPoint


MAX_WEIGHT = FloatPoint.MAX_WEIGHT = FixedPoint.BondingCurve.MAX_WEIGHT


def test(supply, balance, weights, amount):
    fixedPoint = FixedPoint.deposit(supply, balance, weights, amount)
    floatPoint = FloatPoint.deposit(supply, balance, weights, amount)
    if fixedPoint > floatPoint:
        error = ['Implementation Error:']
        error.append(f'supply     = {supply    }')
        error.append(f'balance    = {balance   }')
        error.append(f'weights    = {weights   }')
        error.append(f'amount     = {amount    }')
        error.append(f'fixedPoint = {fixedPoint}')
        error.append(f'floatPoint = {floatPoint}')
        raise Exception('\n'.join(error))
    return fixedPoint / floatPoint


size = int(sys.argv[1] if len(sys.argv) > 1 else input('How many test-cases would you like to execute? '))


worstAccuracy = 1
numOfFailures = 0


for n in range(size):
    supply  = random.randrange(2, 10 ** 26)
    balance = random.randrange(1, 10 ** 23)
    weights = random.randrange(MAX_WEIGHT // 100, MAX_WEIGHT * 2 + 1)
    amount  = random.randrange(1, balance * 10)
    try:
        accuracy = test(supply, balance, weights, amount)
        worstAccuracy = min(worstAccuracy, accuracy)
    except AssertionError as error:
        accuracy = 0
        numOfFailures += 1
    except Exception as error:
        print(error)
        break
    print(f'Test #{n}: accuracy = {accuracy:.24f}, worstAccuracy = {worstAccuracy:.24f}, numOfFailures = {numOfFailures}')
