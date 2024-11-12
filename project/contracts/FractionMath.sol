// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity 0.8.28;

import "./IntegralMath.sol";

library FractionMath {
    uint256 internal constant MAX_EXP_BIT_LEN = 4;
    uint256 internal constant MAX_EXP = 2 ** MAX_EXP_BIT_LEN - 1;
    uint256 internal constant MAX_UINT128 = type(uint128).max;

    /**
      * @dev Compute the power of a given ratio while opting for accuracy over performance
      *
      * @param n The ratio numerator
      * @param d The ratio denominator
      * @param exp The exponentiation value
      *
      * @return The powered ratio numerator
      * @return The powered ratio denominator
    */
    function poweredRatioExact(uint256 n, uint256 d, uint256 exp) internal pure returns (uint256, uint256) { unchecked {
        return poweredRatio(n, d, exp, productRatio);
    }}

    /**
      * @dev Compute the power of a given ratio while opting for performance over accuracy
      *
      * @param n The ratio numerator
      * @param d The ratio denominator
      * @param exp The exponentiation value
      *
      * @return The powered ratio numerator
      * @return The powered ratio denominator
    */
    function poweredRatioQuick(uint256 n, uint256 d, uint256 exp) internal pure returns (uint256, uint256) { unchecked {
        return poweredRatio(n, d, exp, mulRatio128);
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
        uint256 n = IntegralMath.minFactor(xn, yn);
        uint256 d = IntegralMath.minFactor(xd, yd);
        uint256 z = n > d ? n : d;
        return (IntegralMath.mulDivC(xn, yn, z), IntegralMath.mulDivC(xd, yd, z));
    }}

    /**
      * @dev Reduce the components of a given ratio
      *
      * @param n The ratio numerator
      * @param d The ratio denominator
      * @param max The maximum desired value
      *
      * @return The reduced ratio numerator
      * @return The reduced ratio denominator
    */
    function reducedRatio(uint256 n, uint256 d, uint256 max) internal pure returns (uint256, uint256) { unchecked {
        uint256 scale = ((n > d ? n : d) - 1) / max + 1;
        return (n / scale, d / scale);
    }}

    /**
      * @dev Compute a normalized ratio as `scale * n / (n + d)` and `scale * d / (n + d)`
      *
      * @param n The ratio numerator
      * @param d The ratio denominator
      * @param scale The desired scale
      *
      * @return The normalized ratio numerator
      * @return The normalized ratio denominator
    */
    function normalizedRatio(uint256 n, uint256 d, uint256 scale) internal pure returns (uint256, uint256) { unchecked {
        if (n <= d) {
            return estimatedRatio(n, d, scale);
        }
        (d, n) = estimatedRatio(d, n, scale);
        return (n, d);
    }}

    /**
      * @dev Compute an estimated ratio as `scale * n / (n + d)` and `scale * d / (n + d)`, assuming that `n <= d`
      *
      * @param n The ratio numerator
      * @param d The ratio denominator
      * @param scale The desired scale
      *
      * @return The estimated ratio numerator
      * @return The estimated ratio denominator
    */
    function estimatedRatio(uint256 n, uint256 d, uint256 scale) private pure returns (uint256, uint256) { unchecked {
        uint256 x = MAX_VAL / scale;
        if (n > x) {
            // `n * scale` will overflow
            uint256 y = (n - 1) / x + 1;
            n /= y;
            d /= y;
            // `n * scale` will not overflow
        }

        if (n < d) {
            uint256 p = n * scale;
            uint256 q = unsafeAdd(n, d); // `n + d` can overflow
            if (q >= n) {
                // `n + d` did not overflow
                uint256 r = IntegralMath.roundDiv(p, q);
                return (r, scale - r); // `r = n * scale / (n + d) < scale`
            }
            if (p < d - (d - n) / 2) {
                return (0, scale); // `n * scale < (n + d) / 2 < MAX_VAL < n + d`
            }
            return (1, scale - 1); // `(n + d) / 2 < n * scale < MAX_VAL < n + d`
        }
        return (scale / 2, scale - scale / 2); // reflect the fact that initially `n <= d`
    }}

    /**
      * @dev Compute the power of a given ratio
      *
      * @param n The ratio numerator
      * @param d The ratio denominator
      * @param exp The exponentiation value
      * @param safeRatio The computing function
      *
      * @return The powered ratio numerator
      * @return The powered ratio denominator
    */
    function poweredRatio(
        uint256 n, uint256 d, uint256 exp,
        function (uint256, uint256, uint256, uint256) pure returns (uint256, uint256) safeRatio
    ) private pure returns (uint256, uint256) { unchecked {
        require(exp <= MAX_EXP, "exp too large");

        uint256[MAX_EXP_BIT_LEN] memory ns;
        uint256[MAX_EXP_BIT_LEN] memory ds;

        (ns[0], ds[0]) = safeRatio(n, 1, d, 1);
        for (uint256 i = 0; (exp >> i) > 1; ++i) {
            (ns[i + 1], ds[i + 1]) = safeRatio(ns[i], ns[i], ds[i], ds[i]);
        }

        n = 1;
        d = 1;

        for (uint256 i = 0; (exp >> i) > 0; ++i) {
            if (((exp >> i) & 1) > 0) {
                (n, d) = safeRatio(n, ns[i], d, ds[i]);
            }
        }

        return (n, d);
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
