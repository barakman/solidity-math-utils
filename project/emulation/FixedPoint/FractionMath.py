from .common.BuiltIn import *
from .common.Uint import *
from . import IntegralMath

MAX_EXP_BIT_LEN = 4;
MAX_EXP = 2 ** MAX_EXP_BIT_LEN - 1;
MAX_UINT128 = 2 ** 128 - 1;
MAX_UINT256 = 2 ** 256 - 1;

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
    n = IntegralMath.mulDivC(xn, yn, MAX_UINT256);
    d = IntegralMath.mulDivC(xd, yd, MAX_UINT256);
    z = n if n > d else d;
    if (z > 1):
        return (IntegralMath.mulDivC(xn, yn, z), IntegralMath.mulDivC(xd, yd, z));
    return (xn * yn, xd * yd);

'''
    @dev Compute the power of a given ratio
    
    @param baseN The ratio numerator
    @param baseD The ratio denominator
    @param exp   The exponentiation value
    
    @return The powered ratio numerator
    @return The powered ratio denominator
'''
def poweredRatio(baseN, baseD, exp):
    require(exp <= MAX_EXP, "exp too large");

    ns = [0] * MAX_EXP_BIT_LEN;
    ds = [0] * MAX_EXP_BIT_LEN;

    (ns[0], ds[0]) = reducedRatio(baseN, baseD, MAX_UINT128);
    for i in range(len(bin(exp))):
        (ns[i + 1], ds[i + 1]) = reducedRatio(ns[i] ** 2, ds[i] ** 2, MAX_UINT128);

    n = 1;
    d = 1;

    for i in range(len(bin(exp)) + 1):
        if (((exp >> i) & 1) > 0):
            (n, d) = reducedRatio(n * ns[i], d * ds[i], MAX_UINT128);

    return (n, d);

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
        return accurateRatio(baseN, baseD, scale);
    (d, n) = accurateRatio(baseD, baseN, scale);
    return (n, d);

'''
    @dev Compute a normalized ratio as `scale * n / (n + d)` and `scale * d / (n + d)`, assuming that `n <= d`
    
    @param baseN The ratio numerator
    @param baseD The ratio denominator
    @param scale The desired scale
    
    @return The normalized ratio numerator
    @return The normalized ratio denominator
'''
def accurateRatio(baseN, baseD, scale):
    maxVal = MAX_UINT256 // scale; # `MAX_UINT256 >= scale` hence `maxVal >= 1`
    if (maxVal < baseN):
        # `maxVal < baseN <= MAX_UINT256` hence `maxVal < MAX_UINT256` hence `maxVal + 1` is safe
        # `maxVal + 1 >= 2` hence `baseN / (maxVal + 1) < MAX_UINT256` hence `baseN / (maxVal + 1) + 1` is safe
        c = baseN // (maxVal + 1) + 1;
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
            return (0, scale); # `baseN * scale < (baseN + baseD) / 2 < MAX_UINT256 < baseN + baseD`
        return (1, scale - 1); # `(baseN + baseD) / 2 < baseN * scale < MAX_UINT256 < baseN + baseD`
    return (scale // 2, scale - scale // 2); # reflect the fact that `baseN <= baseD` at the beginning
