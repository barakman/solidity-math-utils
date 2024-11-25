// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity 0.8.28;

import "./common/Uint.sol";

library IntegralMath {
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
        return x ** 2 == n ? x : x + 1;
    }}

    /**
      * @dev Compute the largest integer smaller than or equal to the cubic root of `n`
    */
    function floorCbrt(uint256 n) internal pure returns (uint256) { unchecked {
        uint256 x = 0;
        for (uint256 y = 1 << 255; y > 0; y >>= 3) {
            x <<= 1;
            uint256 z = 3 * x * (x + 1) + 1;
            if (n / y >= z) {
                n -= y * z;
                x += 1;
            }
        }
        return x;
    }}

    /**
      * @dev Compute the smallest integer larger than or equal to the cubic root of `n`
    */
    function ceilCbrt(uint256 n) internal pure returns (uint256) { unchecked {
        uint256 x = floorCbrt(n);
        return x ** 3 == n ? x : x + 1;
    }}

    /**
      * @dev Compute the nearest integer to the quotient of `n` and `d` (or `n / d`)
    */
    function roundDiv(uint256 n, uint256 d) internal pure returns (uint256) { unchecked {
        return n / d + (n % d) / (d - d / 2);
    }}

    /**
      * @dev Compute the smallest integer `z` such that `x * y / z <= 2 ^ 256 - 1`
    */
    function minFactor(uint256 x, uint256 y) internal pure returns (uint256) { unchecked {
        (uint256 hi, uint256 lo) = mul512(x, y);
        return hi > ~lo ? hi + 2 : hi + 1;
        // General:
        // - find the smallest integer `z` such that `x * y / z <= 2 ^ 256 - 1`
        // - the value of `x * y` is represented via `2 ^ 256 * hi + lo`
        // - the expression `~lo` is equivalent to `2 ^ 256 - 1 - lo`
        // 
        // Safety:
        // - if `x < 2 ^ 256 - 1` or `y < 2 ^ 256 - 1`
        //   then `hi < 2 ^ 256 - 2`
        //   hence neither `hi + 1` nor `hi + 2` overflows
        // - if `x = 2 ^ 256 - 1` and `y = 2 ^ 256 - 1`
        //   then `hi = 2 ^ 256 - 2 = ~lo`
        //   hence `hi + 1`, which does not overflow, is computed
        // 
        // Symbols:
        // - let `H` denote `hi`
        // - let `L` denote `lo`
        // - let `N` denote `2 ^ 256 - 1`
        // 
        // Inference:
        // `x * y / z <= 2 ^ 256 - 1`     <-->
        // `x * y / (2 ^ 256 - 1) <= z`   <-->
        // `((N + 1) * H + L) / N <= z`   <-->
        // `(N * H + H + L) / N <= z`     <-->
        // `H + (H + L) / N <= z`
        // 
        // Inference:
        // `0 <= H <= N && 0 <= L <= N`   <-->
        // `0 <= H + L <= N + N`          <-->
        // `0 <= H + L <= N * 2`          <-->
        // `0 <= (H + L) / N <= 2`
        // 
        // Inference:
        // - `0 = (H + L) / N` --> `H + L = 0` --> `x * y = 0` --> `z = 1 = H + 1`
        // - `0 < (H + L) / N <= 1` --> `H + (H + L) / N <= H + 1` --> `z = H + 1`
        // - `1 < (H + L) / N <= 2` --> `H + (H + L) / N <= H + 2` --> `z = H + 2`
        // 
        // Implementation:
        // - if `hi > ~lo`:
        //   `~L < H <= N`                         <-->
        //   `N - L < H <= N`                      <-->
        //   `N < H + L <= N + L`                  <-->
        //   `1 < (H + L) / N <= 2`                <-->
        //   `H + 1 < H + (H + L) / N <= H + 2`    <-->
        //   `z = H + 2`
        // - if `hi <= ~lo`:
        //   `H <= ~L`                             <-->
        //   `H <= N - L`                          <-->
        //   `H + L <= N`                          <-->
        //   `(H + L) / N <= 1`                    <-->
        //   `H + (H + L) / N <= H + 1`            <-->
        //   `z = H + 1`
    }}

    /**
      * @dev Compute the largest integer smaller than or equal to `x * y / z`
    */
    function mulDivF(uint256 x, uint256 y, uint256 z) internal pure returns (uint256) { unchecked {
        (uint256 xyh, uint256 xyl) = mul512(x, y);
        if (xyh == 0) { // `x * y < 2 ^ 256`
            return xyl / z;
        }
        if (xyh < z) { // `x * y / z < 2 ^ 256`
            uint256 m = mulmod(x, y, z);                    // `m = x * y % z`
            (uint256 nh, uint256 nl) = sub512(xyh, xyl, m); // `n = x * y - m` hence `n / z = floor(x * y / z)`
            if (nh == 0) { // `n < 2 ^ 256`
                return nl / z;
            }
            uint256 p = unsafeSub(0, z) & z; // `p` is the largest power of 2 which `z` is divisible by
            uint256 q = div512(nh, nl, p);   // `n` is divisible by `p` because `n` is divisible by `z` and `z` is divisible by `p`
            uint256 r = inv256(z / p);       // `z / p = 1 mod 2` hence `inverse(z / p) = 1 mod 2 ^ 256`
            return unsafeMul(q, r);          // `q * r = (n / p) * inverse(z / p) = n / z`
        }
        revert(); // `x * y / z >= 2 ^ 256`
    }}

    /**
      * @dev Compute the smallest integer larger than or equal to `x * y / z`
    */
    function mulDivC(uint256 x, uint256 y, uint256 z) internal pure returns (uint256) { unchecked {
        uint256 w = mulDivF(x, y, z);
        if (mulmod(x, y, z) > 0)
            return safeAdd(w, 1);
        return w;
    }}

    /**
      * @dev Compute the nearest integer smaller than or larger than `x * y / z`
    */
    function mulDivR(uint256 x, uint256 y, uint256 z) internal pure returns (uint256) { unchecked {
        uint256 w = mulDivF(x, y, z);
        if (mulmod(x, y, z) > (z - 1) / 2)
            return safeAdd(w, 1);
        return w;
    }}

    /**
      * @dev Compute the largest integer smaller than or equal to `(x * y) / (z * w)`
    */
    function mulDivExF(uint256 x, uint256 y, uint256 z, uint256 w) internal pure returns (uint256) { unchecked {
        (uint256 zwh, uint256 zwl) = mul512(z, w);
        if (zwh > 0) {
            uint256 res = 0;
            (uint256 xyh, uint256 xyl) = mul512(x, y);
            if (xyh > zwh) {
                uint8 xyhn = floorLog2(xyh);
                uint8 zwhn = floorLog2(zwh);
                while (xyhn > zwhn) {
                    uint8 n = xyhn - zwhn - 1;
                    res += 1 << n; // set `res = res + 2 ^ n`
                    (xyh, xyl) = sub512Ex(xyh, xyl, (zwh << n) | (zwl >> (256 - n)), zwl << n); // set `xy = xy - zw * 2 ^ n`
                    xyhn = floorLog2(xyh);
                }
            }
            if (xyh > zwh || (xyh == zwh && xyl >= zwl)) // `xy >= zw`
                return res + 1;
            return res;
        }
        return mulDivF(x, y, zwl);
    }}

    /**
      * @dev Compute the smallest integer larger than or equal to `(x * y) / (z * w)`
    */
    function mulDivExC(uint256 x, uint256 y, uint256 z, uint256 w) internal pure returns (uint256) { unchecked {
        uint256 v = mulDivExF(x, y, z, w);
        (uint256 xyh, uint256 xyl) = mul512(x, y);
        (uint256 zwh, uint256 zwl) = mul512(z, w);
        (uint256 vzwlh, uint256 vzwll) = mul512(v, zwl);
        if (xyh == v * zwh + vzwlh && xyl == vzwll)
            return v;
        return safeAdd(v, 1);
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
      * @dev Compute the value of `2 ^ 256 * xh + xl - y`, where `2 ^ 256 * xh + xl >= y`
    */
    function sub512(uint256 xh, uint256 xl, uint256 y) private pure returns (uint256, uint256) { unchecked {
        if (xl >= y)
            return (xh, xl - y);
        return (xh - 1, unsafeSub(xl, y));
    }}

    /**
      * @dev Compute the value of `(2 ^ 256 * xh + xl) / pow2n`, where `xl` is divisible by `pow2n`
    */
    function div512(uint256 xh, uint256 xl, uint256 pow2n) private pure returns (uint256) { unchecked {
        uint256 pow2nInv = unsafeAdd(unsafeSub(0, pow2n) / pow2n, 1); // `1 << (256 - n)`
        return unsafeMul(xh, pow2nInv) | (xl / pow2n); // `(xh << (256 - n)) | (xl >> n)`
    }}

    /**
      * @dev Compute the inverse of `d` modulo `2 ^ 256`, where `d` is congruent to `1` modulo `2`
    */
    function inv256(uint256 d) private pure returns (uint256) { unchecked {
        // approximate the root of `f(x) = 1 / x - d` using the newton–raphson convergence method
        uint256 x = 1;
        for (uint256 i = 0; i < 8; ++i)
            x = unsafeMul(x, unsafeSub(2, unsafeMul(x, d))); // `x = x * (2 - x * d) mod 2 ^ 256`
        return x;
    }}

    /**
      * @dev Compute the value of `(2 ^ 256 * xh + xl) - (2 ^ 256 * yh + yl)`, where `2 ^ 256 * xh + xl >= 2 ^ 256 * yh + yl`
    */
    function sub512Ex(uint256 xh, uint256 xl, uint256 yh, uint256 yl) private pure returns (uint256, uint256) { unchecked {
        if (xl >= yl)
            return (xh - yh, xl - yl);
        return (xh - yh - 1, unsafeSub(xl, yl));
    }}
}
