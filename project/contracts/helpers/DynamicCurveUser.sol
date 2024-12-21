// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity 0.8.28;

import "../DynamicCurve.sol";

contract DynamicCurveUser {
    function equalizeExact(uint256 t, uint256 s, uint256 r, uint256 q, uint256 p) external pure returns (uint256, uint256) {
        return DynamicCurve.equalizeExact(t, s, r, q, p);
    }

    function equalizeQuick(uint256 t, uint256 s, uint256 r, uint256 q, uint256 p) external pure returns (uint256, uint256) {
        return DynamicCurve.equalizeQuick(t, s, r, q, p);
    }
}
