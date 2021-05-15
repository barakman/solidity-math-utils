from mpmath import mp
from mpmath import lambertw
from decimal import Decimal
from decimal import getcontext


getcontext().prec = mp.dps = 80 # 78 digits for a maximum of 2^256-1, and 2 more digits for after the decimal point


def pow(a, b, c, d, factor):
    a, b, c, d, factor = [Decimal(value) for value in vars().values()]
    return (a/b)**(c/d)*factor


def log(a, b, factor):
    a, b, factor = [Decimal(value) for value in vars().values()]
    return (a/b).ln()*factor


def exp(a, b, factor):
    a, b, factor = [Decimal(value) for value in vars().values()]
    return (a/b).exp()*factor


def lambertNeg(x, factor):
    x, factor = [Decimal(value) for value in vars().values()]
    return Decimal(str(lambertw(-x/factor)))/(-x/factor)*factor


def lambertPos(x, factor):
    x, factor = [Decimal(value) for value in vars().values()]
    return Decimal(str(lambertw(+x/factor)))/(+x/factor)*factor


def buy(supply, balance, weight, amount):
    supply, balance, weight, amount = [Decimal(value) for value in vars().values()]
    return supply*((1+amount/balance)**(weight/MAX_WEIGHT)-1)


def sell(supply, balance, weight, amount):
    supply, balance, weight, amount = [Decimal(value) for value in vars().values()]
    return balance*(1-(1-amount/supply)**(MAX_WEIGHT/weight))


def convert(balance1, weight1, balance2, weight2, amount):
    balance1, weight1, balance2, weight2, amount = [Decimal(value) for value in vars().values()]
    return balance2*(1-(balance1/(balance1+amount))**(weight1/weight2))


def deposit(supply, balance, weights, amount):
    supply, balance, weights, amount = [Decimal(value) for value in vars().values()]
    return supply*((amount/balance+1)**(weights/MAX_WEIGHT)-1)


def withdraw(supply, balance, weights, amount):
    supply, balance, weights, amount = [Decimal(value) for value in vars().values()]
    return balance*(1-((supply-amount)/supply)**(MAX_WEIGHT/weights))


def invest(supply, balance, weights, amount):
    supply, balance, weights, amount = [Decimal(value) for value in vars().values()]
    return balance*(((supply+amount)/supply)**(MAX_WEIGHT/weights)-1)
