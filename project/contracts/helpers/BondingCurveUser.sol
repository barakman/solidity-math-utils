// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity 0.8.27;

import "../BondingCurve.sol";

contract BondingCurveUser {
    function buy(uint256 supply, uint256 balance, uint256 weight, uint256 amount) external pure returns (uint256) {
        return BondingCurve.buy(supply, balance, weight, amount);
    }

    function sell(uint256 supply, uint256 balance, uint256 weight, uint256 amount) external pure returns (uint256) {
        return BondingCurve.sell(supply, balance, weight, amount);
    }

    function convert(uint256 balance1, uint256 weight1, uint256 balance2, uint256 weight2, uint256 amount) external pure returns (uint256) {
        return BondingCurve.convert(balance1, weight1, balance2, weight2, amount);
    }

    function deposit(uint256 supply, uint256 balance, uint256 weights, uint256 amount) external pure returns (uint256) {
        return BondingCurve.deposit(supply, balance, weights, amount);
    }

    function withdraw(uint256 supply, uint256 balance, uint256 weights, uint256 amount) external pure returns (uint256) {
        return BondingCurve.withdraw(supply, balance, weights, amount);
    }

    function invest(uint256 supply, uint256 balance, uint256 weights, uint256 amount) external pure returns (uint256) {
        return BondingCurve.invest(supply, balance, weights, amount);
    }
}
