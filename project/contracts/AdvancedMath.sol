// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity 0.8.28;

import "./AnalyticMath.sol";
import "./FractionMath.sol";
import "./IntegralMath.sol";

library AdvancedMath {
    uint256 internal constant FIXED_1 = AnalyticMath.FIXED_1;

    // Auto-generated via 'PrintAdvancedMathConstants.py'
    uint256 internal constant LAMBERT_CONV_RADIUS = 0x02f16ac6c59de6f8d5d6f63c1482a7c86;
    uint256 internal constant LAMBERT_POS2_SAMPLE = 0x0183060c183060c183060c183060c1830;
    uint256 internal constant LAMBERT_POS2_MAXVAL = 0xc2f16ac6c59de6f8d5d6f63c1482a7c56;
    uint256 internal constant LAMBERT_POS2_T_SIZE = 0x000000000000000000000000000000010;
    uint256 internal constant LAMBERT_POS2_T_MASK = 0x0ffffffffffffffffffffffffffffffff;
    bytes   internal constant LAMBERT_POS2_VALUES = hex"60e393c68d20b1bd09deaabc0373b9c5"
                                                    hex"577b97aa1fe222bb452fdf111b1f0be2"
                                                    hex"5035f241d6eae0cd7bacba119993de7b"
                                                    hex"4a5cbc96a05589cb4d86be1db3168364"
                                                    hex"4585c8b3f8fe489c6e1833ca47871384"
                                                    hex"416e1b785d13eba07a08f3f18876a5ab"
                                                    hex"3de8f65ac388101ddf718a6f5c1eff65"
                                                    hex"3ad71c1c77e34fa32a9f184967eccbf6"
                                                    hex"3821f57dbd2763256c1a99bbd2051378"
                                                    hex"35b8b28d1a73dc27500ffe35559cc028"
                                                    hex"338e82ce00e2496262c64457535ba1a1"
                                                    hex"31996ec6b07b4a83421b5ebc4ab4e1f1"
                                                    hex"2fd19346ed17dac61219ce0c2c5ac4b0"
                                                    hex"2e309a221c12ba361e3ed695167feee2"
                                                    hex"2cb15ad3a1eb65f6d74a75da09a1b6c5"
                                                    hex"2b4f95cd46904d05d72bdcde337d9cc7"
                                                    hex"2a07c206cde2c9467e42ebdfc395e285"
                                                    hex"28d6e752efcbae881bb2163e088236de"
                                                    hex"27ba81d008f57136440e87f44fb95f59"
                                                    hex"26b06bf4b3ca8a8e6b5f1207cf63e484"
                                                    hex"25b6cd7b40b306b014cc93eb0fd34b1b"
                                                    hex"24cc0df118d221d961d0e3c7c2cc74d8"
                                                    hex"23eeca079ec9f001c7488cb0210969d3"
                                                    hex"231dcb016e2797ddce1ba75a69081655"
                                                    hex"2257ffc1f84048f54f9072007f255977"
                                                    hex"219c772441c4b78d49d6bf72dea3ab56"
                                                    hex"20ea5b53c3a2de83f69655808913322d"
                                                    hex"2040edf2ba98675afaf33ad7b36a7956"
                                                    hex"1f9f84e53efd744e8c01d02e4f1071c8"
                                                    hex"1f0587a1831d516e4979ad85cd0b3e5a"
                                                    hex"1e726cec66b24906997bda3801535ebd"
                                                    hex"1de5b8eebff06b21b543b19c5fa002d9"
                                                    hex"1d5efb93b9235c7a64079fab2ad709ba"
                                                    hex"1cddcf23ba8eb156b9b26750904cf312"
                                                    hex"1c61d711c357ed86ebefbfee82d3264a"
                                                    hex"1beabef2fb396b13011f8ea801422ad9"
                                                    hex"1b783999c85b7cd9ce638b020080d100"
                                                    hex"1b0a004ee7fd8c81ac47b6c04894bb04"
                                                    hex"1a9fd223fef4735d6e1130db2341072b"
                                                    hex"1a39735bdda3a6d7e2b3d1dd5d800661"
                                                    hex"19d6ace55419021d7827019f435c30c5"
                                                    hex"19774be5f6227a7ba0b2e9c5d78c13c8"
                                                    hex"191b21529a9dc854272046bfe7592441"
                                                    hex"18c20193b99c0f235d36b322031296a9"
                                                    hex"186bc43415f31f813caf1fb4300e23c9"
                                                    hex"181843985b6794d75c8c626a51041977"
                                                    hex"17c75cbe8d10c6063ecfe590c8a0fd84"
                                                    hex"1778ef0449cafac4a5cf259d93863693"
                                                    hex"172cdbf30ff93902a95a8146b585c655"
                                                    hex"16e30711c7afebcb40109634b86d8799"
                                                    hex"169b55baf39bccd230485248f4995e18"
                                                    hex"1655aef6fe5d98ce041a10e7ca963ad3"
                                                    hex"1611fb5a2c46df8f23786225867f6d08"
                                                    hex"15d024e5c8ecb766b45e74cdc8172794"
                                                    hex"159016ec3550613e36a46d481b57d4a2"
                                                    hex"1551bdf786c6d4b006e447ee93fe60bf"
                                                    hex"151507b27099e70da8f1197ca7a94b1e"
                                                    hex"14d9e2d33ad6bc2f8f1e6a949032aae3"
                                                    hex"14a03f0890117064244d99699b33162a"
                                                    hex"14680ce7f240e96bd25479e66a1a1872"
                                                    hex"14313dddac5beb6ae0dc9ab15e6325a4"
                                                    hex"13fbc41e1b3092ef02d998374545ec41"
                                                    hex"13c792982c23053712ec80994a00d48b"
                                                    hex"13949ce8f42d5c83b87967913b857db2"
                                                    hex"1362d75044b414864af094d1c98c5045"
                                                    hex"133236a6269740b8ed72a7216b473521"
                                                    hex"1302b05126670d0c809cfdf596bf59aa"
                                                    hex"12d43a3d5ed4e587f9bf9f3546a14cc9"
                                                    hex"12a6cad4306bf1e228555efcf9e981b3"
                                                    hex"127a58f49753c126c34fccd0fb33a40a"
                                                    hex"124edbec11664bc999baaffb949ae84c"
                                                    hex"12244b70083d14d53392cc3d4aec745c"
                                                    hex"11fa9f97b40d9011194c94a270e6c582"
                                                    hex"11d1d0d66d3fb456945cf53f8cddd542"
                                                    hex"11a9d7f6639ed17b5ab53f819bad9299"
                                                    hex"1182ae13b2dfe31bd4041aed11d1bc02"
                                                    hex"115c4c97ccfcbb784459d0fc547c65dc"
                                                    hex"1136ad3533932db11c651bec0f863f9f"
                                                    hex"1111c9e37a1528d2e3a11bbe1671030d"
                                                    hex"10ed9cdb8b2486b23f5197f432dfedde"
                                                    hex"10ca20942bf4f38da855bc16829f7176"
                                                    hex"10a74fbeb90156f2ef7da0e6ff154ef2"
                                                    hex"1085254417c9ec4689192684fd24d9fb"
                                                    hex"10639c41d9adf82e9a962729d9c5354b"
                                                    hex"1042b0078c48d2121c45356ef952a884"
                                                    hex"10225c143406bfe3646184b22ff0b242"
                                                    hex"10029c13edebbcadcd02f4bf6077e934"
                                                    hex"0fe36bddb5c56d8889ed2aa2164563dd"
                                                    hex"0fc4c7714e3aeceb64a83c0fbd5b3409"
                                                    hex"0fa6aaf54861476764473f34e82d3a9c"
                                                    hex"0f8912b528ab0b6a790407fa5f9bf8b1"
                                                    hex"0f6bfb1fa7349e64712ab860554d7b78"
                                                    hex"0f4f60c509968df5add12deae5027309"
                                                    hex"0f334055948b2a0dc667a844c6723b23"
                                                    hex"0f1796a013d5b15214dc09abf2a0592b"
                                                    hex"0efc609076f78738f15c360223f8c79d"
                                                    hex"0ee19b2e815b8e957ce06c5e16449ca8"
                                                    hex"0ec7439c8cb9187b324eb1d2758ee4d3"
                                                    hex"0ead57165c8714db919b9ccd15e45159"
                                                    hex"0e93d2f0016d88ff1e5182897a357740"
                                                    hex"0e7ab494cbb6ec0c4cbc602eb4bb78e3"
                                                    hex"0e61f9864bd512e429ac81729beeec69"
                                                    hex"0e499f5b601dee819305eb00790b9c9a"
                                                    hex"0e31a3bf4ef3ab0dadc11b18d962c820"
                                                    hex"0e1a0470ec99d736c6436de2abaf3b64"
                                                    hex"0e02bf41cc063d700f4cb7817df3dfd7"
                                                    hex"0debd2157a081b83117c46ea1dc579d1"
                                                    hex"0dd53ae0c22b7df344fa51532b60dd98"
                                                    hex"0dbef7a8fcc8c7c9c5332ac339c9f88d"
                                                    hex"0da9068365b9ee4b304fb9666adccf46"
                                                    hex"0d9365947b37bb14237ee7d1802ffa2f"
                                                    hex"0d7e130f64698ce1098c56ddad89fb56"
                                                    hex"0d690d355f399d48cad4f9225f1a3f9d"
                                                    hex"0d5452553506d42a1f2f7d5cf97679d9"
                                                    hex"0d3fe0cab5d3b39f329597f217bf7928"
                                                    hex"0d2bb6fe3997f32783f2b5d8a3acd0c9"
                                                    hex"0d17d364275fffa6cb83e0553ca42663"
                                                    hex"0d04347c81ead056e793c81ed9aa583e"
                                                    hex"0cf0d8d2797b5e9e40afe04977971655"
                                                    hex"0cddbefc029796ff51a1c94f6c2e5589"
                                                    hex"0ccae5997172d28b9d7969676b6cfb06"
                                                    hex"0cb84b5519c5d86400e5ebbcb895c475"
                                                    hex"0ca5eee2f2da13533492e3978c84b997"
                                                    hex"0c93cf003f91157bbee2579fcf0a33f3"
                                                    hex"0c81ea733a34b805f2bf6edd83fca2cd"
                                                    hex"0c70400ac3df22f2e73d2a54bee3b3ee"
                                                    hex"0c5ece9e174cd59d6c32f900259dd921"
                                                    hex"0c4d950c7eed66993aa3f25a85ea9e43";

    /**
      * @dev Solve x * (a / b) ^ x = c / d
      * Solution: x = W(log(a / b) * c / d) / (log(a / b) * c / d) * c / d
    */
    function solve(uint256 a, uint256 b, uint256 c, uint256 d) internal pure returns (uint256, uint256) { unchecked {
        if (a > b)
            return call(lambertPos, a, b, c, d);
        if (b > a)
            return call(lambertNeg, b, a, c, d);
        return (c, d);
    }}

    /**
      * @dev Compute W(-x / FIXED_1) / (-x / FIXED_1) * FIXED_1
      * Input range: 1 <= x <= LAMBERT_CONV_RADIUS
    */
    function lambertNeg(uint256 x) internal pure returns (uint256) { unchecked {
        require(x > 0, "lambertNeg: x < min");
        if (x <= LAMBERT_CONV_RADIUS)
            return lambertNeg1(x);
        revert("lambertNeg: x > max");
    }}

    /**
      * @dev Compute W(x / FIXED_1) / (x / FIXED_1) * FIXED_1
      * Input range: 1 <= x <= 2 ^ 256 - 1
    */
    function lambertPos(uint256 x) internal pure returns (uint256) { unchecked {
        require(x > 0, "lambertPos: x < min");
        if (x <= LAMBERT_CONV_RADIUS)
            return lambertPos1(x);
        if (x <= LAMBERT_POS2_MAXVAL)
            return lambertPos2(x);
        return lambertPos3(x);
    }}

    /**
      * @dev Compute W(-x / FIXED_1) / (-x / FIXED_1) * FIXED_1
      * Input range: 1 <= x <= LAMBERT_CONV_RADIUS
      * Auto-generated via 'PrintAdvancedMathLambertNeg1.py'
    */
    function lambertNeg1(uint256 x) internal pure returns (uint256) { unchecked {
        uint256 res = 0;
        uint256 xi = x;

        xi = (xi * x) / FIXED_1; res += xi * 0x00000000014d29a73a6e7b02c3668c7b0880000000; // add x^(03-1) * (34! * 03^(03-1) / 03!)
        xi = (xi * x) / FIXED_1; res += xi * 0x0000000002504a0cd9a7f7215b60f9be4800000000; // add x^(04-1) * (34! * 04^(04-1) / 04!)
        xi = (xi * x) / FIXED_1; res += xi * 0x000000000484d0a1191c0ead267967c7a4a0000000; // add x^(05-1) * (34! * 05^(05-1) / 05!)
        xi = (xi * x) / FIXED_1; res += xi * 0x00000000095ec580d7e8427a4baf26a90a00000000; // add x^(06-1) * (34! * 06^(06-1) / 06!)
        xi = (xi * x) / FIXED_1; res += xi * 0x000000001440b0be1615a47dba6e5b3b1f10000000; // add x^(07-1) * (34! * 07^(07-1) / 07!)
        xi = (xi * x) / FIXED_1; res += xi * 0x000000002d207601f46a99b4112418400000000000; // add x^(08-1) * (34! * 08^(08-1) / 08!)
        xi = (xi * x) / FIXED_1; res += xi * 0x0000000066ebaac4c37c622dd8288a7eb1b2000000; // add x^(09-1) * (34! * 09^(09-1) / 09!)
        xi = (xi * x) / FIXED_1; res += xi * 0x00000000ef17240135f7dbd43a1ba10cf200000000; // add x^(10-1) * (34! * 10^(10-1) / 10!)
        xi = (xi * x) / FIXED_1; res += xi * 0x0000000233c33c676a5eb2416094a87b3657000000; // add x^(11-1) * (34! * 11^(11-1) / 11!)
        xi = (xi * x) / FIXED_1; res += xi * 0x0000000541cde48bc0254bed49a9f8700000000000; // add x^(12-1) * (34! * 12^(12-1) / 12!)
        xi = (xi * x) / FIXED_1; res += xi * 0x0000000cae1fad2cdd4d4cb8d73abca0d19a400000; // add x^(13-1) * (34! * 13^(13-1) / 13!)
        xi = (xi * x) / FIXED_1; res += xi * 0x0000001edb2aa2f760d15c41ceedba956400000000; // add x^(14-1) * (34! * 14^(14-1) / 14!)
        xi = (xi * x) / FIXED_1; res += xi * 0x0000004ba8d20d2dabd386c9529659841a2e200000; // add x^(15-1) * (34! * 15^(15-1) / 15!)
        xi = (xi * x) / FIXED_1; res += xi * 0x000000bac08546b867cdaa20000000000000000000; // add x^(16-1) * (34! * 16^(16-1) / 16!)
        xi = (xi * x) / FIXED_1; res += xi * 0x000001cfa8e70c03625b9db76c8ebf5bbf24820000; // add x^(17-1) * (34! * 17^(17-1) / 17!)
        xi = (xi * x) / FIXED_1; res += xi * 0x000004851d99f82060df265f3309b26f8200000000; // add x^(18-1) * (34! * 18^(18-1) / 18!)
        xi = (xi * x) / FIXED_1; res += xi * 0x00000b550d19b129d270c44f6f55f027723cbb0000; // add x^(19-1) * (34! * 19^(19-1) / 19!)
        xi = (xi * x) / FIXED_1; res += xi * 0x00001c877dadc761dc272deb65d4b0000000000000; // add x^(20-1) * (34! * 20^(20-1) / 20!)
        xi = (xi * x) / FIXED_1; res += xi * 0x000048178ece97479f33a77f2ad22a81b64406c000; // add x^(21-1) * (34! * 21^(21-1) / 21!)
        xi = (xi * x) / FIXED_1; res += xi * 0x0000b6ca8268b9d810fedf6695ef2f8a6c00000000; // add x^(22-1) * (34! * 22^(22-1) / 22!)
        xi = (xi * x) / FIXED_1; res += xi * 0x0001d0e76631a5b05d007b8cb72a7c7f11ec36e000; // add x^(23-1) * (34! * 23^(23-1) / 23!)
        xi = (xi * x) / FIXED_1; res += xi * 0x0004a1c37bd9f85fd9c6c780000000000000000000; // add x^(24-1) * (34! * 24^(24-1) / 24!)
        xi = (xi * x) / FIXED_1; res += xi * 0x000bd8369f1b702bf491e2ebfcee08250313b65400; // add x^(25-1) * (34! * 25^(25-1) / 25!)
        xi = (xi * x) / FIXED_1; res += xi * 0x001e5c7c32a9f6c70ab2cb59d9225764d400000000; // add x^(26-1) * (34! * 26^(26-1) / 26!)
        xi = (xi * x) / FIXED_1; res += xi * 0x004dff5820e165e910f95120a708e742496221e600; // add x^(27-1) * (34! * 27^(27-1) / 27!)
        xi = (xi * x) / FIXED_1; res += xi * 0x00c8c8f66db1fced378ee50e536000000000000000; // add x^(28-1) * (34! * 28^(28-1) / 28!)
        xi = (xi * x) / FIXED_1; res += xi * 0x0205db8dffff45bfa2938f128f599dbf16eb11d880; // add x^(29-1) * (34! * 29^(29-1) / 29!)
        xi = (xi * x) / FIXED_1; res += xi * 0x053a044ebd984351493e1786af38d39a0800000000; // add x^(30-1) * (34! * 30^(30-1) / 30!)
        xi = (xi * x) / FIXED_1; res += xi * 0x0d86dae2a4cc0f47633a544479735869b487b59c40; // add x^(31-1) * (34! * 31^(31-1) / 31!)
        xi = (xi * x) / FIXED_1; res += xi * 0x231000000000000000000000000000000000000000; // add x^(32-1) * (34! * 32^(32-1) / 32!)
        xi = (xi * x) / FIXED_1; res += xi * 0x5b0485a76f6646c2039db1507cdd51b08649680822; // add x^(33-1) * (34! * 33^(33-1) / 33!)
        xi = (xi * x) / FIXED_1; res += xi * 0xec983c46c49545bc17efa6b5b0055e242200000000; // add x^(34-1) * (34! * 34^(34-1) / 34!)

        return res / 0xde1bc4d19efcac82445da75b00000000 + FIXED_1 + x; // divide by 34! and then add x^(1-1) * (1^(1-1) / 1!) + x^(2-1) * (2^(2-1) / 2!)
    }}

    /**
      * @dev Compute W(x / FIXED_1) / (x / FIXED_1) * FIXED_1
      * Input range: 1 <= x <= LAMBERT_CONV_RADIUS
      * Auto-generated via 'PrintAdvancedMathLambertPos1.py'
    */
    function lambertPos1(uint256 x) internal pure returns (uint256) { unchecked {
        uint256 res = 0;
        uint256 xi = x;

        xi = (xi * x) / FIXED_1; res += xi * 0x00000000014d29a73a6e7b02c3668c7b0880000000; // add x^(03-1) * (34! * 03^(03-1) / 03!)
        xi = (xi * x) / FIXED_1; res -= xi * 0x0000000002504a0cd9a7f7215b60f9be4800000000; // sub x^(04-1) * (34! * 04^(04-1) / 04!)
        xi = (xi * x) / FIXED_1; res += xi * 0x000000000484d0a1191c0ead267967c7a4a0000000; // add x^(05-1) * (34! * 05^(05-1) / 05!)
        xi = (xi * x) / FIXED_1; res -= xi * 0x00000000095ec580d7e8427a4baf26a90a00000000; // sub x^(06-1) * (34! * 06^(06-1) / 06!)
        xi = (xi * x) / FIXED_1; res += xi * 0x000000001440b0be1615a47dba6e5b3b1f10000000; // add x^(07-1) * (34! * 07^(07-1) / 07!)
        xi = (xi * x) / FIXED_1; res -= xi * 0x000000002d207601f46a99b4112418400000000000; // sub x^(08-1) * (34! * 08^(08-1) / 08!)
        xi = (xi * x) / FIXED_1; res += xi * 0x0000000066ebaac4c37c622dd8288a7eb1b2000000; // add x^(09-1) * (34! * 09^(09-1) / 09!)
        xi = (xi * x) / FIXED_1; res -= xi * 0x00000000ef17240135f7dbd43a1ba10cf200000000; // sub x^(10-1) * (34! * 10^(10-1) / 10!)
        xi = (xi * x) / FIXED_1; res += xi * 0x0000000233c33c676a5eb2416094a87b3657000000; // add x^(11-1) * (34! * 11^(11-1) / 11!)
        xi = (xi * x) / FIXED_1; res -= xi * 0x0000000541cde48bc0254bed49a9f8700000000000; // sub x^(12-1) * (34! * 12^(12-1) / 12!)
        xi = (xi * x) / FIXED_1; res += xi * 0x0000000cae1fad2cdd4d4cb8d73abca0d19a400000; // add x^(13-1) * (34! * 13^(13-1) / 13!)
        xi = (xi * x) / FIXED_1; res -= xi * 0x0000001edb2aa2f760d15c41ceedba956400000000; // sub x^(14-1) * (34! * 14^(14-1) / 14!)
        xi = (xi * x) / FIXED_1; res += xi * 0x0000004ba8d20d2dabd386c9529659841a2e200000; // add x^(15-1) * (34! * 15^(15-1) / 15!)
        xi = (xi * x) / FIXED_1; res -= xi * 0x000000bac08546b867cdaa20000000000000000000; // sub x^(16-1) * (34! * 16^(16-1) / 16!)
        xi = (xi * x) / FIXED_1; res += xi * 0x000001cfa8e70c03625b9db76c8ebf5bbf24820000; // add x^(17-1) * (34! * 17^(17-1) / 17!)
        xi = (xi * x) / FIXED_1; res -= xi * 0x000004851d99f82060df265f3309b26f8200000000; // sub x^(18-1) * (34! * 18^(18-1) / 18!)
        xi = (xi * x) / FIXED_1; res += xi * 0x00000b550d19b129d270c44f6f55f027723cbb0000; // add x^(19-1) * (34! * 19^(19-1) / 19!)
        xi = (xi * x) / FIXED_1; res -= xi * 0x00001c877dadc761dc272deb65d4b0000000000000; // sub x^(20-1) * (34! * 20^(20-1) / 20!)
        xi = (xi * x) / FIXED_1; res += xi * 0x000048178ece97479f33a77f2ad22a81b64406c000; // add x^(21-1) * (34! * 21^(21-1) / 21!)
        xi = (xi * x) / FIXED_1; res -= xi * 0x0000b6ca8268b9d810fedf6695ef2f8a6c00000000; // sub x^(22-1) * (34! * 22^(22-1) / 22!)
        xi = (xi * x) / FIXED_1; res += xi * 0x0001d0e76631a5b05d007b8cb72a7c7f11ec36e000; // add x^(23-1) * (34! * 23^(23-1) / 23!)
        xi = (xi * x) / FIXED_1; res -= xi * 0x0004a1c37bd9f85fd9c6c780000000000000000000; // sub x^(24-1) * (34! * 24^(24-1) / 24!)
        xi = (xi * x) / FIXED_1; res += xi * 0x000bd8369f1b702bf491e2ebfcee08250313b65400; // add x^(25-1) * (34! * 25^(25-1) / 25!)
        xi = (xi * x) / FIXED_1; res -= xi * 0x001e5c7c32a9f6c70ab2cb59d9225764d400000000; // sub x^(26-1) * (34! * 26^(26-1) / 26!)
        xi = (xi * x) / FIXED_1; res += xi * 0x004dff5820e165e910f95120a708e742496221e600; // add x^(27-1) * (34! * 27^(27-1) / 27!)
        xi = (xi * x) / FIXED_1; res -= xi * 0x00c8c8f66db1fced378ee50e536000000000000000; // sub x^(28-1) * (34! * 28^(28-1) / 28!)
        xi = (xi * x) / FIXED_1; res += xi * 0x0205db8dffff45bfa2938f128f599dbf16eb11d880; // add x^(29-1) * (34! * 29^(29-1) / 29!)
        xi = (xi * x) / FIXED_1; res -= xi * 0x053a044ebd984351493e1786af38d39a0800000000; // sub x^(30-1) * (34! * 30^(30-1) / 30!)
        xi = (xi * x) / FIXED_1; res += xi * 0x0d86dae2a4cc0f47633a544479735869b487b59c40; // add x^(31-1) * (34! * 31^(31-1) / 31!)
        xi = (xi * x) / FIXED_1; res -= xi * 0x231000000000000000000000000000000000000000; // sub x^(32-1) * (34! * 32^(32-1) / 32!)
        xi = (xi * x) / FIXED_1; res += xi * 0x5b0485a76f6646c2039db1507cdd51b08649680822; // add x^(33-1) * (34! * 33^(33-1) / 33!)
        xi = (xi * x) / FIXED_1; res -= xi * 0xec983c46c49545bc17efa6b5b0055e242200000000; // sub x^(34-1) * (34! * 34^(34-1) / 34!)

        return res / 0xde1bc4d19efcac82445da75b00000000 + FIXED_1 - x; // divide by 34! and then add x^(1-1) * (1^(1-1) / 1!) - x^(2-1) * (2^(2-1) / 2!)
    }}

    /**
      * @dev Compute W(x / FIXED_1) / (x / FIXED_1) * FIXED_1
      * Input range: LAMBERT_CONV_RADIUS + 1 <= x <= LAMBERT_POS2_MAXVAL
    */
    function lambertPos2(uint256 x) internal pure returns (uint256) { unchecked {
        bytes memory values = LAMBERT_POS2_VALUES;
        uint256 y = x - LAMBERT_CONV_RADIUS - 1;
        uint256 i = y / LAMBERT_POS2_SAMPLE;
        uint256 a = LAMBERT_POS2_SAMPLE * (i + 0);
        uint256 b = LAMBERT_POS2_SAMPLE * (i + 1);
        uint256 c = LAMBERT_POS2_T_SIZE * (i + 1);
        uint256 d = LAMBERT_POS2_T_SIZE * (i + 2);
        uint256 e = read(values, c) & LAMBERT_POS2_T_MASK;
        uint256 f = read(values, d) & LAMBERT_POS2_T_MASK;
        uint256 g = e * (b - y);
        uint256 h = f * (y - a);
        return (g + h) / LAMBERT_POS2_SAMPLE;
    }}

    /**
      * @dev Compute W(x / FIXED_1) / (x / FIXED_1) * FIXED_1
      * Input range: LAMBERT_POS2_MAXVAL + 1 <= x <= 2 ^ 256 - 1
    */
    function lambertPos3(uint256 x) internal pure returns (uint256) { unchecked {
        uint256 a = AnalyticMath.fixedLog(x);
        uint256 b = AnalyticMath.fixedLog(a);
        uint256 c = IntegralMath.mulDivF(b, b + (a - FIXED_1) * 2, a);
        uint256 d = IntegralMath.mulDivF(FIXED_1 / 2, c, a);
        uint256 e = IntegralMath.mulDivF(FIXED_1, a - b + d, x);
        return e;
    }}

    // auxiliary function
    function read(bytes memory data, uint256 offset) private pure returns (uint256 result) {
        assembly {result := mload(add(data, offset))}
    }

    // auxiliary function
    function call(function (uint256) pure returns (uint256) f, uint256 x, uint256 y, uint256 z, uint256 w) private pure returns (uint256, uint256) {
        return FractionMath.productRatio(f(IntegralMath.mulDivF(AnalyticMath.fixedLog(IntegralMath.mulDivF(FIXED_1, x, y)), z, w)), z, w, FIXED_1);
    }
}
