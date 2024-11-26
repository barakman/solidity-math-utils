from .common.BuiltIn import *
from .common.Uint256 import *
from . import IntegralMath

MAX_EXP_BIT_LEN = 4;
MAX_EXP = 2 ** MAX_EXP_BIT_LEN - 1;
MAX_UINT128 = 2 ** 128 - 1;

'''
    @dev Compute the power of a given ratio while opting for accuracy over performance
    
    @param n The ratio numerator
    @param d The ratio denominator
    @param exp The exponentiation value
    
    @return The powered ratio numerator
    @return The powered ratio denominator
'''
def poweredRatioExact(n, d, exp):
    return poweredRatio(n, d, exp, productRatio);

'''
    @dev Compute the power of a given ratio while opting for performance over accuracy
    
    @param n The ratio numerator
    @param d The ratio denominator
    @param exp The exponentiation value
    
    @return The powered ratio numerator
    @return The powered ratio denominator
'''
def poweredRatioQuick(n, d, exp):
    return poweredRatio(n, d, exp, mulRatio128);

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
    n = IntegralMath.minFactor(xn, yn);
    d = IntegralMath.minFactor(xd, yd);
    z = n if n > d else d;
    return (IntegralMath.mulDivC(xn, yn, z), IntegralMath.mulDivC(xd, yd, z));

'''
    @dev Reduce the components of a given ratio to fit up to a given threshold
    
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
    @dev Normalize the components of a given ratio to sum up to a given scale
    
    @param n The ratio numerator
    @param d The ratio denominator
    @param scale The desired scale
    
    @return The normalized ratio numerator
    @return The normalized ratio denominator
'''
def normalizedRatio(n, d, scale):
    if (n < d):
        (n, d) = estimatedRatio(n, d, scale);
    else:
        (d, n) = estimatedRatio(d, n, scale);
    return (n, d);

'''
    @dev Compute `scale * n / (n + d)` and `scale * d / (n + d)` assuming that `n < d`
    
    @param n The ratio numerator
    @param d The ratio denominator
    @param scale The desired scale
    
    @return The estimated ratio numerator
    @return The estimated ratio denominator
'''
def estimatedRatio(n, d, scale):
    if (n > MAX_VAL - d):
        x = unsafeAdd(n, d) + 1;
        y = IntegralMath.mulDivF(x, n // 2, n // 2 + d // 2);
        n -= y;
        d -= x - y;

    z = IntegralMath.mulDivR(scale, n, n + d);
    return(z, scale - z);

'''
    @dev Compute the power of a given ratio
    
    @param n The ratio numerator
    @param d The ratio denominator
    @param exp The exponentiation value
    @param safeRatio The computing function
    
    @return The powered ratio numerator
    @return The powered ratio denominator
'''
def poweredRatio(n, d, exp, safeRatio):
    require(exp <= MAX_EXP, "exp too large");

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
