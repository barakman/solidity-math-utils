// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity 0.8.4;

import "../IntegralMath.sol";

contract IntegralMathUser {
    using IntegralMath for *;

    function roundDiv(uint256 n, uint256 d) external pure returns (uint256) {
        return IntegralMath.roundDiv(n, d);
    }

    function floorLog2(uint256 n) external pure returns (uint8) {
        return IntegralMath.floorLog2(n);
    }

    function floorSqrt(uint256 n) external pure returns (uint256) {
        return IntegralMath.floorSqrt(n);
    }

    function ceilSqrt(uint256 n) external pure returns (uint256) {
        return IntegralMath.ceilSqrt(n);
    }
}
