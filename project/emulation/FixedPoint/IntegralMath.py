from .common.BuiltIn import *
from .common.Uint import *

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
    return x if x ** 2 == n else x + 1;

'''
    @dev Compute the largest integer smaller than or equal to the cubic root of `n`
'''
def floorCbrt(n):
    x = 0;
    for y in [1 << k for k in range(255, -1, -3)]:
        x <<= 1;
        z = 3 * x * (x + 1) + 1;
        if (n // y >= z):
            n -= y * z;
            x += 1;
    return x;

'''
    @dev Compute the smallest integer larger than or equal to the cubic root of `n`
'''
def ceilCbrt(n):
    x = floorCbrt(n);
    return x if x ** 3 == n else x + 1;

'''
    @dev Compute the nearest integer to the quotient of `n` and `d` (or `n / d`)
'''
def roundDiv(n, d):
    return n // d + (n % d) // (d - d // 2);

'''
    @dev Compute the smallest integer `z` such that `x * y / z <= 2 ^ 256 - 1`
'''
def minFactor(x, y):
    (hi, lo) = mul512(x, y);
    return hi + 2 if hi > MAX_VAL - lo else hi + 1;
    # General:
    # - find the smallest integer `z` such that `x * y / z <= 2 ^ 256 - 1`
    # - the value of `x * y` is represented via `2 ^ 256 * hi + lo`
    # - the expression `~lo` is equivalent to `2 ^ 256 - 1 - lo`
    # 
    # Safety:
    # - if `x < 2 ^ 256 - 1` or `y < 2 ^ 256 - 1`
    #   then `hi < 2 ^ 256 - 2`
    #   hence neither `hi + 1` nor `hi + 2` overflows
    # - if `x = 2 ^ 256 - 1` and `y = 2 ^ 256 - 1`
    #   then `hi = 2 ^ 256 - 2 = ~lo`
    #   hence `hi + 1`, which does not overflow, is computed
    # 
    # Symbols:
    # - let `H` denote `hi`
    # - let `L` denote `lo`
    # - let `N` denote `2 ^ 256 - 1`
    # 
    # Inference:
    # `x * y / z <= 2 ^ 256 - 1`     <-->
    # `x * y / (2 ^ 256 - 1) <= z`   <-->
    # `((N + 1) * H + L) / N <= z`   <-->
    # `(N * H + H + L) / N <= z`     <-->
    # `H + (H + L) / N <= z`
    # 
    # Inference:
    # `0 <= H <= N && 0 <= L <= N`   <-->
    # `0 <= H + L <= N + N`          <-->
    # `0 <= H + L <= N * 2`          <-->
    # `0 <= (H + L) / N <= 2`
    # 
    # Inference:
    # - `0 = (H + L) / N` --> `H + L = 0` --> `x * y = 0` --> `z = 1 = H + 1`
    # - `0 < (H + L) / N <= 1` --> `H + (H + L) / N <= H + 1` --> `z = H + 1`
    # - `1 < (H + L) / N <= 2` --> `H + (H + L) / N <= H + 2` --> `z = H + 2`
    # 
    # Implementation:
    # - if `hi > ~lo`:
    #   `~L < H <= N`                         <-->
    #   `N - L < H <= N`                      <-->
    #   `N < H + L <= N + L`                  <-->
    #   `1 < (H + L) / N <= 2`                <-->
    #   `H + 1 < H + (H + L) / N <= H + 2`    <-->
    #   `z = H + 2`
    # - if `hi <= ~lo`:
    #   `H <= ~L`                             <-->
    #   `H <= N - L`                          <-->
    #   `H + L <= N`                          <-->
    #   `(H + L) / N <= 1`                    <-->
    #   `H + (H + L) / N <= H + 1`            <-->
    #   `z = H + 1`

'''
    @dev Compute the largest integer smaller than or equal to `x * y / z`
'''
def mulDivF(x, y, z):
    (xyh, xyl) = mul512(x, y);
    if (xyh == 0): # `x * y < 2 ^ 256`
        return xyl // z;
    if (xyh < z): # `x * y / z < 2 ^ 256`
        m = mulMod(x, y, z);            # `m = x * y % z`
        (nh, nl) = sub512(xyh, xyl, m); # `n = x * y - m` hence `n / z = floor(x * y / z)`
        if (nh == 0): # `n < 2 ^ 256`
            return nl // z;
        p = unsafeSub(0, z) & z; # `p` is the largest power of 2 which `z` is divisible by
        q = div512(nh, nl, p);   # `n` is divisible by `p` because `n` is divisible by `z` and `z` is divisible by `p`
        r = inv256(z // p);      # `z / p = 1 mod 2` hence `inverse(z / p) = 1 mod 2 ^ 256`
        return unsafeMul(q, r);  # `q * r = (n / p) * inverse(z / p) = n / z`
    revert(); # `x * y / z >= 2 ^ 256`

'''
    @dev Compute the smallest integer larger than or equal to `x * y / z`
'''
def mulDivC(x, y, z):
    w = mulDivF(x, y, z);
    if (mulMod(x, y, z) > 0):
        return safeAdd(w, 1);
    return w;

'''
    @dev Compute the nearest integer to `x * y / z`
'''
def mulDivR(x, y, z):
    w = mulDivF(x, y, z);
    if (mulMod(x, y, z) > (z - 1) // 2):
        return safeAdd(w, 1);
    return w;

'''
    @dev Compute the largest integer smaller than or equal to `(x * y) / (z * w)`
'''
def mulDivExF(x, y, z, w):
    (zwh, zwl) = mul512(z, w);
    if (zwh > 0):
        res = 0;
        (xyh, xyl) = mul512(x, y);
        if (xyh > zwh):
            xyhn = floorLog2(xyh);
            zwhn = floorLog2(zwh);
            while (xyhn > zwhn):
                n = xyhn - zwhn - 1;
                res += 1 << n; # set `res = res + 2 ^ n`
                (xyh, xyl) = sub512Ex(xyh, xyl, (zwh << n) | (zwl >> (256 - n)), zwl << n); # set `xy = xy - zw * 2 ^ n`
                xyhn = floorLog2(xyh);
        if (xyh > zwh or (xyh == zwh and xyl >= zwl)): # `xy >= zw`
            return res + 1;
        return res;
    return mulDivF(x, y, zwl);

'''
    @dev Compute the smallest integer larger than or equal to `(x * y) / (z * w)`
'''
def mulDivExC(x, y, z, w):
    v = mulDivExF(x, y, z, w);
    (xyh, xyl) = mul512(x, y);
    (zwh, zwl) = mul512(z, w);
    (vzwlh, vzwll) = mul512(v, zwl);
    if (xyh == v * zwh + vzwlh and xyl == vzwll):
        return v;
    return safeAdd(v, 1);

'''
    @dev Compute the value of `x * y`
'''
def mul512(x, y):
    p = mulModMax(x, y);
    q = unsafeMul(x, y);
    if (p >= q):
        return (p - q, q);
    return (unsafeSub(p, q) - 1, q);

'''
    @dev Compute the value of `2 ^ 256 * xh + xl - y`, where `2 ^ 256 * xh + xl >= y`
'''
def sub512(xh, xl, y):
    if (xl >= y):
        return (xh, xl - y);
    return (xh - 1, unsafeSub(xl, y));

'''
    @dev Compute the value of `(2 ^ 256 * xh + xl) / pow2n`, where `xl` is divisible by `pow2n`
'''
def div512(xh, xl, pow2n):
    pow2nInv = unsafeAdd(unsafeSub(0, pow2n) // pow2n, 1); # `1 << (256 - n)`
    return unsafeMul(xh, pow2nInv) | (xl // pow2n); # `(xh << (256 - n)) | (xl >> n)`

'''
    @dev Compute the inverse of `d` modulo `2 ^ 256`, where `d` is congruent to `1` modulo `2`
'''
def inv256(d):
    # approximate the root of `f(x) = 1 / x - d` using the newton–raphson convergence method
    x = 1;
    for i in range(8):
        x = unsafeMul(x, unsafeSub(2, unsafeMul(x, d))); # `x = x * (2 - x * d) mod 2 ^ 256`
    return x;

'''
    @dev Compute the value of `(2 ^ 256 * xh + xl) - (2 ^ 256 * yh + yl)`, where `2 ^ 256 * xh + xl >= 2 ^ 256 * yh + yl`
'''
def sub512Ex(xh, xl, yh, yl):
    if (xl >= yl):
        return (xh - yh, xl - yl);
    return (xh - yh - 1, unsafeSub(xl, yl));
