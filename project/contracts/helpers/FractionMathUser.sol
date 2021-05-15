// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity 0.8.4;

import "../FractionMath.sol";

contract FractionMathUser {
    using FractionMath for *;

    function poweredRatio(uint256 baseN, uint256 baseD, uint256 exp) external pure returns (uint256, uint256) {
        return FractionMath.poweredRatio(baseN, baseD, exp);
    }

    function reducedRatio(uint256 baseN, uint256 baseD, uint256 max) external pure returns (uint256, uint256) {
        return FractionMath.reducedRatio(baseN, baseD, max);
    }

    function normalizedRatio(uint256 baseN, uint256 baseD, uint256 scale) external pure returns (uint256, uint256) {
        return FractionMath.normalizedRatio(baseN, baseD, scale);
    }
}
