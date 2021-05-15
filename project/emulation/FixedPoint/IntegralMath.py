'''
    @dev Compute the nearest integer to the quotient of `n / d`
'''
def roundDiv(n, d):
    return n // d + (n % d) // (d - d // 2);

'''
    @dev Compute the largest integer smaller than or equal to the binary logarithm of `n`
'''
def floorLog2(n):
    res = 0;

    if (n < 256):
        # at most 8 iterations
        while (n > 1):
            n >>= 1;
            res += 1;
    else:
        # exactly 8 iterations
        for s in [1 << (8 - 1 - k) for k in range(8)]:
            if (n >= 1 << s):
                n >>= s;
                res |= s;

    return res;

'''
    @dev Compute the largest integer smaller than or equal to the square root of `n`
'''
def floorSqrt(n):
    if (n > 0):
        x = n // 2 + 1;
        y = (x + n // x) // 2;
        while (x > y):
            x = y;
            y = (x + n // x) // 2;
        return x;
    return 0;

'''
    @dev Compute the smallest integer larger than or equal to the square root of `n`
'''
def ceilSqrt(n):
    x = floorSqrt(n);
    return x if x * x == n else x + 1;
