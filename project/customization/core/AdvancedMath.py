from core import Decimal
from core import INV_EXP
from core import checked
from math import factorial


def lambertNeg1Terms(fixed1, maxNumOfTerms, maxVal):
    return lambertTerms(fixed1, maxNumOfTerms, maxVal, lambertNeg1)


def lambertPos1Terms(fixed1, maxNumOfTerms, maxVal):
    return lambertTerms(fixed1, maxNumOfTerms, maxVal, lambertPos1)


def lambertNegParams(fixed1, samples, part_n, part_d):
    bgn, end = lambertNegLimits(fixed1, samples, part_n, part_d)
    return bgn, end, *lambertLutParams(fixed1, samples, bgn, end, -1)


def lambertPosParams(fixed1, samples, size_n, size_d):
    bgn, end = lambertPosLimits(fixed1, samples, size_n, size_d)
    return bgn, end, *lambertLutParams(fixed1, samples, bgn, end, +1)


def lambertNegLimits(fixed1, samples, part_n, part_d):
    radius = int(INV_EXP * fixed1)
    return radius - radius * part_n // part_d // (samples - 1) * (samples - 1), radius


def lambertPosLimits(fixed1, samples, size_n, size_d):
    radius = int(INV_EXP * fixed1)
    return radius, radius + fixed1 * size_n // size_d // (samples - 1) * (samples - 1)


def lambertLutParams(fixed1, samples, bgn, end, sign):
    sample = (end - (bgn + 1)) // (samples - 1) + 1
    values = [int(lambertRatio(Decimal(sign * (bgn + 1 + sample * i)) / fixed1) * fixed1) for i in range(samples)]
    t_size = (len(bin(max(values))) - 3) // 8 + 1
    t_mask = (1 << (t_size * 8)) - 1
    return sample, t_size, t_mask, values


def lambertTerms(fixed1, maxNumOfTerms, maxVal, func):
    lo = 0
    hi = maxNumOfTerms
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        try:
            func(mid, maxVal, fixed1)
            lo = mid
        except:
            hi = mid
    try:
        return func(hi, maxVal, fixed1)
    except:
        return func(lo, maxVal, fixed1)


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
    a = x if x < 1 else x.ln()
    for _ in range(8):
        e = a.exp()
        f = a * e
        if f == x: break
        a = (a * f + x) / (f + e)
    return a / x
