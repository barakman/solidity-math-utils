// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity 0.8.4;

contract Safe {
    /**
      * @dev Revert on overflow
    */
    function add(uint256 x, uint256 y) internal pure returns (uint256) {
        return x + y;
    }

    /**
      * @dev Revert on overflow
    */
    function mul(uint256 x, uint256 y) internal pure returns (uint256) {
        return x * y;
    }
}
