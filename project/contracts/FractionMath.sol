// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity 0.8.6;

import "./IntegralMath.sol";

library FractionMath {
    using IntegralMath for *;

    uint256 internal constant MAX_EXP_BIT_LEN = 4;
    uint256 internal constant MAX_EXP = 2 ** MAX_EXP_BIT_LEN - 1;
    uint256 internal constant MAX_UINT128 = type(uint128).max;

    /**
      * @dev Compute the power of a given ratio
      *
      * @param baseN The ratio numerator
      * @param baseD The ratio denominator
      * @param exp   The exponentiation value
      * @param fast  Opt for accuracy or performance
      *
      * @return The powered ratio numerator
      * @return The powered ratio denominator
    */
    function poweredRatio(uint256 baseN, uint256 baseD, uint256 exp, bool fast) internal pure returns (uint256, uint256) { unchecked {
        require(exp <= MAX_EXP, "exp too large");

        function (uint256, uint256, uint256, uint256) pure returns (uint256, uint256) safeRatio = fast ? mulRatio128 : productRatio;

        uint256[MAX_EXP_BIT_LEN] memory ns;
        uint256[MAX_EXP_BIT_LEN] memory ds;

        (ns[0], ds[0]) = safeRatio(baseN, 1, baseD, 1);
        for (uint256 i = 0; (exp >> i) > 1; ++i) {
            (ns[i + 1], ds[i + 1]) = safeRatio(ns[i], ns[i], ds[i], ds[i]);
        }

        uint256 n = 1;
        uint256 d = 1;

        for (uint256 i = 0; (exp >> i) > 0; ++i) {
            if (((exp >> i) & 1) > 0) {
                (n, d) = safeRatio(n, ns[i], d, ds[i]);
            }
        }

        return (n, d);
    }}

    /**
      * @dev Compute the product of two given ratios
      *
      * @param xn The 1st ratio numerator
      * @param yn The 2nd ratio numerator
      * @param xd The 1st ratio denominator
      * @param yd The 2nd ratio denominator
      *
      * @return The product ratio numerator
      * @return The product ratio denominator
    */
    function productRatio(uint256 xn, uint256 yn, uint256 xd, uint256 yd) internal pure returns (uint256, uint256) { unchecked {
        uint256 n = IntegralMath.mulDivC(xn, yn, MAX_VAL);
        uint256 d = IntegralMath.mulDivC(xd, yd, MAX_VAL);
        uint256 z = n > d ? n : d;
        if (z > 1) {
            return (IntegralMath.mulDivC(xn, yn, z), IntegralMath.mulDivC(xd, yd, z));
        }
        return (xn * yn, xd * yd);
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
            return estimatedRatio(baseN, baseD, scale);
        }
        (uint256 d, uint256 n) = estimatedRatio(baseD, baseN, scale);
        return (n, d);
    }}

    /**
      * @dev Compute an estimated ratio as `scale * n / (n + d)` and `scale * d / (n + d)`, assuming that `n <= d`
      *
      * @param baseN The ratio numerator
      * @param baseD The ratio denominator
      * @param scale The desired scale
      *
      * @return The estimated ratio numerator
      * @return The estimated ratio denominator
    */
    function estimatedRatio(uint256 baseN, uint256 baseD, uint256 scale) private pure returns (uint256, uint256) { unchecked {
        uint256 maxN = MAX_VAL / scale; // `MAX_VAL >= scale` hence `maxN >= 1`
        if (maxN < baseN) {
            // `maxN < baseN <= MAX_VAL` hence `maxN < MAX_VAL` hence `maxN + 1` is safe
            // `maxN + 1 >= 2` hence `baseN / (maxN + 1) < MAX_VAL` hence `baseN / (maxN + 1) + 1` is safe
            uint256 c = baseN / (maxN + 1) + 1;
            baseN /= c; // we can now safely compute `baseN * scale`
            baseD /= c;
        }

        if (baseN != baseD) {
            uint256 n = baseN * scale;
            uint256 d = unsafeAdd(baseN, baseD); // `baseN + baseD` can overflow
            if (d >= baseN) {
                // `baseN + baseD` did not overflow
                uint256 x = IntegralMath.roundDiv(n, d); // we can now safely compute `scale - x`
                uint256 y = scale - x;
                return (x, y);
            }
            if (n < baseD - (baseD - baseN) / 2) {
                return (0, scale); // `baseN * scale < (baseN + baseD) / 2 < MAX_VAL < baseN + baseD`
            }
            return (1, scale - 1); // `(baseN + baseD) / 2 < baseN * scale < MAX_VAL < baseN + baseD`
        }
        return (scale / 2, scale - scale / 2); // reflect the fact that initially `baseN <= baseD`
    }}

    /**
      * @dev Compute the product of two ratios and reduce the components of the result to 128 bits,
      * under the implicit assumption that the components of the product are not larger than 256 bits
      *
      * @param xn The 1st ratio numerator
      * @param yn The 2nd ratio numerator
      * @param xd The 1st ratio denominator
      * @param yd The 2nd ratio denominator
      *
      * @return The product ratio numerator
      * @return The product ratio denominator
    */
    function mulRatio128(uint256 xn, uint256 yn, uint256 xd, uint256 yd) private pure returns (uint256, uint256) { unchecked {
        return reducedRatio(xn * yn, xd * yd, MAX_UINT128);
    }}
}
