from core import Decimal
from core import LOG_TWO
from core import MAX_VAL
from core import two_pow
from core import checked
from math import factorial
from collections import namedtuple


def ln2Min(fixed1):
    return (LOG_TWO * fixed1).__floor__()


def ln2Max(fixed1):
    return (LOG_TWO * fixed1).__ceil__()


def logMid(fixed1, maxHiTermVal):
    return int(two_pow(maxHiTermVal).exp() * fixed1) + 1


def expMid(fixed1, maxHiTermVal):
    return int(two_pow(maxHiTermVal) * fixed1 - 1) + 1


def optimalLogTerms(fixed1, maxHiTermVal, numOfHiTerms):
    HiTerm = namedtuple('HiTerm', 'exp, bit, num, den')
    LoTerm = namedtuple('LoTerm', 'num, den')

    hiTerms = []
    loTerms = [LoTerm(fixed1 * 2, fixed1 * 2)]

    top = int(two_pow(maxHiTermVal).exp() * fixed1)
    for n in range(numOfHiTerms):
        cur = two_pow(maxHiTermVal - n - 1)
        exp = int(fixed1 * cur.exp())
        bit = int(fixed1 * cur)
        num, den = epow(-cur, top)
        assert num * (exp + 1) >= fixed1 * den
        hiTerms.append(HiTerm(exp, bit, num, den))
        top = exp

    mid = logMid(fixed1, maxHiTermVal) - 1
    res = optimalLog(mid, hiTerms, loTerms, fixed1)

    while True:
        n = len(loTerms)
        val = fixed1 * (2 * n + 2)
        loTermsNext = loTerms + [LoTerm(val // (2 * n + 1), val)]
        resNext = optimalLog(mid, hiTerms, loTermsNext, fixed1)
        if res < resNext:
            res = resNext
            loTerms = loTermsNext
        else:
            return hiTerms, loTerms


def optimalExpTerms(fixed1, maxHiTermVal, numOfHiTerms):
    HiTerm = namedtuple('HiTerm', 'bit, num, den')
    LoTerm = namedtuple('LoTerm', 'val, ind')

    hiTerms = []
    loTerms = [LoTerm(1, 1)]

    top = int(two_pow(maxHiTermVal - numOfHiTerms).exp() * fixed1) - 1
    for n in range(numOfHiTerms + 1):
        cur = two_pow(maxHiTermVal - numOfHiTerms + n)
        bit = int(fixed1 * cur)
        num, den = epow(cur, top)
        assert num <= den * cur.exp()
        hiTerms.append(HiTerm(bit, num, den))
        top = top * num // den

    mid = expMid(fixed1, maxHiTermVal) - 1
    res = optimalExp(mid, hiTerms, loTerms, fixed1)

    while True:
        n = len(loTerms)
        val = factorial(n + 1)
        loTermsNext = [LoTerm(val // factorial(i + 1), i + 1) for i in range(n + 1)]
        resNext = optimalExp(mid, hiTerms, loTermsNext, fixed1)
        if res < resNext:
            res = resNext
            loTerms = loTermsNext
        else:
            return hiTerms, loTerms


def optimalLog(x, hiTerms, loTerms, fixed1):
    res = 0
    for term in hiTerms:
        if x > term.exp:
            res |= term.bit
            x = checked(x * term.num) // term.den
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


def epow(cur, top):
    e = cur.exp()
    lists = [
        list(func(e, top)) for func in [
            lambda e, top: epow_n_first(e, top, int.__sub__     , 0, 100000),
            lambda e, top: epow_d_first(e, top, int.__sub__     , 0, 100000),
            lambda e, top: epow_n_first(e, top, int.__floordiv__, 1,  10000),
            lambda e, top: epow_d_first(e, top, int.__floordiv__, 1,  10000),
            lambda e, top: epow_n_first(e, top, int.__rshift__  , 0,    100),
            lambda e, top: epow_d_first(e, top, int.__rshift__  , 0,    100),
        ]
    ]
    return max(sum(lists, []), key = lambda x: Decimal(x[0]) / Decimal(x[1]))


def epow_n_first(e, top, op, bgn, end):
    m = MAX_VAL // top
    ns = [op(m, i) for i in range(bgn, end)]
    ds = [(n / e).__ceil__() for n in ns]
    return zip(ns, ds)


def epow_d_first(e, top, op, bgn, end):
    m = int(MAX_VAL / (top * e))
    ds = [op(m, i) for i in range(bgn, end)]
    ns = [(d * e).__floor__() for d in ds]
    return zip(ns, ds)
