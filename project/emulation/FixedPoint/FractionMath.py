from .common.BuiltIn import *
from .common.Uint import *
from . import IntegralMath

MAX_EXP_BIT_LEN = 4;
MAX_EXP = 2 ** MAX_EXP_BIT_LEN - 1;
MAX_UINT128 = 2 ** 128 - 1;

'''
    @dev Compute the power of a given ratio
    
    @param baseN The ratio numerator
    @param baseD The ratio denominator
    @param exp   The exponentiation value
    @param fast  Opt for accuracy or performance
    
    @return The powered ratio numerator
    @return The powered ratio denominator
'''
def poweredRatio(baseN, baseD, exp, fast):
    require(exp <= MAX_EXP, "exp too large");

    safeRatio = mulRatio128 if fast else productRatio;

    ns = [0] * MAX_EXP_BIT_LEN;
    ds = [0] * MAX_EXP_BIT_LEN;

    (ns[0], ds[0]) = safeRatio(baseN, 1, baseD, 1);
    for i in range(len(bin(exp))):
        (ns[i + 1], ds[i + 1]) = safeRatio(ns[i], ns[i], ds[i], ds[i]);

    n = 1;
    d = 1;

    for i in range(len(bin(exp)) + 1):
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
    
    @param baseN The ratio numerator
    @param baseD The ratio denominator
    @param max   The maximum desired value
    
    @return The reduced ratio numerator
    @return The reduced ratio denominator
'''
def reducedRatio(baseN, baseD, max):
    if (baseN > max or baseD > max):
        return normalizedRatio(baseN, baseD, max);
    return (baseN, baseD);

'''
    @dev Compute a normalized ratio as `scale * n / (n + d)` and `scale * d / (n + d)`
    
    @param baseN The ratio numerator
    @param baseD The ratio denominator
    @param scale The desired scale
    
    @return The normalized ratio numerator
    @return The normalized ratio denominator
'''
def normalizedRatio(baseN, baseD, scale):
    if (baseN <= baseD):
        return estimatedRatio(baseN, baseD, scale);
    (d, n) = estimatedRatio(baseD, baseN, scale);
    return (n, d);

'''
    @dev Compute an estimated ratio as `scale * n / (n + d)` and `scale * d / (n + d)`, assuming that `n <= d`
    
    @param baseN The ratio numerator
    @param baseD The ratio denominator
    @param scale The desired scale
    
    @return The estimated ratio numerator
    @return The estimated ratio denominator
'''
def estimatedRatio(baseN, baseD, scale):
    maxN = MAX_VAL // scale; # `MAX_VAL >= scale` hence `maxN >= 1`
    if (maxN < baseN):
        # `maxN < baseN <= MAX_VAL` hence `maxN < MAX_VAL` hence `maxN + 1` is safe
        # `maxN + 1 >= 2` hence `baseN / (maxN + 1) < MAX_VAL` hence `baseN / (maxN + 1) + 1` is safe
        c = baseN // (maxN + 1) + 1;
        baseN //= c; # we can now safely compute `baseN * scale`
        baseD //= c;

    if (baseN != baseD):
        n = baseN * scale;
        d = unsafeAdd(baseN, baseD); # `baseN + baseD` can overflow
        if (d >= baseN):
            # `baseN + baseD` did not overflow
            x = IntegralMath.roundDiv(n, d); # we can now safely compute `scale - x`
            y = scale - x;
            return (x, y);
        if (n < baseD - (baseD - baseN) // 2):
            return (0, scale); # `baseN * scale < (baseN + baseD) / 2 < MAX_VAL < baseN + baseD`
        return (1, scale - 1); # `(baseN + baseD) / 2 < baseN * scale < MAX_VAL < baseN + baseD`
    return (scale // 2, scale - scale // 2); # reflect the fact that initially `baseN <= baseD`

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
