from core import Decimal
from core import MAX_VAL
from core import INV_EXP
from core import checked
from core import bsearch
from math import factorial


def lambertExactLimit(fixed1):
    return bsearch(lambertPosExact, fixed1, MAX_VAL, fixed1)


def lambertNeg1Terms(fixed1, maxNumOfTerms, sizeN, sizeD, numOfSamples):
    maxVal, _ = lambertNegLimits(fixed1, sizeN, sizeD, numOfSamples)
    return bsearch(lambertNeg1, 0, maxNumOfTerms, maxVal, fixed1)


def lambertPos1Terms(fixed1, maxNumOfTerms, sizeN, sizeD, numOfSamples):
    maxVal, _ = lambertPosLimits(fixed1, sizeN, sizeD, numOfSamples)
    return bsearch(lambertPos1, 0, maxNumOfTerms, maxVal, fixed1)


def lambertNegParams(fixed1, sizeN, sizeD, numOfSamples):
    bgn, end = lambertNegLimits(fixed1, sizeN, sizeD, numOfSamples)
    return bgn, end, *lambertLutParams(fixed1, numOfSamples, bgn, end, -1)


def lambertPosParams(fixed1, sizeN, sizeD, numOfSamples):
    bgn, end = lambertPosLimits(fixed1, sizeN, sizeD, numOfSamples)
    return bgn, end, *lambertLutParams(fixed1, numOfSamples, bgn, end, +1)


def lambertNegLimits(fixed1, sizeN, sizeD, numOfSamples):
    radius = int(INV_EXP * fixed1)
    return radius - radius * sizeN // sizeD // (numOfSamples - 1) * (numOfSamples - 1), radius


def lambertPosLimits(fixed1, sizeN, sizeD, numOfSamples):
    radius = int(INV_EXP * fixed1)
    return radius, radius + fixed1 * sizeN // sizeD // (numOfSamples - 1) * (numOfSamples - 1)


def lambertLutParams(fixed1, numOfSamples, bgn, end, sign):
    sample = (end - (bgn + 1)) // (numOfSamples - 1) + 1
    values = [int(lambertRatio(Decimal(sign * (bgn + 1 + sample * i)) / fixed1) * fixed1) for i in range(numOfSamples)]
    t_size = (len(bin(max(values))) - 3) // 8 + 1
    t_mask = (1 << (t_size * 8)) - 1
    return sample, t_size, t_mask, values


def lambertPosExact(x, fixed1):
    y = int((Decimal(x) / fixed1).ln() * fixed1)
    z = y * y // fixed1
    y = fixed1 * (z + fixed1) // (y + fixed1)
    for _ in range(7):
        e = checked(int((Decimal(y) / fixed1).exp() * fixed1))
        f = checked(y * e // fixed1)
        g = checked(y * f // fixed1)
        y = checked(fixed1 * checked(g + x) // checked(f + e))
    return x


def lambertNeg1(numOfTerms, x, fixed1):
    terms = lambertBinomial(numOfTerms)
    res = 0
    xi = x
    for i in range(2, len(terms)):
        xi = checked(xi * x) // fixed1
        res = checked(res + checked(xi * terms[i]))
    res = checked(checked(res // terms[0] + fixed1) + x)
    return terms


def lambertPos1(numOfTerms, x, fixed1):
    terms = lambertBinomial(numOfTerms)
    res = 0
    xi = x
    for i in range(2, len(terms)):
        xi = checked(xi * x) // fixed1
        res = checked(res + checked(xi * terms[i]) * (-1) ** i)
    res = checked(checked(res // terms[0] + fixed1) - x)
    return terms


def lambertBinomial(numOfTerms):
    maxFactorial = factorial(numOfTerms - 1)
    return [maxFactorial // factorial(i) * i ** (i - 1) for i in range(1, numOfTerms)]


def lambertRatio(x):
    y = x if x < 1 else x.ln()
    for _ in range(8):
        e = y.exp()
        f = y * e
        if f == x: break
        y = (y * f + x) / (f + e)
    return y / x
