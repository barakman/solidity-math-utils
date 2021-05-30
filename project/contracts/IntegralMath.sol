// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity 0.8.4;

import "./common/Uint.sol";

library IntegralMath {
    /**
      * @dev Compute the nearest integer to the quotient of `n / d`
    */
    function roundDiv(uint256 n, uint256 d) internal pure returns (uint256) { unchecked {
        return n / d + (n % d) / (d - d / 2);
    }}

    /**
      * @dev Compute the largest integer smaller than or equal to the binary logarithm of `n`
    */
    function floorLog2(uint256 n) internal pure returns (uint8) { unchecked {
        uint8 res = 0;

        if (n < 256) {
            // at most 8 iterations
            while (n > 1) {
                n >>= 1;
                res += 1;
            }
        }
        else {
            // exactly 8 iterations
            for (uint8 s = 128; s > 0; s >>= 1) {
                if (n >= 1 << s) {
                    n >>= s;
                    res |= s;
                }
            }
        }

        return res;
    }}

    /**
      * @dev Compute the largest integer smaller than or equal to the square root of `n`
    */
    function floorSqrt(uint256 n) internal pure returns (uint256) { unchecked {
        if (n > 0) {
            uint256 x = n / 2 + 1;
            uint256 y = (x + n / x) / 2;
            while (x > y) {
                x = y;
                y = (x + n / x) / 2;
            }
            return x;
        }
        return 0;
    }}

    /**
      * @dev Compute the smallest integer larger than or equal to the square root of `n`
    */
    function ceilSqrt(uint256 n) internal pure returns (uint256) { unchecked {
        uint256 x = floorSqrt(n);
        return x * x == n ? x : x + 1;
    }}

    /**
      * @dev Compute the largest integer smaller than or equal to `x * y / z`
    */
    function mulDivF(uint256 x, uint256 y, uint256 z) internal pure returns (uint256) { unchecked {
        (uint256 xyh, uint256 xyl) = mul512(x, y);
        if (xyh > 0)
            return div512(xyh, xyl, z);
        return xyl / z;
    }}

    /**
      * @dev Compute the smallest integer larger than or equal to `x * y / z`
    */
    function mulDivC(uint256 x, uint256 y, uint256 z) internal pure returns (uint256) { unchecked {
        uint256 w = mulDivF(x, y, z);
        if (mulMod(x, y, z) > 0)
            return safeAdd(w, 1);
        return w;
    }}

    /**
      * @dev Compute the value of `x * y`
    */
    function mul512(uint256 x, uint256 y) private pure returns (uint256, uint256) { unchecked {
        uint256 p = mulModMax(x, y);
        uint256 q = unsafeMul(x, y);
        if (p >= q)
            return (p - q, q);
        return (unsafeSub(p, q) - 1, q);
    }}

    /**
      * @dev Compute the largest integer smaller than or equal to `(2 ^ 256 * xh + xl) / y`
    */
    function div512(uint256 xh, uint256 xl, uint256 y) private pure returns (uint256) { unchecked {
        require(xh < y);
        uint256 result = 0;
        uint256 length = 255 - floorLog2(y);
        while (xh > 0) {
            uint256 bits = floorLog2(xh) + length;
            result += 1 << bits;
            (uint256 yh, uint256 yl) = shl512(y, bits);
            (xh, xl) = sub512(xh, xl, yh, yl);
        }
        return result + xl / y;
    }}

    /**
      * @dev Compute the value of `x * 2 ^ y`
    */
    function shl512(uint256 x, uint256 y) private pure returns (uint256, uint256) { unchecked {
        return (x >> (256 - y), unsafeShl(x, y));
    }}

    /**
      * @dev Compute the value of `2 ^ 256 * xh + xl - 2 ^ 256 * yh - yl`
    */
    function sub512(uint256 xh, uint256 xl, uint256 yh, uint256 yl) private pure returns (uint256, uint256) { unchecked {
        if (xl >= yl)
            return (xh - yh, xl - yl);
        return (xh - yh - 1, unsafeSub(xl, yl));
    }}
}
