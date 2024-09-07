// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity 0.8.27;

import "../DynamicCurve.sol";

contract DynamicCurveUser {
    function equalize(uint256 t, uint256 s, uint256 r, uint256 q, uint256 p) external pure returns (uint256, uint256) {
        return DynamicCurve.equalize(t, s, r, q, p);
    }
}
