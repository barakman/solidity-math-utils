import sys


class Assert:
    non = lambda ratio: True
    lte = lambda ratio: ratio <= 1
    gte = lambda ratio: ratio >= 1


def run(getInput, getOutput):
    tests = int(sys.argv[1] if len(sys.argv) > 1 else input('How many tests would you like to execute? '))

    minRatio = float('+inf')
    maxRatio = float('-inf')
    failures = 0

    for test in range(tests):
        inputArgs = getInput()
        try:
            fixedPoint, floatPoint, assertion = getOutput(**inputArgs)
        except AssertionError:
            ratio = 0
            failures += 1
        else:
            ratio = div(fixedPoint, floatPoint)
            if assertion(ratio):
                minRatio = min(minRatio, ratio)
                maxRatio = max(maxRatio, ratio)
            else:
                abort(inputArgs, fixedPoint, floatPoint)
                break
        print(f'Test #{test}: ratio = {ratio:.40f}, min = {minRatio:.40f}, max = {maxRatio:.40f}, failures = {failures}')


def div(fixedPoint, floatPoint):
    return {
        int:   lambda fixedPoint, floatPoint: fixedPoint / floatPoint,
        tuple: lambda fixedPoint, floatPoint: fixedPoint[0] / (fixedPoint[1] * floatPoint)
    }[type(fixedPoint)](fixedPoint, floatPoint)


def abort(inputArgs, fixedPoint, floatPoint):
    maxKeyLen = max(len(key) for key in inputArgs)
    error = [f'Implementation Error:']
    error.append(f'- Input:')
    error.extend(f'  - {key.ljust(maxKeyLen)} = {val}' for key, val in inputArgs.items())
    error.append(f'- Output:')
    error.append(f'  - fixedPoint = {fixedPoint}')
    error.append(f'  - floatPoint = {floatPoint:f}')
    print('\n'.join(error))
