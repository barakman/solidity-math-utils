// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity 0.8.6;

import "./AdvancedMath.sol";

contract DynamicCurve is AdvancedMath {
    uint256 private constant MAX_WEIGHT = 1000000;

    /**
      * @dev Consider a pool which implements the bonding-curve model over a primary reserve token and a secondary reserve token.
      * Let 'on-chain price' denote the conversion rate between these tokens inside the pool (i.e., as determined by the pool).
      * Let 'off-chain price' denote the conversion rate between these tokens outside the pool (i.e., as determined by the market).
      * The arbitrage incentive is always to convert to the point where the on-chain price is equal to the off-chain price.
      * We want this operation to also impact the primary reserve balance becoming equal to the primary reserve staked balance.
      * In other words, we want the arbitrager to convert the difference between the reserve balance and the reserve staked balance.
      * Hence we adjust the weights in order to create an arbitrage incentive which, when realized, will subsequently equalize the pool.
      *
      * Input:
      * - Let t denote the primary reserve token staked balance
      * - Let s denote the primary reserve token balance
      * - Let r denote the secondary reserve token balance
      * - Let q denote the numerator of the off-chain price
      * - Let p denote the denominator of the off-chain price
      * Where p primary tokens are equal to q secondary tokens
      *
      * Output:
      * - Solve the equation x * (s / t) ^ x = (t / r) * (q / p)
      * - Return x / (x + 1) as the weight of the primary reserve token
      * - Return 1 / (x + 1) as the weight of the secondary reserve token
      *
      * If the rate-provider provides the rates for a common unit, for example:
      * - P = 2 ==> 2 primary reserve tokens = 1 ether
      * - Q = 3 ==> 3 secondary reserve tokens = 1 ether
      * Then you can simply use p = P and q = Q
      *
      * If the rate-provider provides the rates for a single unit, for example:
      * - P = 2 ==> 1 primary reserve token = 2 ethers
      * - Q = 3 ==> 1 secondary reserve token = 3 ethers
      * Then you can simply use p = Q and q = P
      *
      * @param t The primary reserve token staked balance
      * @param s The primary reserve token balance
      * @param r The secondary reserve token balance
      * @param q The numerator of the off-chain price
      * @param p The denominator of the off-chain price
      *
      * Note that `numerator / denominator` should represent the amount of secondary tokens equal to one primary token
      *
      * @return The weight of the primary reserve token and the weight of the secondary reserve token, both in ppm units
    */
    function equalize(uint256 t, uint256 s, uint256 r, uint256 q, uint256 p) public view returns (uint256, uint256) { unchecked {
        if (t == s)
            require(t > 0 || r > 0, "invalid balance");
        else
            require(t > 0 && s > 0 && r > 0, "invalid balance");
        require(q > 0 && p > 0, "invalid rate");

        (uint256 tq, uint256 rp) = FractionMath.productRatio(t, q, r, p);
        (uint256 xn, uint256 xd) = solve(s, t, tq, rp);
        (uint256 w1, uint256 w2) = FractionMath.normalizedRatio(xn, xd, MAX_WEIGHT);

        return (w1, w2);
    }}
}
