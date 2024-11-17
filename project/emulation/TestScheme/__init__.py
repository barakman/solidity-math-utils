import sys


def run(getInput, getOutput):
    tests = int(sys.argv[1] if len(sys.argv) > 1 else input('How many tests would you like to execute? '))

    minRatio = float('+inf')
    maxRatio = float('-inf')
    failures = 0

    for test in range(tests):
        inputArgs = getInput()
        try:
            fixedPoint, floatPoint, success = getOutput(**inputArgs)
        except AssertionError:
            ratio = 0
            failures += 1
        else:
            if success:
                ratio = fixedPoint / floatPoint
                minRatio = min(minRatio, ratio)
                maxRatio = max(maxRatio, ratio)
            else:
                printError(inputArgs, fixedPoint, floatPoint)
                break
        print(f'Test #{test}: ratio = {ratio:.30f}, min = {minRatio:.30f}, max = {maxRatio:.30f}, failures = {failures}')


def printError(inputArgs, fixedPoint, floatPoint):
    maxKeyLen = max(len(key) for key in inputArgs)
    error = [f'Implementation Error:']
    error.append(f'- Input:')
    error.extend(f'  - {key.ljust(maxKeyLen)} = {val}' for key, val in inputArgs.items())
    error.append(f'- Output:')
    error.append(f'  - fixedPoint = {fixedPoint}')
    error.append(f'  - floatPoint = {floatPoint:f}')
    print('\n'.join(error))
