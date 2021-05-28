// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity 0.8.4;

library Uint {
    // reverts on overflow
    function safeAdd(uint256 x, uint256 y) internal pure returns (uint256) {
        return x + y;
    }

    // reverts on overflow
    function safeMul(uint256 x, uint256 y) internal pure returns (uint256) {
        return x * y;
    }

    // reverts on overflow
    function safeAdd1(uint256 x) internal pure returns (uint256) { unchecked {
        require(x < type(uint256).max);
        return x + 1;
    }}

    // reverts on overflow
    function safeShl1(uint256 x) internal pure returns (uint256) { unchecked {
        require(x < 256);
        return 1 << x;
    }}

    // does not revert on overflow
    function unsafeAdd(uint256 x, uint256 y) internal pure returns (uint256) { unchecked {
        return x + y;
    }}

    // does not revert on overflow
    function unsafeSub(uint256 x, uint256 y) internal pure returns (uint256) { unchecked {
        return x - y;
    }}

    // does not revert on overflow
    function unsafeMul(uint256 x, uint256 y) internal pure returns (uint256) { unchecked {
        return x * y;
    }}

    // does not revert on overflow
    function unsafeShl(uint256 x, uint256 y) internal pure returns (uint256) { unchecked {
        return x << y;
    }}

    // does not overflow
    function mulModMax(uint256 x, uint256 y) internal pure returns (uint256) { unchecked {
        return mulmod(x, y, type(uint256).max);
    }}

    // does not overflow
    function mulMod(uint256 x, uint256 y, uint256 z) internal pure returns (uint256) { unchecked {
        return mulmod(x, y, z);
    }}
}
