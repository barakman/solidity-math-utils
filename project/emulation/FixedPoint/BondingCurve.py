from .common.BuiltIn import *
from .common.Uint import *
from .AnalyticMath import *

MIN_WEIGHT = 1;
MAX_WEIGHT = 1000000;

'''
    @dev Buy pool tokens with reserve tokens
    
    @param supply   The total amount of pool tokens
    @param balance  The amount of reserve tokens owned by the pool
    @param weight   The weight of the reserve (represented in ppm)
    @param amount   The amount of reserve tokens provided
    
    @return supply * ((1 + amount / balance) ^ (weight / MAX_WEIGHT) - 1)
'''
def buy(supply, balance, weight, amount):
    require(supply > 0, "invalid supply");
    require(balance > 0, "invalid balance");
    require(MIN_WEIGHT <= weight and weight <= MAX_WEIGHT, "invalid weight");

    if (amount == 0):
        return 0;

    if (weight == MAX_WEIGHT):
        return IntegralMath.mulDivF(amount, supply, balance);

    (n, d) = pow(safeAdd(balance, amount), balance, weight, MAX_WEIGHT);
    return IntegralMath.mulDivF(supply, n, d) - supply;

'''
    @dev Sell pool tokens for reserve tokens
    
    @param supply   The total amount of pool tokens
    @param balance  The amount of reserve tokens owned by the pool
    @param weight   The weight of the reserve (represented in ppm)
    @param amount   The amount of pool tokens provided
    
    @return balance * (1 - (1 - amount / supply) ^ (MAX_WEIGHT / weight))
'''
def sell(supply, balance, weight, amount):
    require(supply > 0, "invalid supply");
    require(balance > 0, "invalid balance");
    require(MIN_WEIGHT <= weight and weight <= MAX_WEIGHT, "invalid weight");
    require(amount <= supply, "invalid amount");

    if (amount == 0):
        return 0;

    if (amount == supply):
        return balance;

    if (weight == MAX_WEIGHT):
        return IntegralMath.mulDivF(amount, balance, supply);

    (n, d) = pow(supply, supply - amount, MAX_WEIGHT, weight);
    return IntegralMath.mulDivF(balance, n - d, n);

'''
    @dev Convert reserve tokens of one type to another
    
    @param balance1 The amount of source reserve tokens owned by the pool
    @param weight1  The weight of the source reserve (represented in ppm)
    @param balance2 The amount of target reserve tokens owned by the pool
    @param weight2  The weight of the target reserve (represented in ppm)
    @param amount   The amount of source reserve tokens provided
    
    @return balance2 * (1 - (balance1 / (balance1 + amount)) ^ (weight1 / weight2))
'''
def convert(balance1, weight1, balance2, weight2, amount):
    require(0 < balance1, "invalid source balance");
    require(0 < balance2, "invalid target balance");
    require(MIN_WEIGHT <= weight1 and weight1 <= MAX_WEIGHT, "invalid source weight");
    require(MIN_WEIGHT <= weight2 and weight2 <= MAX_WEIGHT, "invalid target weight");

    if (weight1 == weight2):
        return IntegralMath.mulDivF(balance2, amount, safeAdd(balance1, amount));

    (n, d) = pow(safeAdd(balance1, amount), balance1, weight1, weight2);
    return IntegralMath.mulDivF(balance2, n - d, n);

'''
    @dev Deposit reserve tokens for pool tokens
    
    @param supply   The total amount of pool tokens
    @param balance  The amount of reserve tokens of the desired type owned by the pool
    @param weights  The combined weights of the reserves (represented in ppm)
    @param amount   The amount of reserve tokens of the desired type provided
    
    @return supply * ((amount / balance + 1) ^ (weights / MAX_WEIGHT) - 1)
'''
def deposit(supply, balance, weights, amount):
    require(supply > 0, "invalid supply");
    require(balance > 0, "invalid balance");
    require(MIN_WEIGHT * 2 <= weights and weights <= MAX_WEIGHT * 2, "invalid weights");

    if (amount == 0):
        return 0;

    if (weights == MAX_WEIGHT):
        return IntegralMath.mulDivF(amount, supply, balance);

    (n, d) = pow(safeAdd(balance, amount), balance, weights, MAX_WEIGHT);
    return IntegralMath.mulDivF(supply, n, d) - supply;

'''
    @dev Withdraw reserve tokens with pool tokens
    
    @param supply   The total amount of pool tokens
    @param balance  The amount of reserve tokens of the desired type owned by the pool
    @param weights  The combined weights of the reserves (represented in ppm)
    @param amount   The amount of pool tokens provided
    
    @return balance * (1 - ((supply - amount) / supply) ^ (MAX_WEIGHT / weights))
'''
def withdraw(supply, balance, weights, amount):
    require(supply > 0, "invalid supply");
    require(balance > 0, "invalid balance");
    require(MIN_WEIGHT * 2 <= weights and weights <= MAX_WEIGHT * 2, "invalid weights");
    require(amount <= supply, "invalid amount");

    if (amount == 0):
        return 0;

    if (amount == supply):
        return balance;

    if (weights == MAX_WEIGHT):
        return IntegralMath.mulDivF(amount, balance, supply);

    (n, d) = pow(supply, supply - amount, MAX_WEIGHT, weights);
    return IntegralMath.mulDivF(balance, n - d, n);

'''
    @dev Invest reserve tokens for pool tokens
    
    @param supply   The total amount of pool tokens
    @param balance  The amount of reserve tokens of the desired type owned by the pool
    @param weights  The combined weights of the reserves (represented in ppm)
    @param amount   The amount of pool tokens desired
    
    @return balance * (((supply + amount) / supply) ^ (MAX_WEIGHT / weights) - 1)
'''
def invest(supply, balance, weights, amount):
    require(supply > 0, "invalid supply");
    require(balance > 0, "invalid balance");
    require(MIN_WEIGHT * 2 <= weights and weights <= MAX_WEIGHT * 2, "invalid weights");

    if (amount == 0):
        return 0;

    if (weights == MAX_WEIGHT):
        return IntegralMath.mulDivC(amount, balance, supply);

    (n, d) = pow(safeAdd(supply, amount), supply, MAX_WEIGHT, weights);
    return IntegralMath.mulDivC(balance, n, d) - balance;
