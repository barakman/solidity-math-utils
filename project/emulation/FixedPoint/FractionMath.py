from .common.BuiltIn import *
from .common.Uint import *
from . import IntegralMath

MAX_EXP_BIT_LEN = 4;
MAX_EXP = 2 ** MAX_EXP_BIT_LEN - 1;
MAX_UINT128 = 2 ** 128 - 1;

'''
    @dev Compute the power of a given ratio
    
    @param n The ratio numerator
    @param d The ratio denominator
    @param exp The exponentiation value
    @param fast Opt for performance over accuracy
    
    @return The powered ratio numerator
    @return The powered ratio denominator
'''
def poweredRatio(n, d, exp, fast):
    require(exp <= MAX_EXP, "exp too large");

    safeRatio = mulRatio128 if fast else productRatio;

    ns = [0] * MAX_EXP_BIT_LEN;
    ds = [0] * MAX_EXP_BIT_LEN;

    (ns[0], ds[0]) = safeRatio(n, 1, d, 1);
    for i in range(len(bin(exp)) - 3):
        (ns[i + 1], ds[i + 1]) = safeRatio(ns[i], ns[i], ds[i], ds[i]);

    n = 1;
    d = 1;

    for i in range(len(bin(exp)) - 2):
        if (((exp >> i) & 1) > 0):
            (n, d) = safeRatio(n, ns[i], d, ds[i]);

    return (n, d);

'''
    @dev Compute the product of two given ratios
    
    @param xn The 1st ratio numerator
    @param yn The 2nd ratio numerator
    @param xd The 1st ratio denominator
    @param yd The 2nd ratio denominator
    
    @return The product ratio numerator
    @return The product ratio denominator
'''
def productRatio(xn, yn, xd, yd):
    n = IntegralMath.mulDivC(xn, yn, MAX_VAL);
    d = IntegralMath.mulDivC(xd, yd, MAX_VAL);
    z = n if n > d else d;
    if (z > 1):
        return (IntegralMath.mulDivC(xn, yn, z), IntegralMath.mulDivC(xd, yd, z));
    return (xn * yn, xd * yd);

'''
    @dev Reduce the components of a given ratio
    
    @param n The ratio numerator
    @param d The ratio denominator
    @param max The maximum desired value
    
    @return The reduced ratio numerator
    @return The reduced ratio denominator
'''
def reducedRatio(n, d, max):
    scale = ((n if n > d else d) - 1) // max + 1;
    return (n // scale, d // scale);

'''
    @dev Compute a normalized ratio as `scale * n / (n + d)` and `scale * d / (n + d)`
    
    @param n The ratio numerator
    @param d The ratio denominator
    @param scale The desired scale
    
    @return The normalized ratio numerator
    @return The normalized ratio denominator
'''
def normalizedRatio(n, d, scale):
    if (n <= d):
        return estimatedRatio(n, d, scale);
    (d, n) = estimatedRatio(d, n, scale);
    return (n, d);

'''
    @dev Compute an estimated ratio as `scale * n / (n + d)` and `scale * d / (n + d)`, assuming that `n <= d`
    
    @param n The ratio numerator
    @param d The ratio denominator
    @param scale The desired scale
    
    @return The estimated ratio numerator
    @return The estimated ratio denominator
'''
def estimatedRatio(n, d, scale):
    maxN = MAX_VAL // scale; # `MAX_VAL >= scale` hence `maxN >= 1`
    if (maxN < n):
        # `maxN < n <= MAX_VAL` hence `maxN < MAX_VAL` hence `maxN + 1` is safe
        # `maxN + 1 >= 2` hence `n / (maxN + 1) < MAX_VAL` hence `n / (maxN + 1) + 1` is safe
        c = n // (maxN + 1) + 1;
        n //= c; # we can now safely compute `n * scale`
        d //= c;

    if (n != d):
        p = n * scale;
        q = unsafeAdd(n, d); # `n + d` can overflow
        if (q >= n):
            # `n + d` did not overflow
            r = IntegralMath.roundDiv(p, q);
            return (r, scale - r);
        if (p < d - (d - n) // 2):
            return (0, scale); # `n * scale < (n + d) / 2 < MAX_VAL < n + d`
        return (1, scale - 1); # `(n + d) / 2 < n * scale < MAX_VAL < n + d`
    return (scale // 2, scale - scale // 2); # reflect the fact that initially `n <= d`

'''
    @dev Compute the product of two ratios and reduce the components of the result to 128 bits,
    under the implicit assumption that the components of the product are not larger than 256 bits
    
    @param xn The 1st ratio numerator
    @param yn The 2nd ratio numerator
    @param xd The 1st ratio denominator
    @param yd The 2nd ratio denominator
    
    @return The product ratio numerator
    @return The product ratio denominator
'''
def mulRatio128(xn, yn, xd, yd):
    return reducedRatio(xn * yn, xd * yd, MAX_UINT128);
