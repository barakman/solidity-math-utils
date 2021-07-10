// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity 0.8.6;

import "../AdvancedMath.sol";

contract AdvancedMathAdapter is AdvancedMath {
    function solveTest(uint256 a, uint256 b, uint256 c, uint256 d) external view returns (uint256, uint256) {
        return super.solve(a, b, c, d);
    }

    function lambertNegTest(uint256 x) external pure returns (uint256) {
        return super.lambertNeg(x);
    }

    function lambertPosTest(uint256 x) external view returns (uint256) {
        return super.lambertPos(x);
    }

    function lambertNeg1Test(uint256 x) external pure returns (uint256) {
        return super.lambertNeg1(x);
    }

    function lambertPos1Test(uint256 x) external pure returns (uint256) {
        return super.lambertPos1(x);
    }

    function lambertPos2Test(uint256 x) external view returns (uint256) {
        return super.lambertPos2(x);
    }

    function lambertPos3Test(uint256 x) external pure returns (uint256) {
        return super.lambertPos3(x);
    }

    function maxInputValues() external pure returns (uint256[3] memory) {
        return [LAMBERT_CONV_RADIUS, LAMBERT_POS2_MAXVAL, LAMBERT_POS3_MAXVAL];
    }
}
