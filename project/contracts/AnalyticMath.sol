// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity 0.8.27;

import "./IntegralMath.sol";

library AnalyticMath {
    // Auto-generated via 'PrintAnalyticMathConstants.py'
    uint256 internal constant FIXED_1 = 0x0080000000000000000000000000000000;
    uint256 internal constant LN2_MIN = 0x0058b90bfbe8e7bcd5e4f1d9cc01f97b57;
    uint256 internal constant LN2_MAX = 0x0058b90bfbe8e7bcd5e4f1d9cc01f97b58;
    uint256 internal constant LOG_MID = 0x015bf0a8b1457695355fb8ac404e7a79e4;
    uint256 internal constant EXP_MID = 0x0400000000000000000000000000000000;
    uint256 internal constant EXP_MAX = 0x2cb53f09f05cc627c85ddebfccfeb72758;

    /**
      * @dev Compute (a / b) ^ (c / d)
    */
    function pow(uint256 a, uint256 b, uint256 c, uint256 d) internal pure returns (uint256, uint256) { unchecked {
        if (b == 0 || d == 0)
            revert("division by zero");
        if (a == 0 || c == 0)
            return (a ** c, 1);
        if (a > b)
            return (fixedExp(IntegralMath.mulDivF(fixedLog(IntegralMath.mulDivF(FIXED_1, a, b)), c, d)), FIXED_1);
        if (b > a)
            return (FIXED_1, fixedExp(IntegralMath.mulDivF(fixedLog(IntegralMath.mulDivF(FIXED_1, b, a)), c, d)));
        return (1, 1);
    }}

    /**
      * @dev Compute log(a / b)
    */
    function log(uint256 a, uint256 b) internal pure returns (uint256, uint256) { unchecked {
        return (fixedLog(IntegralMath.mulDivF(FIXED_1, a, b)), FIXED_1);
    }}

    /**
      * @dev Compute exp(a / b)
    */
    function exp(uint256 a, uint256 b) internal pure returns (uint256, uint256) { unchecked {
        return (fixedExp(IntegralMath.mulDivF(FIXED_1, a, b)), FIXED_1);
    }}

    /**
      * @dev Compute log(x / FIXED_1) * FIXED_1
      * Input range: FIXED_1 <= x <= 2 ^ 256 - 1
      * Detailed description:
      * - For x < LOG_MID, compute log(x)
      * - For any other x, compute log(x / 2 ^ log2(x)) + log2(x) * log(2)
      * - The value of log(2) is represented as floor(log(2) * FIXED_1)
      * - With k = log2(x), this solution relies on the following identity:
      *   log(x) =
      *   log(x) + log(2 ^ k) - log(2 ^ k) =
      *   log(x) - log(2 ^ k) + log(2 ^ k) =
      *   log(x / log(2 ^ k)) + log(2 ^ k) =
      *   log(x / log(2 ^ k)) + k * log(2)
    */
    function fixedLog(uint256 x) internal pure returns (uint256) { unchecked {
        if (x < FIXED_1)
            revert("fixedLog: x < min");
        if (x < LOG_MID)
            return optimalLog(x);
        uint8 count = IntegralMath.floorLog2(x / FIXED_1);
        return optimalLog(x >> count) + count * LN2_MIN;
    }}

    /**
      * @dev Compute exp(x / FIXED_1) * FIXED_1
      * Input range: 0 <= x <= EXP_MAX - 1
      * Detailed description:
      * - For x < EXP_MID, compute exp(x)
      * - For any other x, compute exp(x % log(2)) * 2 ^ (x / log(2))
      * - The value of log(2) is represented as ceil(log(2) * FIXED_1)
      * - With k = x / log(2), this solution relies on the following identity:
      *   exp(x) =
      *   exp(x) * 2 ^ k / 2 ^ k =
      *   exp(x) * 2 ^ k / exp(k * log(2)) =
      *   exp(x) / exp(k * log(2)) * 2 ^ k =
      *   exp(x - k * log(2)) * 2 ^ k
    */
    function fixedExp(uint256 x) internal pure returns (uint256) { unchecked {
        if (x < EXP_MID)
            return optimalExp(x);
        if (x < EXP_MAX)
            return optimalExp(x % LN2_MAX) << (x / LN2_MAX);
        revert("fixedExp: x > max");
    }}

    /**
      * @dev Compute log(x / FIXED_1) * FIXED_1
      * Input range: FIXED_1 <= x <= FIXED_1 * 4 - 1
      * Auto-generated via 'PrintAnalyticMathOptimalLog.py'
      * Detailed description:
      * - Rewrite the input as a product of natural exponents and a single residual r, such that 1 < r < 2
      * - The natural logarithm of each (pre-calculated) exponent is the degree of the exponent
      * - The natural logarithm of r is calculated via Taylor series for log(1 + x), where x = r - 1
      * - The natural logarithm of the input is calculated by summing up the intermediate results above
      * - For example: log(250) = log(e^4 * e^1 * e^0.5 * 1.021692859) = 4 + 1 + 0.5 + log(1 + 0.021692859)
    */
    function optimalLog(uint256 x) internal pure returns (uint256) { unchecked {
        uint256 res = 0;

        uint256 y;
        uint256 z;
        uint256 w;

        if (x >= 0xd3094c70f034de4b96ff7d5b6f99fcd9) {res += 0x40000000000000000000000000000000; x = x * FIXED_1 / 0xd3094c70f034de4b96ff7d5b6f99fcd9;} // add 1 / 2^1
        if (x >= 0xa45af1e1f40c333b3de1db4dd55f29a8) {res += 0x20000000000000000000000000000000; x = x * FIXED_1 / 0xa45af1e1f40c333b3de1db4dd55f29a8;} // add 1 / 2^2
        if (x >= 0x910b022db7ae67ce76b441c27035c6a2) {res += 0x10000000000000000000000000000000; x = x * FIXED_1 / 0x910b022db7ae67ce76b441c27035c6a2;} // add 1 / 2^3
        if (x >= 0x88415abbe9a76bead8d00cf112e4d4a9) {res += 0x08000000000000000000000000000000; x = x * FIXED_1 / 0x88415abbe9a76bead8d00cf112e4d4a9;} // add 1 / 2^4
        if (x >= 0x84102b00893f64c705e841d5d4064bd4) {res += 0x04000000000000000000000000000000; x = x * FIXED_1 / 0x84102b00893f64c705e841d5d4064bd4;} // add 1 / 2^5
        if (x >= 0x8204055aaef1c8bd5c3259f4822735a3) {res += 0x02000000000000000000000000000000; x = x * FIXED_1 / 0x8204055aaef1c8bd5c3259f4822735a3;} // add 1 / 2^6
        if (x >= 0x810100ab00222d861931c15e39b44e9a) {res += 0x01000000000000000000000000000000; x = x * FIXED_1 / 0x810100ab00222d861931c15e39b44e9a;} // add 1 / 2^7
        if (x >= 0x808040155aabbbe9451521693554f734) {res += 0x00800000000000000000000000000000; x = x * FIXED_1 / 0x808040155aabbbe9451521693554f734;} // add 1 / 2^8

        z = y = x - FIXED_1;
        w = y * y / FIXED_1;
        res += z * (0x100000000000000000000000000000000 - y) / 0x100000000000000000000000000000000; z = z * w / FIXED_1; // add y^01 / 01 - y^02 / 02
        res += z * (0x0aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa - y) / 0x200000000000000000000000000000000; z = z * w / FIXED_1; // add y^03 / 03 - y^04 / 04
        res += z * (0x099999999999999999999999999999999 - y) / 0x300000000000000000000000000000000; z = z * w / FIXED_1; // add y^05 / 05 - y^06 / 06
        res += z * (0x092492492492492492492492492492492 - y) / 0x400000000000000000000000000000000; z = z * w / FIXED_1; // add y^07 / 07 - y^08 / 08
        res += z * (0x08e38e38e38e38e38e38e38e38e38e38e - y) / 0x500000000000000000000000000000000; z = z * w / FIXED_1; // add y^09 / 09 - y^10 / 10
        res += z * (0x08ba2e8ba2e8ba2e8ba2e8ba2e8ba2e8b - y) / 0x600000000000000000000000000000000; z = z * w / FIXED_1; // add y^11 / 11 - y^12 / 12
        res += z * (0x089d89d89d89d89d89d89d89d89d89d89 - y) / 0x700000000000000000000000000000000; z = z * w / FIXED_1; // add y^13 / 13 - y^14 / 14
        res += z * (0x088888888888888888888888888888888 - y) / 0x800000000000000000000000000000000;                      // add y^15 / 15 - y^16 / 16

        return res;
    }}

    /**
      * @dev Compute exp(x / FIXED_1) * FIXED_1
      * Input range: 0 <= x <= EXP_MID * 2 - 1
      * Auto-generated via 'PrintAnalyticMathOptimalExp.py'
      * Detailed description:
      * - Rewrite the input as a sum of binary exponents and a single residual r, as small as possible
      * - The exponentiation of each binary exponent is given (pre-calculated)
      * - The exponentiation of r is calculated via Taylor series for e^x, where x = r
      * - The exponentiation of the input is calculated by multiplying the intermediate results above
      * - For example: e^5.521692859 = e^(4 + 1 + 0.5 + 0.021692859) = e^4 * e^1 * e^0.5 * e^0.021692859
    */
    function optimalExp(uint256 x) internal pure returns (uint256) { unchecked {
        uint256 res = 0;

        uint256 y;
        uint256 z;

        z = y = x % 0x10000000000000000000000000000000; // get the input modulo 2^(-3)
        z = z * y / FIXED_1; res += z * 0x10e1b3be415a0000; // add y^02 * (20! / 02!)
        z = z * y / FIXED_1; res += z * 0x05a0913f6b1e0000; // add y^03 * (20! / 03!)
        z = z * y / FIXED_1; res += z * 0x0168244fdac78000; // add y^04 * (20! / 04!)
        z = z * y / FIXED_1; res += z * 0x004807432bc18000; // add y^05 * (20! / 05!)
        z = z * y / FIXED_1; res += z * 0x000c0135dca04000; // add y^06 * (20! / 06!)
        z = z * y / FIXED_1; res += z * 0x0001b707b1cdc000; // add y^07 * (20! / 07!)
        z = z * y / FIXED_1; res += z * 0x000036e0f639b800; // add y^08 * (20! / 08!)
        z = z * y / FIXED_1; res += z * 0x00000618fee9f800; // add y^09 * (20! / 09!)
        z = z * y / FIXED_1; res += z * 0x0000009c197dcc00; // add y^10 * (20! / 10!)
        z = z * y / FIXED_1; res += z * 0x0000000e30dce400; // add y^11 * (20! / 11!)
        z = z * y / FIXED_1; res += z * 0x000000012ebd1300; // add y^12 * (20! / 12!)
        z = z * y / FIXED_1; res += z * 0x0000000017499f00; // add y^13 * (20! / 13!)
        z = z * y / FIXED_1; res += z * 0x0000000001a9d480; // add y^14 * (20! / 14!)
        z = z * y / FIXED_1; res += z * 0x00000000001c6380; // add y^15 * (20! / 15!)
        z = z * y / FIXED_1; res += z * 0x000000000001c638; // add y^16 * (20! / 16!)
        z = z * y / FIXED_1; res += z * 0x0000000000001ab8; // add y^17 * (20! / 17!)
        z = z * y / FIXED_1; res += z * 0x000000000000017c; // add y^18 * (20! / 18!)
        z = z * y / FIXED_1; res += z * 0x0000000000000014; // add y^19 * (20! / 19!)
        z = z * y / FIXED_1; res += z * 0x0000000000000001; // add y^20 * (20! / 20!)
        res = res / 0x21c3677c82b40000 + y + FIXED_1; // divide by 20! and then add y^1 / 1! + y^0 / 0!

        if ((x & 0x010000000000000000000000000000000) != 0) res = res * 0x1c3d6a24ed82218787d624d3e5eba95f9 / 0x18ebef9eac820ae8682b9793ac6d1e776; // multiply by e^2^(-3)
        if ((x & 0x020000000000000000000000000000000) != 0) res = res * 0x18ebef9eac820ae8682b9793ac6d1e778 / 0x1368b2fc6f9609fe7aceb46aa619baed4; // multiply by e^2^(-2)
        if ((x & 0x040000000000000000000000000000000) != 0) res = res * 0x1368b2fc6f9609fe7aceb46aa619baed5 / 0x0bc5ab1b16779be3575bd8f0520a9f21f; // multiply by e^2^(-1)
        if ((x & 0x080000000000000000000000000000000) != 0) res = res * 0x0bc5ab1b16779be3575bd8f0520a9f21e / 0x0454aaa8efe072e7f6ddbab84b40a55c9; // multiply by e^2^(+0)
        if ((x & 0x100000000000000000000000000000000) != 0) res = res * 0x0454aaa8efe072e7f6ddbab84b40a55c5 / 0x00960aadc109e7a3bf4578099615711ea; // multiply by e^2^(+1)
        if ((x & 0x200000000000000000000000000000000) != 0) res = res * 0x00960aadc109e7a3bf4578099615711d7 / 0x0002bf84208204f5977f9a8cf01fdce3d; // multiply by e^2^(+2)
        if ((x & 0x400000000000000000000000000000000) != 0) res = res * 0x0002bf84208204f5977f9a8cf01fdc307 / 0x0000003c6ab775dd0b95b4cbee7e65d11; // multiply by e^2^(+3)

        return res;
    }}
}
