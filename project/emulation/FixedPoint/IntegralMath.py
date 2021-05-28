from .common import Uint

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

'''
    @dev Compute the largest integer smaller than or equal to `x * y / z`
'''
def mulDivF(x, y, z):
    (xyh, xyl) = mul512(x, y);
    if (xyh > 0):
        return div512(xyh, xyl, z);
    return xyl // z;

'''
    @dev Compute the smallest integer larger than or equal to `x * y / z`
'''
def mulDivC(x, y, z):
    w = mulDivF(x, y, z);
    if (Uint.mulMod(x, y, z) > 0):
        return Uint.safeAdd1(w);
    return w;

'''
    @dev Compute the value of `x * y`
'''
def mul512(x, y):
    p = Uint.mulModMax(x, y);
    q = Uint.unsafeMul(x, y);
    if (p >= q):
        return (p - q, q);
    return (Uint.unsafeSub(p, q) - 1, q);

'''
    @dev Compute the largest integer smaller than or equal to `(2 ^ 256 * xh + xl) / y`
'''
def div512(xh, xl, y):
    result = 0;
    length = 255 - floorLog2(y);
    while (xh > 0):
        bits = floorLog2(xh) + length;
        result = Uint.safeAdd(result, Uint.safeShl1(bits));
        (yh, yl) = shl512(y, bits);
        (xh, xl) = sub512(xh, xl, yh, yl);
    return Uint.safeAdd(result, xl // y);

'''
    @dev Compute the value of `x * 2 ^ y`
'''
def shl512(x, y):
    return (x >> (256 - y), Uint.unsafeShl(x, y));

'''
    @dev Compute the value of `2 ^ 256 * xh + xl - 2 ^ 256 * yh - yl`
'''
def sub512(xh, xl, yh, yl):
    if (xl >= yl):
        return (xh - yh, xl - yl);
    return (xh - yh - 1, Uint.unsafeSub(xl, yl));
