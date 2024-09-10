from core import Decimal
from core import checked
from math import factorial


def lambertRadius(fixed1):
    return int(Decimal(-1).exp() * fixed1)


def lambertCoefs(fixed1, maxNumOfCoefs, sign):
    lo = 0
    hi = maxNumOfCoefs
    val = lambertRadius(fixed1)
    func = {-1: lambertNeg1, +1: lambertPos1}[sign]
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        try:
            func(mid, val, fixed1)
            lo = mid
        except:
            hi = mid
    try:
        return func(hi, val, fixed1)
    except:
        return func(lo, val, fixed1)


def lambertSamples(fixed1, sizeOfSample, numOfSamples):
    offset = lambertRadius(fixed1) + 1
    return [int(lambertRatio(Decimal(offset + sizeOfSample * i) / fixed1) * fixed1) for i in range(numOfSamples)]


def lambertNeg1(numOfCoefs, x, fixed1):
    coefs = lambertBinomial(numOfCoefs)
    xi = x
    res = 0
    for coef in coefs[2:-1]:
        xi = checked(xi * x) // fixed1
        res = checked(res + checked(xi * coef))
    res = checked(checked(res // coefs[-1] + x) + fixed1)
    return coefs


def lambertPos1(numOfCoefs, x, fixed1):
    coefs = lambertBinomial(numOfCoefs)
    xi = x
    res = checked(checked(fixed1 - x) * coefs[1])
    for i, coef in enumerate(coefs[2:-1]):
        xi = checked(xi * x) // fixed1
        res = checked(res + checked(xi * coef) * (-1) ** i)
    res = res // coefs[1]
    return coefs


def lambertBinomial(numOfCoefs):
    maxFactorial = factorial(numOfCoefs - 1)
    return [maxFactorial * i ** (i - 1) // factorial(i) for i in range(1, numOfCoefs)]


def lambertRatio(x):
    a = x if x < 1 else x.ln()
    for _ in range(8):
        e = a.exp()
        f = a * e
        if f == x: break
        a = (a * f + x) / (f + e)
    return a / x
