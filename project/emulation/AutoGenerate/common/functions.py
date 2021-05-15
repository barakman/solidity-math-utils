from math import factorial


def getTaylorCoefs(numOfCoefficients):
    maxFactorial = factorial(numOfCoefficients-1)
    return [maxFactorial//factorial(i) for i in range(1,numOfCoefficients)]


def getLambertCoefs(numOfLambertCoefs):
    maxFactorial = factorial(numOfLambertCoefs-1)
    return [maxFactorial*i**(i-1)//factorial(i) for i in range(1,numOfLambertCoefs)]


def getMaxExpArray(coefficients,numOfPrecisions):
    return [binarySearch(generalExp,[coefficients,precision]) for precision in range(numOfPrecisions)]


def getMaxValArray(coefficients,maxExpArray):
    return [generalExp(maxExpArray[precision],coefficients,precision) for precision in range(len(maxExpArray))]


def binarySearch(func,args):
    lo = 0
    hi = (1<<256)-1
    while lo+1 < hi:
        mid = (lo+hi)//2
        try:
            func(mid,*args)
            lo = mid
        except:
            hi = mid
    try:
        func(hi,*args)
        return hi
    except:
        func(lo,*args)
        return lo


def generalExp(x,coefficients,precision):
    xi = x
    res = 0
    for coefficient in coefficients[1:]:
        xi = safe(xi*x)>>precision
        res = safe(res+safe(xi*coefficient))
    return safe(safe(res//coefficients[0]+x)+(1<<precision))


def optimalLog(x,hiTerms,loTerms,fixed1):
    res = 0
    for term in hiTerms[+1:]:
        if x >= term.exp:
            res = safe(res+term.val)
            x = safe(x*fixed1)//term.exp
    z = y = safe(x-fixed1)
    w = safe(y*y)//fixed1
    for term in loTerms[:-1]:
        res = safe(res+safe(z*safe(term.num-y))//term.den)
        z = safe(z*w)//fixed1
    res = safe(res+safe(z*safe(loTerms[-1].num-y))//loTerms[-1].den)
    return res


def optimalExp(x,hiTerms,loTerms,fixed1):
    res = 0
    z = y = x % hiTerms[0].bit
    for term in loTerms[+1:]:
        z = safe(z*y)//fixed1
        res = safe(res+safe(z*term.val))
    res = safe(safe(res//loTerms[0].val+y)+fixed1)
    for term in hiTerms[:-1]:
        if x & term.bit:
            res = safe(res*term.num)//term.den
    return res


def lambertPos3(x,optimalLog,generalLog,optimalLogMaxVal,fixed1):
    L1 = optimalLog(x) if x < optimalLogMaxVal else generalLog(x)
    L2 = optimalLog(L1) if L1 < optimalLogMaxVal else generalLog(L1)
    return safe(safe(safe(L1-L2)+safe(L2*fixed1)//L1)*fixed1)//x


def safe(x):
    assert 0 <= x <= 2**256-1
    return x
