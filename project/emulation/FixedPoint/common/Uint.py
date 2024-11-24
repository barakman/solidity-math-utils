MAX_UINT256 = (1 << 256) - 1

# reverts on overflow
def safeAdd(x, y):
    assert x + y <= MAX_UINT256
    return x + y

# does not revert on overflow
def unsafeAdd(x, y):
    return (x + y) & MAX_UINT256

# does not revert on overflow
def unsafeSub(x, y):
    return (x - y) & MAX_UINT256

# does not revert on overflow
def unsafeMul(x, y):
    return (x * y) & MAX_UINT256

# does not overflow
def mulModMax(x, y):
    return (x * y) % MAX_UINT256

# does not overflow
def mulMod(x, y, z):
    return (x * y) % z
