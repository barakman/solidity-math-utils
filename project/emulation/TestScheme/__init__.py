import sys


def run(getInput, getOutput):
    tests = int(sys.argv[1] if len(sys.argv) > 1 else input('How many test-cases would you like to execute? '))

    minRatio = float('+inf')
    maxRatio = float('-inf')
    failures = 0

    for n in range(tests):
        input = getInput()
        try:
            output = getOutput(**input)
        except AssertionError:
            ratio = 0
            failures += 1
        else:
            if output['success']:
                ratio = output['actual'] / output['expected']
                minRatio = min(minRatio, ratio)
                maxRatio = max(maxRatio, ratio)
            else:
                printError(input, output)
                break
        print(f'Test #{n}: ratio = {ratio:.30f}, min = {minRatio:.30f}, max = {maxRatio:.30f}, failures = {failures}')


def printError(input, output):
    maxKeyLen = max(len(key) for key in input)
    error = [f'Implementation Error:']
    error.append(f'- Input:')
    error.extend(f'  - {key.ljust(maxKeyLen)} = {val}' for key, val in input.items())
    error.append(f'- Output:')
    error.append(f'  - Expected = {output['expected']:f}')
    error.append(f'  - Actual   = {output['actual']}')
    print('\n'.join(error))
