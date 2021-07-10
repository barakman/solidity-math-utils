// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity 0.8.6;

import "../FractionMath.sol";

contract FractionMathUser {
    using FractionMath for *;

    function poweredRatio(uint256 baseN, uint256 baseD, uint256 exp, bool fast) external pure returns (uint256, uint256) {
        return FractionMath.poweredRatio(baseN, baseD, exp, fast);
    }

    function productRatio(uint256 xn, uint256 yn, uint256 xd, uint256 yd) external pure returns (uint256, uint256) {
        return FractionMath.productRatio(xn, yn, xd, yd);
    }

    function reducedRatio(uint256 baseN, uint256 baseD, uint256 max) external pure returns (uint256, uint256) {
        return FractionMath.reducedRatio(baseN, baseD, max);
    }

    function normalizedRatio(uint256 baseN, uint256 baseD, uint256 scale) external pure returns (uint256, uint256) {
        return FractionMath.normalizedRatio(baseN, baseD, scale);
    }
}
