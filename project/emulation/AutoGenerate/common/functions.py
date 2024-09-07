from common import Decimal
from math import factorial
from collections import namedtuple
from common.constants import FIXED_1
from common.constants import LOG_MAX_HI_TERM_VAL
from common.constants import LOG_NUM_OF_HI_TERMS
from common.constants import EXP_MAX_HI_TERM_VAL
from common.constants import EXP_NUM_OF_HI_TERMS
from common.constants import LAMBERT_NUM_OF_COEFS


MAX_VAL = (1<<256)-1


def lambertCoefs():
    maxFactorial = factorial(LAMBERT_NUM_OF_COEFS-1)
    return [maxFactorial*i**(i-1)//factorial(i) for i in range(1,LAMBERT_NUM_OF_COEFS)]


def lambertRatio(x):
    a = x if x < 1 else x.ln()
    for _ in range(8):
        e = a.exp()
        f = a * e
        if f == x: break
        a = (a * f + x) / (f + e)
    return a / x


def optimalLogTerms():
    hiTerms = []
    loTerms = []

    HiTerm = namedtuple('HiTerm','val,exp')
    LoTerm = namedtuple('LoTerm','num,den')

    for n in range(LOG_NUM_OF_HI_TERMS+1):
        cur = Decimal(LOG_MAX_HI_TERM_VAL)/2**n
        val = int(FIXED_1*cur)
        exp = int(FIXED_1*cur.exp()+1)
        hiTerms.append(HiTerm(val,exp))

    highest = hiTerms[0].exp-1
    loTerms = [LoTerm(FIXED_1*2,FIXED_1*2)]
    res = optimalLog(highest,hiTerms,loTerms,FIXED_1)

    while True:
        n = len(loTerms)
        val = FIXED_1*(2*n+2)
        loTermsNext = loTerms+[LoTerm(val//(2*n+1),val)]
        resNext = optimalLog(highest,hiTerms,loTermsNext,FIXED_1)
        if res < resNext:
            res = resNext
            loTerms = loTermsNext
        else:
            return hiTerms,loTerms


def optimalExpTerms():
    hiTerms = []
    loTerms = []

    HiTerm = namedtuple('HiTerm','bit,num,den')
    LoTerm = namedtuple('LoTerm','val,ind')

    top = int(Decimal(2**(0+EXP_MAX_HI_TERM_VAL-EXP_NUM_OF_HI_TERMS)).exp()*FIXED_1)-1
    for n in range(EXP_NUM_OF_HI_TERMS+1):
        cur = Decimal(2**(n+EXP_MAX_HI_TERM_VAL-EXP_NUM_OF_HI_TERMS)).exp()
        den = int(MAX_VAL/(cur*top))
        num = int(den*cur)
        top = top*num//den
        bit = (FIXED_1<<(n+EXP_MAX_HI_TERM_VAL))>>EXP_NUM_OF_HI_TERMS
        hiTerms.append(HiTerm(bit,num,den))

    highest = hiTerms[-1].bit-1
    loTerms = [LoTerm(1,1)]
    res = optimalExp(highest,hiTerms,loTerms,FIXED_1)

    while True:
        n = len(loTerms)+1
        val = factorial(n)
        loTermsNext = [LoTerm(val//factorial(i+1),i+1) for i in range(n)]
        resNext = optimalExp(highest,hiTerms,loTermsNext,FIXED_1)
        if res < resNext:
            res = resNext
            loTerms = loTermsNext
        else:
            return hiTerms,loTerms


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


def safe(x):
    assert 0 <= x <= MAX_VAL
    return x
