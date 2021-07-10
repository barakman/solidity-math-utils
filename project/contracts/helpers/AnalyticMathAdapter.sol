// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity 0.8.6;

import "../AnalyticMath.sol";

contract AnalyticMathAdapter is AnalyticMath {
    function powTest(uint256 a, uint256 b, uint256 c, uint256 d) external view returns (uint256, uint256) {
        return super.pow(a, b, c, d);
    }

    function logTest(uint256 a, uint256 b) external pure returns (uint256, uint256) {
        return super.log(a, b);
    }

    function expTest(uint256 a, uint256 b) external view returns (uint256, uint256) {
        return super.exp(a, b);
    }

    function generalLogTest(uint256 x) external pure returns (uint256) {
        return super.generalLog(x);
    }

    function generalExpTest(uint256 x, uint8 precision) external pure returns (uint256) {
        return super.generalExp(x, precision);
    }

    function optimalLogTest(uint256 x) external pure returns (uint256) {
        return super.optimalLog(x);
    }

    function optimalExpTest(uint256 x) external pure returns (uint256) {
        return super.optimalExp(x);
    }

    function findPositionTest(uint256 x) external view returns (uint8) {
        return super.findPosition(x);
    }
}
