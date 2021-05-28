// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity 0.8.4;

import "./IntegralMath.sol";

library FractionMath {
    using IntegralMath for *;

    uint256 internal constant MAX_EXP_BIT_LEN = 4;
    uint256 internal constant MAX_EXP = 2 ** MAX_EXP_BIT_LEN - 1;
    uint256 internal constant MAX_UINT128 = 2 ** 128 - 1;
    uint256 internal constant MAX_UINT256 = 2 ** 256 - 1;

    /**
      * @dev Compute the power of a given ratio
      *
      * @param baseN The ratio numerator
      * @param baseD The ratio denominator
      * @param exp   The exponentiation value
      *
      * @return The powered ratio numerator
      * @return The powered ratio denominator
    */
    function poweredRatio(uint256 baseN, uint256 baseD, uint256 exp) internal pure returns (uint256, uint256) { unchecked {
        require(exp <= MAX_EXP, "exp too large");

        uint256[MAX_EXP_BIT_LEN] memory ns;
        uint256[MAX_EXP_BIT_LEN] memory ds;

        (ns[0], ds[0]) = reducedRatio(baseN, baseD, MAX_UINT128);
        for (uint256 i = 0; (exp >> i) > 1; ++i) {
            (ns[i + 1], ds[i + 1]) = reducedRatio(ns[i] ** 2, ds[i] ** 2, MAX_UINT128);
        }

        uint256 n = 1;
        uint256 d = 1;

        for (uint256 i = 0; (exp >> i) > 0; ++i) {
            if (((exp >> i) & 1) > 0) {
                (n, d) = reducedRatio(n * ns[i], d * ds[i], MAX_UINT128);
            }
        }

        return (n, d);
    }}

    /**
      * @dev Reduce the components of a given ratio
      *
      * @param baseN The ratio numerator
      * @param baseD The ratio denominator
      * @param max   The maximum desired value
      *
      * @return The reduced ratio numerator
      * @return The reduced ratio denominator
    */
    function reducedRatio(uint256 baseN, uint256 baseD, uint256 max) internal pure returns (uint256, uint256) { unchecked {
        if (baseN > max || baseD > max) {
            return normalizedRatio(baseN, baseD, max);
        }
        return (baseN, baseD);
    }}

    /**
      * @dev Compute a normalized ratio as `scale * n / (n + d)` and `scale * d / (n + d)`
      *
      * @param baseN The ratio numerator
      * @param baseD The ratio denominator
      * @param scale The desired scale
      *
      * @return The normalized ratio numerator
      * @return The normalized ratio denominator
    */
    function normalizedRatio(uint256 baseN, uint256 baseD, uint256 scale) internal pure returns (uint256, uint256) { unchecked {
        if (baseN <= baseD) {
            return accurateRatio(baseN, baseD, scale);
        }
        (uint256 d, uint256 n) = accurateRatio(baseD, baseN, scale);
        return (n, d);
    }}

    /**
      * @dev Compute a normalized ratio as `scale * n / (n + d)` and `scale * d / (n + d)`, assuming that `n <= d`
      *
      * @param baseN The ratio numerator
      * @param baseD The ratio denominator
      * @param scale The desired scale
      *
      * @return The normalized ratio numerator
      * @return The normalized ratio denominator
    */
    function accurateRatio(uint256 baseN, uint256 baseD, uint256 scale) private pure returns (uint256, uint256) { unchecked {
        uint256 maxVal = MAX_UINT256 / scale; // `MAX_UINT256 >= scale` hence `maxVal >= 1`
        if (maxVal < baseN) {
            // `maxVal < baseN <= MAX_UINT256` hence `maxVal < MAX_UINT256` hence `maxVal + 1` is safe
            // `maxVal + 1 >= 2` hence `baseN / (maxVal + 1) < MAX_UINT256` hence `baseN / (maxVal + 1) + 1` is safe
            uint256 c = baseN / (maxVal + 1) + 1;
            baseN /= c; // we can now safely compute `baseN * scale`
            baseD /= c;
        }

        if (baseN != baseD) {
            uint256 n = baseN * scale;
            uint256 d = Uint.unsafeAdd(baseN, baseD); // `baseN + baseD` can overflow
            if (d >= baseN) {
                // `baseN + baseD` did not overflow
                uint256 x = IntegralMath.roundDiv(n, d); // we can now safely compute `scale - x`
                uint256 y = scale - x;
                return (x, y);
            }
            if (n < baseD - (baseD - baseN) / 2) {
                return (0, scale); // `baseN * scale < (baseN + baseD) / 2 < MAX_UINT256 < baseN + baseD`
            }
            return (1, scale - 1); // `(baseN + baseD) / 2 < baseN * scale < MAX_UINT256 < baseN + baseD`
        }
        return (scale / 2, scale - scale / 2); // reflect the fact that `baseN <= baseD` at the beginning
    }}
}
