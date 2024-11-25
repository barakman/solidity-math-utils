MAX_VAL = (1 << 256) - 1

# reverts on overflow
def safeAdd(x, y):
    assert x + y <= MAX_VAL
    return x + y

# does not revert on overflow
def unsafeAdd(x, y):
    return (x + y) & MAX_VAL

# does not revert on overflow
def unsafeSub(x, y):
    return (x - y) & MAX_VAL

# does not revert on overflow
def unsafeMul(x, y):
    return (x * y) & MAX_VAL

# does not overflow
def mulModMax(x, y):
    return (x * y) % MAX_VAL

# does not overflow
def mulMod(x, y, z):
    return (x * y) % z
