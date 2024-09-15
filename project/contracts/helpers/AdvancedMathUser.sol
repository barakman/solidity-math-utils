// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity 0.8.27;

import "../AdvancedMath.sol";

contract AdvancedMathUser {
    function solve(uint256 a, uint256 b, uint256 c, uint256 d) external pure returns (uint256, uint256) {
        return AdvancedMath.solve(a, b, c, d);
    }

    function lambertNeg(uint256 x) external pure returns (uint256) {
        return AdvancedMath.lambertNeg(x);
    }

    function lambertPos(uint256 x) external pure returns (uint256) {
        return AdvancedMath.lambertPos(x);
    }
}
