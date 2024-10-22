from core import Decimal
from core import checked
from math import factorial


def lambertRadius(fixed1):
    return int(Decimal(-1).exp() * fixed1)


def lambertTerms(fixed1, maxNumOfTerms, func):
    lo = 0
    hi = maxNumOfTerms
    val = lambertRadius(fixed1)
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


def lambertNeg1Terms(fixed1, maxNumOfTerms):
    return lambertTerms(fixed1, maxNumOfTerms, lambertNeg1)


def lambertPos1Terms(fixed1, maxNumOfTerms):
    return lambertTerms(fixed1, maxNumOfTerms, lambertPos1)


def lambertSamples(fixed1, sizeOfSample, numOfSamples):
    offset = lambertRadius(fixed1) + 1
    return [int(lambertRatio(Decimal(offset + sizeOfSample * i) / fixed1) * fixed1) for i in range(numOfSamples)]


def lambertNeg1(numOfTerms, x, fixed1):
    terms = lambertBinomial(numOfTerms)
    xi = x
    res = 0
    for i in range(2, len(terms)):
        xi = checked(xi * x) // fixed1
        res = checked(res + checked(xi * terms[i]))
    res = checked(checked(res // terms[-1] + x) + fixed1)
    return terms


def lambertPos1(numOfTerms, x, fixed1):
    terms = lambertBinomial(numOfTerms)
    xi = x
    res = checked(checked(fixed1 - x) * terms[1])
    for i in range(2, len(terms)):
        xi = checked(xi * x) // fixed1
        res = checked(res + checked(xi * terms[i]) * (-1) ** i)
    res = res // terms[1]
    return terms


def lambertBinomial(numOfTerms):
    maxFactorial = factorial(numOfTerms - 1)
    return [maxFactorial * i ** (i - 1) // factorial(i) for i in range(1, numOfTerms)]


def lambertRatio(x):
    a = x if x < 1 else x.ln()
    for _ in range(8):
        e = a.exp()
        f = a * e
        if f == x: break
        a = (a * f + x) / (f + e)
    return a / x
