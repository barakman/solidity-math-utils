from core import Decimal
from core import INV_EXP
from core import MAX_VAL
from core import checked
from math import factorial


def lambertRadius(fixed1):
    return int(INV_EXP * fixed1)


def lambertNeg1Terms(fixed1, maxNumOfTerms):
    return lambertTerms(fixed1, maxNumOfTerms, lambertNeg1)


def lambertPos1Terms(fixed1, maxNumOfTerms):
    return lambertTerms(fixed1, maxNumOfTerms, lambertPos1)


def lambertSamples(fixed1, sizeOfSample, numOfSamples):
    offset = lambertRadius(fixed1) + 1
    return [int(lambertRatio(Decimal(offset + sizeOfSample * i) / fixed1) * fixed1) for i in range(numOfSamples)]


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


def lambertPos3MaxVal(fixed1):
    lo = fixed1
    hi = MAX_VAL
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if lambertPos3Val(mid, fixed1):
            lo = mid
        else:
            hi = mid
    if lambertPos3Val(hi, fixed1):
        return hi
    if lambertPos3Val(lo, fixed1):
        return lo
    assert False


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


def lambertPos3Val(x, fixed1):
    f = (Decimal(x) / fixed1).ln()
    return f >= (f + 1) * f.ln()


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
