import sys


def run(getInput, getOutput):
    tests = int(sys.argv[1] if len(sys.argv) > 1 else input('How many test-cases would you like to execute? '))

    minRatio = float('+inf')
    maxRatio = float('-inf')
    failures = 0

    for test in range(tests):
        testInput = getInput()
        try:
            testOutput = getOutput(**testInput)
        except AssertionError:
            ratio = 0
            failures += 1
        else:
            if testOutput['success']:
                ratio = testOutput['actual'] / testOutput['expected']
                minRatio = min(minRatio, ratio)
                maxRatio = max(maxRatio, ratio)
            else:
                printError(testInput, testOutput)
                break
        print(f'Test #{test}: ratio = {ratio:.30f}, min = {minRatio:.30f}, max = {maxRatio:.30f}, failures = {failures}')


def printError(testInput, testOutput):
    maxKeyLen = max(len(key) for key in testInput)
    error = [f'Implementation Error:']
    error.append(f'- Input:')
    error.extend(f'  - {key.ljust(maxKeyLen)} = {val}' for key, val in testInput.items())
    error.append(f'- Output:')
    error.append(f'  - Expected = {testOutput['expected']:f}')
    error.append(f'  - Actual   = {testOutput['actual']}')
    print('\n'.join(error))
