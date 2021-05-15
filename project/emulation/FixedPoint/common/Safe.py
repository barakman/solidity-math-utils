'''
    @dev Revert on overflow
'''
def add(x, y):
    assert x + y < 2 ** 256
    return x + y;

'''
    @dev Revert on overflow
'''
def mul(x, y):
    assert x * y < 2 ** 256
    return x * y;

# Solidity built-in functions
def revert(msg = ""): assert False, msg
def require(cond, msg = ""): assert cond, msg
