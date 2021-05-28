BIT_LEN = 256
MAX_VAL = (1 << BIT_LEN) - 1

# reverts on overflow
def safeAdd(x, y):
    assert x + y <= MAX_VAL
    return x + y

# reverts on overflow
def safeMul(x, y):
    assert x * y <= MAX_VAL
    return x * y

# reverts on overflow
def safeAdd1(x):
    assert x < MAX_VAL
    return x + 1

# reverts on overflow
def safeShl1(x):
    assert x < BIT_LEN
    return 1 << x

# does not revert on overflow
def unsafeAdd(x, y):
    return (x + y) & MAX_VAL

# does not revert on overflow
def unsafeSub(x, y):
    return (x - y) & MAX_VAL

# does not revert on overflow
def unsafeMul(x, y):
    return (x * y) & MAX_VAL

# does not revert on overflow
def unsafeShl(x, y):
    return (x << y) & MAX_VAL

# does not overflow
def mulModMax(x, y):
    return (x * y) % MAX_VAL

# does not overflow
def mulMod(x, y, z):
    return (x * y) % z
