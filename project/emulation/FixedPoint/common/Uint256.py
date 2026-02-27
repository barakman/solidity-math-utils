class uint256:
    max = 2 ** 256 - 1

def bitwiseNot(x):
    return uint256.max - x

def unsafeAdd(x, y):
    return (x + y) & uint256.max

def unsafeSub(x, y):
    return (x - y) & uint256.max

def unsafeMul(x, y):
    return (x * y) & uint256.max

def mulmod(x, y, z):
    return (x * y) % z
