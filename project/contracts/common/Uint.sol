// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity 0.8.6;

uint256 constant MAX_VAL = type(uint256).max;

// reverts on overflow
function safeAdd(uint256 x, uint256 y) pure returns (uint256) {
    return x + y;
}

// does not revert on overflow
function unsafeAdd(uint256 x, uint256 y) pure returns (uint256) { unchecked {
    return x + y;
}}

// does not revert on overflow
function unsafeSub(uint256 x, uint256 y) pure returns (uint256) { unchecked {
    return x - y;
}}

// does not revert on overflow
function unsafeMul(uint256 x, uint256 y) pure returns (uint256) { unchecked {
    return x * y;
}}

// does not overflow
function mulModMax(uint256 x, uint256 y) pure returns (uint256) { unchecked {
    return mulmod(x, y, MAX_VAL);
}}

// does not overflow
function mulMod(uint256 x, uint256 y, uint256 z) pure returns (uint256) { unchecked {
    return mulmod(x, y, z);
}}
