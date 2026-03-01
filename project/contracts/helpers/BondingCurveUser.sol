// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.34;

import "../BondingCurve.sol";

contract BondingCurveUser {
    function mintGain(uint256 supply, uint256 balance, uint256 weight, uint256 weights, uint256 amount) external pure returns (uint256) {
        return BondingCurve.mintGain(supply, balance, weight, weights, amount);
    }

    function mintCost(uint256 supply, uint256 balance, uint256 weight, uint256 weights, uint256 amount) external pure returns (uint256) {
        return BondingCurve.mintCost(supply, balance, weight, weights, amount);
    }

    function burnGain(uint256 supply, uint256 balance, uint256 weight, uint256 weights, uint256 amount) external pure returns (uint256) {
        return BondingCurve.burnGain(supply, balance, weight, weights, amount);
    }

    function burnCost(uint256 supply, uint256 balance, uint256 weight, uint256 weights, uint256 amount) external pure returns (uint256) {
        return BondingCurve.burnCost(supply, balance, weight, weights, amount);
    }

    function swapGain(uint256 balance1, uint256 balance2, uint256 weight1, uint256 weight2, uint256 amount) external pure returns (uint256) {
        return BondingCurve.swapGain(balance1, balance2, weight1, weight2, amount);
    }

    function swapCost(uint256 balance1, uint256 balance2, uint256 weight1, uint256 weight2, uint256 amount) external pure returns (uint256) {
        return BondingCurve.swapCost(balance1, balance2, weight1, weight2, amount);
    }
}
