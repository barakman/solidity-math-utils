// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.34;

import "../AdvancedMath.sol";

contract AdvancedMathUser {
    function solveExact(uint256 a, uint256 b, uint256 c, uint256 d) external pure returns (uint256, uint256) {
        return AdvancedMath.solveExact(a, b, c, d);
    }

    function solveQuick(uint256 a, uint256 b, uint256 c, uint256 d) external pure returns (uint256, uint256) {
        return AdvancedMath.solveQuick(a, b, c, d);
    }

    function lambertNegExact(uint256 x) external pure returns (uint256) {
        return AdvancedMath.lambertNegExact(x);
    }

    function lambertPosExact(uint256 x) external pure returns (uint256) {
        return AdvancedMath.lambertPosExact(x);
    }

    function lambertNegQuick(uint256 x) external pure returns (uint256) {
        return AdvancedMath.lambertNegQuick(x);
    }

    function lambertPosQuick(uint256 x) external pure returns (uint256) {
        return AdvancedMath.lambertPosQuick(x);
    }
}
