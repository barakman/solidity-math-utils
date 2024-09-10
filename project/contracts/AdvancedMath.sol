// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity 0.8.27;

import "./AnalyticMath.sol";
import "./FractionMath.sol";
import "./IntegralMath.sol";

library AdvancedMath {
    uint256 internal constant FIXED_1 = AnalyticMath.FIXED_1;

    // Auto-generated via 'PrintAdvancedMathConstants.py'
    uint256 internal constant LAMBERT_CONV_RADIUS = 0x02f16ac6c59de6f8d5d6f63c1482a7c86;
    uint256 internal constant LAMBERT_POS2_SAMPLE = 0x003060c183060c183060c183060c18306;
    uint256 internal constant LAMBERT_POS2_MAXVAL = 0x1af16ac6c59de6f8d5d6f63c1482a7c80;
    uint256 internal constant LAMBERT_POS2_T_SIZE = 0x000000000000000000000000000000010;
    uint256 internal constant LAMBERT_POS2_T_MASK = 0x0ffffffffffffffffffffffffffffffff;
    bytes   internal constant LAMBERT_POS2_VALUES = hex"60e393c68d20b1bd09deaabc0373b9c5"
                                                    hex"5f8f46e4854120989ed94719fb4c2011"
                                                    hex"5e479ebb9129fb1b7e72a648f992b606"
                                                    hex"5d0bd23fe42dfedde2e9586be12b85fe"
                                                    hex"5bdb29ddee979308ddfca81aeeb8095a"
                                                    hex"5ab4fd8a260d2c7e2c0d2afcf0009dad"
                                                    hex"5998b31359a55d48724c65cf09001221"
                                                    hex"5885bcad2b322dfc43e8860f9c018cf5"
                                                    hex"577b97aa1fe222bb452fdf111b1f0be2"
                                                    hex"5679cb5e3575632e5baa27e2b949f704"
                                                    hex"557fe8241b3a31c83c732f1cdff4a1c5"
                                                    hex"548d868026504875d6e59bbe95fc2a6b"
                                                    hex"53a2465ce347cf34d05a867c17dd3088"
                                                    hex"52bdce5dcd4faed59c7f5511cf8f8acc"
                                                    hex"51dfcb453c07f8da817606e7885f7c3e"
                                                    hex"5107ef6b0a5a2be8f8ff15590daa3cce"
                                                    hex"5035f241d6eae0cd7bacba119993de7b"
                                                    hex"4f698fe90d5b53d532171e1210164c66"
                                                    hex"4ea288ca297a0e6a09a0eee240e16c85"
                                                    hex"4de0a13fdcf5d4213fc398ba6e3becde"
                                                    hex"4d23a145eef91fec06b06140804c4808"
                                                    hex"4c6b5430d4c1ee5526473db4ae0f11de"
                                                    hex"4bb7886c240562eba11f4963a53b4240"
                                                    hex"4b080f3f1cb491d2d521e0ea4583521e"
                                                    hex"4a5cbc96a05589cb4d86be1db3168364"
                                                    hex"49b566d40243517658d78c33162d6ece"
                                                    hex"4911e6a02e5507a30f947383fd9a3276"
                                                    hex"487216c2b31be4adc41db8a8d5cc0c88"
                                                    hex"47d5d3fc4a7a1b188cd3d788b5c5e9fc"
                                                    hex"473cfce4871a2c40bc4f9e1c32b955d0"
                                                    hex"46a771ca578ab878485810e285e31c67"
                                                    hex"4615149718aed4c258c373dc676aa72d"
                                                    hex"4585c8b3f8fe489c6e1833ca47871384"
                                                    hex"44f972f174e41e5efb7e9d63c29ce735"
                                                    hex"446ff970ba86d8b00beb05ecebf3c4dc"
                                                    hex"43e9438ec88971812d6f198b5ccaad96"
                                                    hex"436539d11ff7bea657aeddb394e809ef"
                                                    hex"42e3c5d3e5a913401d86f66db5d81c2c"
                                                    hex"4264d2395303070ea726cbe98df62174"
                                                    hex"41e84a9a593bb7194c3a6349ecae4eea"
                                                    hex"416e1b785d13eba07a08f3f18876a5ab"
                                                    hex"40f6322ff389d423ba9dd7e7e7b7e809"
                                                    hex"40807cec8a466880ecf4184545d240a4"
                                                    hex"400cea9ce88a8d3ae668e8ea0d9bf07f"
                                                    hex"3f9b6ae8772d4c55091e0ed7dfea0ac1"
                                                    hex"3f2bee253fd84594f54bcaafac383a13"
                                                    hex"3ebe654e95208bb9210c575c081c5958"
                                                    hex"3e52c1fc5665635b78ce1f05ad53c086"
                                                    hex"3de8f65ac388101ddf718a6f5c1eff65"
                                                    hex"3d80f522d59bd0b328ca012df4cd2d49"
                                                    hex"3d1ab193129ea72b23648a161163a85a"
                                                    hex"3cb61f68d32576c135b95cfb53f76d75"
                                                    hex"3c5332d9f1aae851a3619e77e4cc8473"
                                                    hex"3bf1e08edbe2aa109e1525f65759ef73"
                                                    hex"3b921d9cff13fa2c197746a3dfc4918f"
                                                    hex"3b33df818910bfc1a5aefb8f63ae2ac4"
                                                    hex"3ad71c1c77e34fa32a9f184967eccbf6"
                                                    hex"3a7bc9abf2c5bb53e2f7384a8a16521a"
                                                    hex"3a21dec7e76369783a68a0c6385a1c57"
                                                    hex"39c9525de6c9cdf7c1c157ca4a7a6ee3"
                                                    hex"39721bad3dc85d1240ff0190e0adaac3"
                                                    hex"391c324344d3248f0469eb28dd3d77e0"
                                                    hex"38c78df7e3c796279fb4ff84394ab3da"
                                                    hex"387426ea4638ae9aae08049d3554c20a"
                                                    hex"3821f57dbd2763256c1a99bbd2051378"
                                                    hex"37d0f256cb46a8c92ff62fbbef289698"
                                                    hex"37811658591ffc7abdd1feaf3cef9b73"
                                                    hex"37325aa10e9e82f7df0f380f7997154b"
                                                    hex"36e4b888cfb408d873b9a80d439311c6"
                                                    hex"3698299e59f4bb9de645fc9b08c64cca"
                                                    hex"364ca7a5012cb603023b57dd3ebfd50d"
                                                    hex"36022c928915b778ab1b06aaee7e61d4"
                                                    hex"35b8b28d1a73dc27500ffe35559cc028"
                                                    hex"357033e951fe250ec5eb4e60955132d7"
                                                    hex"3528ab2867934e3a21b5412e4c4f8881"
                                                    hex"34e212f66c55057f9676c80094a61d59"
                                                    hex"349c66289e5b3c4b540c24f42fa4b9bb"
                                                    hex"34579fbbd0c733a9c8d6af6b0f7d00f7"
                                                    hex"3413bad2e712288b924b5882b5b369bf"
                                                    hex"33d0b2b56286510ef730e213f71f12e9"
                                                    hex"338e82ce00e2496262c64457535ba1a1"
                                                    hex"334d26a96b373bb7c2f8ea1827f27a92"
                                                    hex"330c99f4f4211469e00b3e18c31475ea"
                                                    hex"32ccd87d6486094999c7d5e6f33237d8"
                                                    hex"328dde2dd617b6665a2e8556f250c1af"
                                                    hex"324fa70e9adc270f8262755af5a99af9"
                                                    hex"32122f443110611ca51040f41fa6e1e3"
                                                    hex"31d5730e42c0831482f0f1485c4263d8"
                                                    hex"31996ec6b07b4a83421b5ebc4ab4e1f1"
                                                    hex"315e1ee0a68ff46bb43ec2b85032e876"
                                                    hex"31237fe7bc4deacf6775b9efa1a145f8"
                                                    hex"30e98e7f1cc5a356e44627a6972ea2ff"
                                                    hex"30b04760b8917ec74205a3002650ec05"
                                                    hex"3077a75c803468e9132ce0cf3224241d"
                                                    hex"303fab57a6a275c36f19cda9bace667a"
                                                    hex"3008504beb8dcbd2cf3bc1f6d5a064f0"
                                                    hex"2fd19346ed17dac61219ce0c2c5ac4b0"
                                                    hex"2f9b7169808c324b5852fd3d54ba9714"
                                                    hex"2f65e7e711cf4b064eea9c08cbdad574"
                                                    hex"2f30f405093042ddff8a251b6bf6d103"
                                                    hex"2efc931a3750f2e8bfe323edfe037574"
                                                    hex"2ec8c28e46dbe56d98685278339400cb"
                                                    hex"2e957fd933c3926d8a599b602379b851"
                                                    hex"2e62c882c7c9ed4473412702f08ba0e5"
                                                    hex"2e309a221c12ba361e3ed695167feee2"
                                                    hex"2dfef25d1f865ae18dd07cfea4bcea10"
                                                    hex"2dcdcee821cdc80decc02c44344aeb31"
                                                    hex"2d9d2d8562b34944d0b201bb87260c83"
                                                    hex"2d6d0c04a5b62a2c42636308669b729a"
                                                    hex"2d3d6842c9a235517fc5a0332691528f"
                                                    hex"2d0e402963fe1ea2834abc408c437c10"
                                                    hex"2cdf91ae602647908aff975e4d6a2a8c"
                                                    hex"2cb15ad3a1eb65f6d74a75da09a1b6c5"
                                                    hex"2c8399a6ab8e9774d6fcff373d210727"
                                                    hex"2c564c4046f64edba6883ca06bbc4535"
                                                    hex"2c2970c431f952641e05cb493e23eed3"
                                                    hex"2bfd0560cd9eb14563bc7c0732856c18"
                                                    hex"2bd1084ed0332f7ff4150f9d0ef41a2c"
                                                    hex"2ba577d0fa1628b76d040b12a82492fb"
                                                    hex"2b7a5233cd21581e855e89dc2f1e8a92"
                                                    hex"2b4f95cd46904d05d72bdcde337d9cc7"
                                                    hex"2b2540fc9b4d9abba3faca6691914675"
                                                    hex"2afb5229f68d0830d8be8adb0a0db70f"
                                                    hex"2ad1c7c63a9b294c5bc73a3ba3ab7a2b"
                                                    hex"2aa8a04ac3cbe1ee1c9c86361465dbb8"
                                                    hex"2a7fda392d725a44a2c8aeb9ab35430d"
                                                    hex"2a57741b18cde618717792b4faa216db"
                                                    hex"2a2f6c81f5d84dd950a35626d6d5503a";

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
        uint256 xi = x;
        uint256 res = 0;

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

        return res / 0xde1bc4d19efcac82445da75b00000000 + x + FIXED_1; // divide by 34! and then add x^(2-1) * (34! * 2^(2-1) / 2!) + x^(1-1) * (34! * 1^(1-1) / 1!)
    }}

    /**
      * @dev Compute W(x / FIXED_1) / (x / FIXED_1) * FIXED_1
      * Input range: 1 <= x <= LAMBERT_CONV_RADIUS
      * Auto-generated via 'PrintAdvancedMathLambertPos1.py'
    */
    function lambertPos1(uint256 x) internal pure returns (uint256) { unchecked {
        uint256 xi = x;
        uint256 res = (FIXED_1 - x) * 0xde1bc4d19efcac82445da75b00000000; // x^(1-1) * (34! * 1^(1-1) / 1!) - x^(2-1) * (34! * 2^(2-1) / 2!)

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

        return res / 0xde1bc4d19efcac82445da75b00000000; // divide by 34!
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
        uint256 c = read(values, i + 0) * (b - y);
        uint256 d = read(values, i + 1) * (y - a);
        return (c + d) / LAMBERT_POS2_SAMPLE;
    }}

    /**
      * @dev Compute W(x / FIXED_1) / (x / FIXED_1) * FIXED_1
      * Input range: LAMBERT_POS2_MAXVAL + 1 <= x <= 2 ^ 256 - 1
    */
    function lambertPos3(uint256 x) internal pure returns (uint256) { unchecked {
        uint256 a = AnalyticMath.fixedLog(x);
        uint256 b = AnalyticMath.fixedLog(a);
        uint256 c = IntegralMath.mulDivF(FIXED_1, b, a);
        uint256 d = IntegralMath.mulDivF(FIXED_1, a - b + c, x);
        return d;
    }}

    // auxiliary function
    function read(bytes memory array, uint256 index) private pure returns (uint256 result) {
        assembly {result := and(mload(add(array, mul(add(index, 1), LAMBERT_POS2_T_SIZE))), LAMBERT_POS2_T_MASK)}
    }

    // auxiliary function
    function call(function (uint256) pure returns (uint256) f, uint256 x, uint256 y, uint256 z, uint256 w) private pure returns (uint256, uint256) {
        return FractionMath.productRatio(f(IntegralMath.mulDivF(AnalyticMath.fixedLog(IntegralMath.mulDivF(FIXED_1, x, y)), z, w)), z, w, FIXED_1);
    }
}
