// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.34;

function unsafeAdd(uint256 x, uint256 y) pure returns (uint256) { unchecked {
    return x + y;
}}

function unsafeSub(uint256 x, uint256 y) pure returns (uint256) { unchecked {
    return x - y;
}}

function unsafeMul(uint256 x, uint256 y) pure returns (uint256) { unchecked {
    return x * y;
}}
