// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity 0.8.30;

import "../AnalyticMath.sol";

contract AnalyticMathUser {
    function pow(uint256 a, uint256 b, uint256 c, uint256 d) external pure returns (uint256, uint256) {
        return AnalyticMath.pow(a, b, c, d);
    }

    function log(uint256 a, uint256 b) external pure returns (uint256, uint256) {
        return AnalyticMath.log(a, b);
    }

    function exp(uint256 a, uint256 b) external pure returns (uint256, uint256) {
        return AnalyticMath.exp(a, b);
    }

    function fixedLog(uint256 x) external pure returns (uint256) {
        return AnalyticMath.fixedLog(x);
    }

    function fixedExp(uint256 x) external pure returns (uint256) {
        return AnalyticMath.fixedExp(x);
    }
}
