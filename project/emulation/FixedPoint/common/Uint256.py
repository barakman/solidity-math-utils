MAX_VAL = (1 << 256) - 1

def unsafeAdd(x, y):
    return (x + y) & MAX_VAL

def unsafeSub(x, y):
    return (x - y) & MAX_VAL

def unsafeMul(x, y):
    return (x * y) & MAX_VAL

def mulModMax(x, y):
    return (x * y) % MAX_VAL
