// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity 0.8.6;

import "../IntegralMath.sol";

contract IntegralMathUser {
    using IntegralMath for *;

    function floorLog2(uint256 n) external pure returns (uint8) {
        return IntegralMath.floorLog2(n);
    }

    function floorSqrt(uint256 n) external pure returns (uint256) {
        return IntegralMath.floorSqrt(n);
    }

    function ceilSqrt(uint256 n) external pure returns (uint256) {
        return IntegralMath.ceilSqrt(n);
    }

    function floorCbrt(uint256 n) external pure returns (uint256) {
        return IntegralMath.floorCbrt(n);
    }

    function ceilCbrt(uint256 n) external pure returns (uint256) {
        return IntegralMath.ceilCbrt(n);
    }

    function roundDiv(uint256 n, uint256 d) external pure returns (uint256) {
        return IntegralMath.roundDiv(n, d);
    }

    function mulDivF(uint256 x, uint256 y, uint256 z) external pure returns (uint256) {
        return IntegralMath.mulDivF(x, y, z);
    }

    function mulDivC(uint256 x, uint256 y, uint256 z) external pure returns (uint256) {
        return IntegralMath.mulDivC(x, y, z);
    }
}
