from core import Decimal
from core import MAX_VAL
from core import checked
from math import factorial
from collections import namedtuple


def scaledLn2(fixed1):
    return Decimal(2).ln() * fixed1


def optimalLogTerms(fixed1, maxHiTermVal, numOfHiTerms):
    HiTerm = namedtuple('HiTerm', 'val,exp')
    LoTerm = namedtuple('LoTerm', 'num,den')

    hiTerms = []
    loTerms = [LoTerm(fixed1 * 2, fixed1 * 2)]

    for n in range(numOfHiTerms + 1):
        cur = Decimal(2 ** (maxHiTermVal - n))
        val = int(fixed1 * cur)
        exp = int(fixed1 * cur.exp() + 1)
        hiTerms.append(HiTerm(val, exp))

    highest = hiTerms[0].exp - 1
    res = optimalLog(highest, hiTerms, loTerms, fixed1)

    while True:
        n = len(loTerms)
        val = fixed1 * (2 * n + 2)
        loTermsNext = loTerms + [LoTerm(val // (2 * n + 1), val)]
        resNext = optimalLog(highest, hiTerms, loTermsNext, fixed1)
        if res < resNext:
            res = resNext
            loTerms = loTermsNext
        else:
            return hiTerms, loTerms


def optimalExpTerms(fixed1, maxHiTermVal, numOfHiTerms):
    HiTerm = namedtuple('HiTerm', 'bit,num,den')
    LoTerm = namedtuple('LoTerm', 'val,ind')

    hiTerms = []
    loTerms = [LoTerm(1, 1)]

    top = int(Decimal(2 ** (0 + maxHiTermVal - numOfHiTerms)).exp() * fixed1) - 1
    for n in range(numOfHiTerms + 1):
        cur = Decimal(2 ** (n + maxHiTermVal - numOfHiTerms)).exp()
        den = int(MAX_VAL / (cur * top))
        num = int(den * cur)
        top = top * num // den
        bit = (fixed1 << (n + maxHiTermVal)) >> numOfHiTerms
        hiTerms.append(HiTerm(bit, num, den))

    highest = hiTerms[-1].bit - 1
    res = optimalExp(highest, hiTerms, loTerms, fixed1)

    while True:
        n = len(loTerms)
        val = factorial(n + 1)
        loTermsNext = [LoTerm(val // factorial(i + 1), i + 1) for i in range(n + 1)]
        resNext = optimalExp(highest, hiTerms, loTermsNext, fixed1)
        if res < resNext:
            res = resNext
            loTerms = loTermsNext
        else:
            return hiTerms, loTerms


def optimalLog(x, hiTerms, loTerms, fixed1):
    res = 0
    for term in hiTerms[+1:]:
        if x >= term.exp:
            res |= term.val
            x = checked(x * fixed1) // term.exp
    z = y = checked(x - fixed1)
    w = checked(y * y) // fixed1
    for term in loTerms[:-1]:
        res = checked(res + checked(z * checked(term.num - y)) // term.den)
        z = checked(z * w) // fixed1
    res = checked(res + checked(z * checked(loTerms[-1].num - y)) // loTerms[-1].den)
    return res


def optimalExp(x, hiTerms, loTerms, fixed1):
    res = 0
    z = y = x % hiTerms[0].bit
    for term in loTerms[+1:]:
        z = checked(z * y) // fixed1
        res = checked(res + checked(z * term.val))
    res = checked(checked(res // loTerms[0].val + y) + fixed1)
    for term in hiTerms[:-1]:
        if x & term.bit:
            res = checked(res * term.num) // term.den
    return res
