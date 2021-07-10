// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity 0.8.6;

import "./AnalyticMath.sol";

contract BondingCurve is AnalyticMath {
    uint256 private constant MIN_WEIGHT = 1;
    uint256 private constant MAX_WEIGHT = 1000000;

    /**
      * @dev Buy pool tokens with reserve tokens
      *
      * @param supply   The total amount of pool tokens
      * @param balance  The amount of reserve tokens owned by the pool
      * @param weight   The weight of the reserve (represented in ppm)
      * @param amount   The amount of reserve tokens provided
      *
      * @return supply * ((1 + amount / balance) ^ (weight / MAX_WEIGHT) - 1)
    */
    function buy(uint256 supply, uint256 balance, uint256 weight, uint256 amount) public view returns (uint256) { unchecked {
        require(supply > 0, "invalid supply");
        require(balance > 0, "invalid balance");
        require(MIN_WEIGHT <= weight && weight <= MAX_WEIGHT, "invalid weight");

        if (amount == 0)
            return 0;

        if (weight == MAX_WEIGHT)
            return IntegralMath.mulDivF(amount, supply, balance);

        (uint256 n, uint256 d) = pow(safeAdd(balance, amount), balance, weight, MAX_WEIGHT);
        return IntegralMath.mulDivF(supply, n, d) - supply;
    }}

    /**
      * @dev Sell pool tokens for reserve tokens
      *
      * @param supply   The total amount of pool tokens
      * @param balance  The amount of reserve tokens owned by the pool
      * @param weight   The weight of the reserve (represented in ppm)
      * @param amount   The amount of pool tokens provided
      *
      * @return balance * (1 - (1 - amount / supply) ^ (MAX_WEIGHT / weight))
    */
    function sell(uint256 supply, uint256 balance, uint256 weight, uint256 amount) public view returns (uint256) { unchecked {
        require(supply > 0, "invalid supply");
        require(balance > 0, "invalid balance");
        require(MIN_WEIGHT <= weight && weight <= MAX_WEIGHT, "invalid weight");
        require(amount <= supply, "invalid amount");

        if (amount == 0)
            return 0;

        if (amount == supply)
            return balance;

        if (weight == MAX_WEIGHT)
            return IntegralMath.mulDivF(amount, balance, supply);

        (uint256 n, uint256 d) = pow(supply, supply - amount, MAX_WEIGHT, weight);
        return IntegralMath.mulDivF(balance, n - d, n);
    }}

    /**
      * @dev Convert reserve tokens of one type to another
      *
      * @param balance1 The amount of source reserve tokens owned by the pool
      * @param weight1  The weight of the source reserve (represented in ppm)
      * @param balance2 The amount of target reserve tokens owned by the pool
      * @param weight2  The weight of the target reserve (represented in ppm)
      * @param amount   The amount of source reserve tokens provided
      *
      * @return balance2 * (1 - (balance1 / (balance1 + amount)) ^ (weight1 / weight2))
    */
    function convert(uint256 balance1, uint256 weight1, uint256 balance2, uint256 weight2, uint256 amount) public view returns (uint256) { unchecked {
        require(0 < balance1, "invalid source balance");
        require(0 < balance2, "invalid target balance");
        require(MIN_WEIGHT <= weight1 && weight1 <= MAX_WEIGHT, "invalid source weight");
        require(MIN_WEIGHT <= weight2 && weight2 <= MAX_WEIGHT, "invalid target weight");

        if (weight1 == weight2)
            return IntegralMath.mulDivF(balance2, amount, safeAdd(balance1, amount));

        (uint256 n, uint256 d) = pow(safeAdd(balance1, amount), balance1, weight1, weight2);
        return IntegralMath.mulDivF(balance2, n - d, n);
    }}

    /**
      * @dev Deposit reserve tokens for pool tokens
      *
      * @param supply   The total amount of pool tokens
      * @param balance  The amount of reserve tokens of the desired type owned by the pool
      * @param weights  The combined weights of the reserves (represented in ppm)
      * @param amount   The amount of reserve tokens of the desired type provided
      *
      * @return supply * ((amount / balance + 1) ^ (weights / MAX_WEIGHT) - 1)
    */
    function deposit(uint256 supply, uint256 balance, uint256 weights, uint256 amount) public view returns (uint256) { unchecked {
        require(supply > 0, "invalid supply");
        require(balance > 0, "invalid balance");
        require(MIN_WEIGHT * 2 <= weights && weights <= MAX_WEIGHT * 2, "invalid weights");

        if (amount == 0)
            return 0;

        if (weights == MAX_WEIGHT)
            return IntegralMath.mulDivF(amount, supply, balance);

        (uint256 n, uint256 d) = pow(safeAdd(balance, amount), balance, weights, MAX_WEIGHT);
        return IntegralMath.mulDivF(supply, n, d) - supply;
    }}

    /**
      * @dev Withdraw reserve tokens with pool tokens
      *
      * @param supply   The total amount of pool tokens
      * @param balance  The amount of reserve tokens of the desired type owned by the pool
      * @param weights  The combined weights of the reserves (represented in ppm)
      * @param amount   The amount of pool tokens provided
      *
      * @return balance * (1 - ((supply - amount) / supply) ^ (MAX_WEIGHT / weights))
    */
    function withdraw(uint256 supply, uint256 balance, uint256 weights, uint256 amount) public view returns (uint256) { unchecked {
        require(supply > 0, "invalid supply");
        require(balance > 0, "invalid balance");
        require(MIN_WEIGHT * 2 <= weights && weights <= MAX_WEIGHT * 2, "invalid weights");
        require(amount <= supply, "invalid amount");

        if (amount == 0)
            return 0;

        if (amount == supply)
            return balance;

        if (weights == MAX_WEIGHT)
            return IntegralMath.mulDivF(amount, balance, supply);

        (uint256 n, uint256 d) = pow(supply, supply - amount, MAX_WEIGHT, weights);
        return IntegralMath.mulDivF(balance, n - d, n);
    }}

    /**
      * @dev Invest reserve tokens for pool tokens
      *
      * @param supply   The total amount of pool tokens
      * @param balance  The amount of reserve tokens of the desired type owned by the pool
      * @param weights  The combined weights of the reserves (represented in ppm)
      * @param amount   The amount of pool tokens desired
      *
      * @return balance * (((supply + amount) / supply) ^ (MAX_WEIGHT / weights) - 1)
    */
    function invest(uint256 supply, uint256 balance, uint256 weights, uint256 amount) public view returns (uint256) { unchecked {
        require(supply > 0, "invalid supply");
        require(balance > 0, "invalid balance");
        require(MIN_WEIGHT * 2 <= weights && weights <= MAX_WEIGHT * 2, "invalid weights");

        if (amount == 0)
            return 0;

        if (weights == MAX_WEIGHT)
            return IntegralMath.mulDivC(amount, balance, supply);

        (uint256 n, uint256 d) = pow(safeAdd(supply, amount), supply, MAX_WEIGHT, weights);
        return IntegralMath.mulDivC(balance, n, d) - balance;
    }}
}
