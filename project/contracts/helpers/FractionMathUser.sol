// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity 0.8.28;

import "../FractionMath.sol";

contract FractionMathUser {
    function poweredRatioExact(uint256 n, uint256 d, uint256 exp) external pure returns (uint256, uint256) {
        return FractionMath.poweredRatioExact(n, d, exp);
    }

    function poweredRatioQuick(uint256 n, uint256 d, uint256 exp) external pure returns (uint256, uint256) {
        return FractionMath.poweredRatioQuick(n, d, exp);
    }

    function productRatio(uint256 xn, uint256 yn, uint256 xd, uint256 yd) external pure returns (uint256, uint256) {
        return FractionMath.productRatio(xn, yn, xd, yd);
    }

    function reducedRatio(uint256 n, uint256 d, uint256 max) external pure returns (uint256, uint256) {
        return FractionMath.reducedRatio(n, d, max);
    }

    function normalizedRatio(uint256 n, uint256 d, uint256 scale) external pure returns (uint256, uint256) {
        return FractionMath.normalizedRatio(n, d, scale);
    }
}
