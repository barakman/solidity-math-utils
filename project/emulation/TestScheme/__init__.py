import sys


class Assert:
    LTE = +1
    GTE = -1
    NONE = 0


def run(getInput, getOutput):
    tests = int(sys.argv[1] if len(sys.argv) > 1 else input('How many tests would you like to execute? '))

    minRatio = float('+inf')
    maxRatio = float('-inf')
    failures = 0

    for test in range(tests):
        inputArgs = getInput()
        try:
            fixedPoint, floatPoint, sign = getOutput(**inputArgs)
        except AssertionError:
            ratio = 0
            failures += 1
        else:
            ratio = div(fixedPoint, floatPoint)
            if ratio ** sign <= 1:
                minRatio = min(minRatio, ratio)
                maxRatio = max(maxRatio, ratio)
            else:
                abort(inputArgs, fixedPoint, floatPoint)
                break
        print(f'Test #{test}: ratio = {ratio:.30f}, min = {minRatio:.30f}, max = {maxRatio:.30f}, failures = {failures}')


def div(fixedPoint, floatPoint):
    fixedPoint, floatPoint = [f if type(f) is tuple else (f, type(f)(1)) for f in [fixedPoint, floatPoint]]
    return (fixedPoint[0] * floatPoint[1]) / (fixedPoint[1] * floatPoint[0])


def abort(inputArgs, fixedPoint, floatPoint):
    maxKeyLen = max(len(key) for key in inputArgs)
    fixedPoint, floatPoint = [f if type(f) is tuple else [f] for f in [fixedPoint, floatPoint]]
    error = [f'Implementation Error:']
    error.append(f'- Input:')
    error.extend(f'  - {key.ljust(maxKeyLen)} = {val}' for key, val in inputArgs.items())
    error.append(f'- Output:')
    error.extend(f'  - fixedPoint[{ind}] = {val:d}' for ind, val in enumerate(fixedPoint))
    error.extend(f'  - floatPoint[{ind}] = {val:f}' for ind, val in enumerate(floatPoint))
    print('\n'.join(error))
