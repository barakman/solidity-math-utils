from .common.BuiltIn import *
from .common.Uint256 import *
from . import AnalyticMath
from . import IntegralMath

'''
    @dev Calculate the amount of pool tokens returned in exchange for a specified amount of reserve tokens
    
    @param supply   The total amount of pool tokens
    @param balance  The amount of reserve tokens owned by the pool
    @param weight   The weight of this reserve in the pool
    @param weights  The weight of all reserves in the pool
    @param amount   The amount of reserve tokens provided
    
    @return supply * ((1 + amount / balance) ^ (weight / weights) - 1)
    
    @notice This function never overestimates the true result
'''
def mintGain(supply, balance, weight, weights, amount):
    require(supply > 0 and balance > 0 and weight > 0 and weights > 0, "InvalidInput()");
    require(weight <= weights, "WeightOutOfBound()");
    require(amount <= MAX_VAL - balance, "AmountOutOfBound()");

    if (weight == weights):
        return IntegralMath.mulDivF(supply, amount, balance);

    (n, d) = AnalyticMath.pow(balance + amount, balance, weight, weights);
    return IntegralMath.mulDivF(supply, n - d, d);

'''
    @dev Calculate the amount of reserve tokens required in exchange for a specified amount of pool tokens
    
    @param supply   The total amount of pool tokens
    @param balance  The amount of reserve tokens owned by the pool
    @param weight   The weight of this reserve in the pool
    @param weights  The weight of all reserves in the pool
    @param amount   The amount of pool tokens desired
    
    @return balance * ((1 + amount / supply) ^ (weights / weight) - 1)
    
    @notice This function might underestimate the true result
'''
def mintCost(supply, balance, weight, weights, amount):
    require(supply > 0 and balance > 0 and weight > 0 and weights > 0, "InvalidInput()");
    require(weight <= weights, "WeightOutOfBound()");
    require(amount <= MAX_VAL - supply, "AmountOutOfBound()");

    if (weight == weights):
        return IntegralMath.mulDivC(balance, amount, supply);

    (n, d) = AnalyticMath.pow(supply + amount, supply, weights, weight);
    return IntegralMath.mulDivC(balance, n - d, d);

'''
    @dev Calculate the amount of reserve tokens returned in exchange for a specified amount of pool tokens
    
    @param supply   The total amount of pool tokens
    @param balance  The amount of reserve tokens owned by the pool
    @param weight   The weight of this reserve in the pool
    @param weights  The weight of all reserves in the pool
    @param amount   The amount of pool tokens provided
    
    @return balance * (1 - (1 - amount / supply) ^ (weights / weight))
    
    @notice This function never overestimates the true result
'''
def burnGain(supply, balance, weight, weights, amount):
    require(supply > 0 and balance > 0 and weight > 0 and weights > 0, "InvalidInput()");
    require(weight <= weights, "WeightOutOfBound()");
    require(amount <= supply, "AmountOutOfBound()");

    if (amount == supply):
        return balance;

    if (weight == weights):
        return IntegralMath.mulDivF(balance, amount, supply);

    (n, d) = AnalyticMath.pow(supply - amount, supply, weights, weight);
    return IntegralMath.mulDivF(balance, d - n, d);

'''
    @dev Calculate the amount of pool tokens required in exchange for a specified amount of reserve tokens
    
    @param supply   The total amount of pool tokens
    @param balance  The amount of reserve tokens owned by the pool
    @param weight   The weight of this reserve in the pool
    @param weights  The weight of all reserves in the pool
    @param amount   The amount of reserve tokens desired
    
    @return supply * (1 - (1 - amount / balance) ^ (weight / weights))
    
    @notice This function might underestimate the true result
'''
def burnCost(supply, balance, weight, weights, amount):
    require(supply > 0 and balance > 0 and weight > 0 and weights > 0, "InvalidInput()");
    require(weight <= weights, "WeightOutOfBound()");
    require(amount <= balance, "AmountOutOfBound()");

    if (amount == balance):
        return supply;

    if (weight == weights):
        return IntegralMath.mulDivC(supply, amount, balance);

    (n, d) = AnalyticMath.pow(balance - amount, balance, weight, weights);
    return IntegralMath.mulDivC(supply, d - n, d);

'''
    @dev Calculate the amount of reserve2 tokens returned in exchange for a specified amount of reserve1 tokens
    
    @param balance1 The amount of reserve1 tokens owned by the pool
    @param balance2 The amount of reserve2 tokens owned by the pool
    @param weight1  The weight of reserve1 in the pool
    @param weight2  The weight of reserve2 in the pool
    @param amount   The amount of reserve1 tokens provided
    
    @return balance2 * (1 - (balance1 / (balance1 + amount)) ^ (weight1 / weight2))
    
    @notice This function never overestimates the true result
'''
def swapGain(balance1, balance2, weight1, weight2, amount):
    require(balance1 > 0 and balance2 > 0 and weight1 > 0 and weight2 > 0, "InvalidInput()");
    require(amount <= MAX_VAL - balance1, "AmountOutOfBound()");

    if (weight1 == weight2):
        return IntegralMath.mulDivF(balance2, amount, balance1 + amount);

    (n, d) = AnalyticMath.pow(balance1, balance1 + amount, weight1, weight2);
    return IntegralMath.mulDivF(balance2, d - n, d);

'''
    @dev Calculate the amount of reserve1 tokens required in exchange for a specified amount of reserve2 tokens
    
    @param balance1 The amount of reserve1 tokens owned by the pool
    @param balance2 The amount of reserve2 tokens owned by the pool
    @param weight1  The weight of reserve1 in the pool
    @param weight2  The weight of reserve2 in the pool
    @param amount   The amount of reserve2 tokens desired
    
    @return balance1 * ((balance2 / (balance2 - amount)) ^ (weight2 / weight1) - 1)
    
    @notice This function might underestimate the true result
'''
def swapCost(balance1, balance2, weight1, weight2, amount):
    require(balance1 > 0 and balance2 > 0 and weight1 > 0 and weight2 > 0, "InvalidInput()");
    require(amount < balance2, "AmountOutOfBound()");

    if (weight1 == weight2):
        return IntegralMath.mulDivC(balance1, amount, balance2 - amount);

    (n, d) = AnalyticMath.pow(balance2, balance2 - amount, weight2, weight1);
    return IntegralMath.mulDivC(balance1, n - d, d);
