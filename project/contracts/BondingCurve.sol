// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.34;

import "./AnalyticMath.sol";
import "./IntegralMath.sol";

library BondingCurve {
    error InvalidInput();
    error WeightOutOfBound();
    error AmountOutOfBound();

    /**
      * @dev Calculate the amount of pool tokens returned in exchange for a specified amount of reserve tokens
      *
      * @param supply   The total amount of pool tokens
      * @param balance  The amount of reserve tokens owned by the pool
      * @param weight   The weight of this reserve in the pool
      * @param weights  The weight of all reserves in the pool
      * @param amount   The amount of reserve tokens provided
      *
      * @return supply * ((1 + amount / balance) ^ (weight / weights) - 1)
      *
      * @notice This function never overestimates the true result
    */
    function mintGain(uint256 supply, uint256 balance, uint256 weight, uint256 weights, uint256 amount) internal pure returns (uint256) { unchecked {
        require(supply > 0 && balance > 0 && weight > 0 && weights > 0, InvalidInput());
        require(weight <= weights, WeightOutOfBound());
        require(amount <= ~balance, AmountOutOfBound());

        if (weight == weights)
            return IntegralMath.mulDivF(supply, amount, balance);

        (uint256 n, uint256 d) = AnalyticMath.pow(balance + amount, balance, weight, weights);
        return IntegralMath.mulDivF(supply, n - d, d);
    }}

    /**
      * @dev Calculate the amount of reserve tokens required in exchange for a specified amount of pool tokens
      *
      * @param supply   The total amount of pool tokens
      * @param balance  The amount of reserve tokens owned by the pool
      * @param weight   The weight of this reserve in the pool
      * @param weights  The weight of all reserves in the pool
      * @param amount   The amount of pool tokens desired
      *
      * @return balance * ((1 + amount / supply) ^ (weights / weight) - 1)
      *
      * @notice This function might underestimate the true result
    */
    function mintCost(uint256 supply, uint256 balance, uint256 weight, uint256 weights, uint256 amount) internal pure returns (uint256) { unchecked {
        require(supply > 0 && balance > 0 && weight > 0 && weights > 0, InvalidInput());
        require(weight <= weights, WeightOutOfBound());
        require(amount <= ~supply, AmountOutOfBound());

        if (weight == weights)
            return IntegralMath.mulDivC(balance, amount, supply);

        (uint256 n, uint256 d) = AnalyticMath.pow(supply + amount, supply, weights, weight);
        return IntegralMath.mulDivC(balance, n - d, d);
    }}

    /**
      * @dev Calculate the amount of reserve tokens returned in exchange for a specified amount of pool tokens
      *
      * @param supply   The total amount of pool tokens
      * @param balance  The amount of reserve tokens owned by the pool
      * @param weight   The weight of this reserve in the pool
      * @param weights  The weight of all reserves in the pool
      * @param amount   The amount of pool tokens provided
      *
      * @return balance * (1 - (1 - amount / supply) ^ (weights / weight))
      *
      * @notice This function never overestimates the true result
    */
    function burnGain(uint256 supply, uint256 balance, uint256 weight, uint256 weights, uint256 amount) internal pure returns (uint256) { unchecked {
        require(supply > 0 && balance > 0 && weight > 0 && weights > 0, InvalidInput());
        require(weight <= weights, WeightOutOfBound());
        require(amount <= supply, AmountOutOfBound());

        if (amount == supply)
            return balance;

        if (weight == weights)
            return IntegralMath.mulDivF(balance, amount, supply);

        (uint256 n, uint256 d) = AnalyticMath.pow(supply - amount, supply, weights, weight);
        return IntegralMath.mulDivF(balance, d - n, d);
    }}

    /**
      * @dev Calculate the amount of pool tokens required in exchange for a specified amount of reserve tokens
      *
      * @param supply   The total amount of pool tokens
      * @param balance  The amount of reserve tokens owned by the pool
      * @param weight   The weight of this reserve in the pool
      * @param weights  The weight of all reserves in the pool
      * @param amount   The amount of reserve tokens desired
      *
      * @return supply * (1 - (1 - amount / balance) ^ (weight / weights))
      *
      * @notice This function might underestimate the true result
    */
    function burnCost(uint256 supply, uint256 balance, uint256 weight, uint256 weights, uint256 amount) internal pure returns (uint256) { unchecked {
        require(supply > 0 && balance > 0 && weight > 0 && weights > 0, InvalidInput());
        require(weight <= weights, WeightOutOfBound());
        require(amount <= balance, AmountOutOfBound());

        if (amount == balance)
            return supply;

        if (weight == weights)
            return IntegralMath.mulDivC(supply, amount, balance);

        (uint256 n, uint256 d) = AnalyticMath.pow(balance - amount, balance, weight, weights);
        return IntegralMath.mulDivC(supply, d - n, d);
    }}

    /**
      * @dev Calculate the amount of reserve2 tokens returned in exchange for a specified amount of reserve1 tokens
      *
      * @param balance1 The amount of reserve1 tokens owned by the pool
      * @param balance2 The amount of reserve2 tokens owned by the pool
      * @param weight1  The weight of reserve1 in the pool
      * @param weight2  The weight of reserve2 in the pool
      * @param amount   The amount of reserve1 tokens provided
      *
      * @return balance2 * (1 - (balance1 / (balance1 + amount)) ^ (weight1 / weight2))
      *
      * @notice This function never overestimates the true result
    */
    function swapGain(uint256 balance1, uint256 balance2, uint256 weight1, uint256 weight2, uint256 amount) internal pure returns (uint256) { unchecked {
        require(balance1 > 0 && balance2 > 0 && weight1 > 0 && weight2 > 0, InvalidInput());
        require(amount <= ~balance1, AmountOutOfBound());

        if (weight1 == weight2)
            return IntegralMath.mulDivF(balance2, amount, balance1 + amount);

        (uint256 n, uint256 d) = AnalyticMath.pow(balance1, balance1 + amount, weight1, weight2);
        return IntegralMath.mulDivF(balance2, d - n, d);
    }}

    /**
      * @dev Calculate the amount of reserve1 tokens required in exchange for a specified amount of reserve2 tokens
      *
      * @param balance1 The amount of reserve1 tokens owned by the pool
      * @param balance2 The amount of reserve2 tokens owned by the pool
      * @param weight1  The weight of reserve1 in the pool
      * @param weight2  The weight of reserve2 in the pool
      * @param amount   The amount of reserve2 tokens desired
      *
      * @return balance1 * ((balance2 / (balance2 - amount)) ^ (weight2 / weight1) - 1)
      *
      * @notice This function might underestimate the true result
    */
    function swapCost(uint256 balance1, uint256 balance2, uint256 weight1, uint256 weight2, uint256 amount) internal pure returns (uint256) { unchecked {
        require(balance1 > 0 && balance2 > 0 && weight1 > 0 && weight2 > 0, InvalidInput());
        require(amount < balance2, AmountOutOfBound());

        if (weight1 == weight2)
            return IntegralMath.mulDivC(balance1, amount, balance2 - amount);

        (uint256 n, uint256 d) = AnalyticMath.pow(balance2, balance2 - amount, weight2, weight1);
        return IntegralMath.mulDivC(balance1, n - d, d);
    }}
}
