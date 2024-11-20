const TestContract = artifacts.require("AdvancedMathUser");
const Constants = require("./helpers/Constants.js");
const Utilities = require("./helpers/Utilities.js");
const Decimal = require("decimal.js");

const W_MIN_X = Decimal(-1).exp().neg();
const FIXED_1 = Decimal(Constants.FIXED_1);

const LAMBERT_NEG0 = Decimal(0);
const LAMBERT_NEG1 = Decimal(Constants.LAMBERT_NEG1_MAXVAL);
const LAMBERT_NEG2 = Decimal(Constants.LAMBERT_NEG2_MAXVAL);
const LAMBERT_POS0 = Decimal(0);
const LAMBERT_POS1 = Decimal(Constants.LAMBERT_POS1_MAXVAL);
const LAMBERT_POS2 = Decimal(Constants.LAMBERT_POS2_MAXVAL);
const LAMBERT_POS3 = Decimal(Constants.LAMBERT_POS2_MAXVAL).mul(100);

const LAMBERT_POS_EXACT_MAX_VAL = Decimal("0x000a13db974da98db99f369a126e720f563fffffffffffffffffffffffffffff");
const LAMBERT_POS_QUICK_MAX_VAL = Decimal("0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff");

const SIGN = {
    lambertNegExact: -1,
    lambertPosExact: +1,
    lambertNegQuick: -1,
    lambertPosQuick: +1,
};

function solvable(a, b, c, d) {
    return Decimal(a).div(b).ln().mul(c).div(d).gte(W_MIN_X);
}

function lambertRatio(x) {
    assert(x.gte(W_MIN_X));
    let y = x.lt(1) ? x : x.ln();
    for (let n = 0; n < 8; n++) {
        const e = y.exp();
        const f = y.mul(e);
        if (f.eq(x)) break;
        y = y.mul(f).add(x).div(f.add(e));
    }
    return y.div(x);
}

describe(TestContract.contractName, () => {
    let testContract;

    before(async () => {
        testContract = await TestContract.new();
    });

    for (const a of [1, 2, 3, 4, 5]) {
        for (const b of [1, 2, 3, 4, 5]) {
            for (const c of [1, 2, 3, 4, 5]) {
                for (const d of [1, 2, 3, 4, 5]) {
                    testSolve("solveExact", a, b, c, d, "0.00000000000000000000010142175418052637");
                    testSolve("solveQuick", a, b, c, d, "0.00478611537034482992866132560056904476");
                }
            }
        }
    }

    for (const a of [1, 2, 3, 4, 5].map(n => n + 1000)) {
        for (const b of [1, 2, 3, 4, 5].map(n => n + 1000)) {
            for (const c of [1, 2, 3, 4, 5].map(n => n + 1000)) {
                for (const d of [1, 2, 3, 4, 5].map(n => n + 1000)) {
                    testSolve("solveExact", a, b, c, d, "0.00000000000000000000000000000000001082");
                    testSolve("solveQuick", a, b, c, d, "0.00000000000000000000000000000000103095");
                }
            }
        }
    }

    for (let percent = 0; percent <= 100; percent++) {
        testSuccess("lambertNegExact", percent, LAMBERT_NEG0, LAMBERT_NEG1, "0.00000000000000000000000000000000000088");
        testSuccess("lambertNegExact", percent, LAMBERT_NEG1, LAMBERT_NEG2, "0.00000000000000000000000000000000000259");
        testSuccess("lambertPosExact", percent, LAMBERT_POS0, LAMBERT_POS1, "0.00000000000000000000000000000000000097");
        testSuccess("lambertPosExact", percent, LAMBERT_POS1, LAMBERT_POS2, "0.00000000000000000000000000000000000006");
        testSuccess("lambertPosExact", percent, LAMBERT_POS2, LAMBERT_POS3, "0.00000000000000000000000000000000000230");
    }

    for (let percent = 0; percent <= 100; percent++) {
        testSuccess("lambertNegQuick", percent, LAMBERT_NEG0, LAMBERT_NEG1, "0.04458843601911142612093766473768569069");
        testSuccess("lambertNegQuick", percent, LAMBERT_NEG1, LAMBERT_NEG2, "0.00656991066935660006721266366675943493");
        testSuccess("lambertPosQuick", percent, LAMBERT_POS0, LAMBERT_POS1, "0.00352502537296632393189150614600911966");
        testSuccess("lambertPosQuick", percent, LAMBERT_POS1, LAMBERT_POS2, "0.00202834415207521945800897906620169050");
        testSuccess("lambertPosQuick", percent, LAMBERT_POS2, LAMBERT_POS3, "0.00261178569717540774470351850757097501");
    }

    for (let percent = 0; percent <= 100; percent++) {
        testSuccess("lambertPosExact", percent, LAMBERT_POS3, LAMBERT_POS_EXACT_MAX_VAL, "0.00000724581731315842051513071553963081");
        testSuccess("lambertPosQuick", percent, LAMBERT_POS3, LAMBERT_POS_QUICK_MAX_VAL, "0.04077461765786128270949836764496569026");
    }

    for (let i = 1; i <= 50; i++) {
        for (let j = 0; j <= i; j++) {
            testFailure("lambertPosExact", LAMBERT_POS_EXACT_MAX_VAL.add(2 ** i - j), "with panic code");
            testFailure("lambertPosExact", LAMBERT_POS_QUICK_MAX_VAL.sub(2 ** i - j), "without a reason");
        }
    }

    testFailure("lambertPosExact", LAMBERT_POS0.add(0), "lambertPosExact: x < min");
    testFailure("lambertPosQuick", LAMBERT_POS0.add(0), "lambertPosQuick: x < min");

    testFailure("lambertNegExact", LAMBERT_NEG0.add(0), "lambertNegExact: x < min");
    testFailure("lambertNegQuick", LAMBERT_NEG0.add(0), "lambertNegQuick: x < min");

    testFailure("lambertNegExact", LAMBERT_NEG2.add(1), "lambertNegExact: x > max");
    testFailure("lambertNegQuick", LAMBERT_NEG2.add(1), "lambertNegQuick: x > max");

    function testSolve(methodName, a, b, c, d, maxError) {
        it(`${methodName}(${a}, ${b}, ${c}, ${d})`, async () => {
            if (solvable(a, b, c, d)) {
                const result = await testContract[methodName](a, b, c, d);
                const x = Decimal(result[0].toString()).div(result[1].toString());
                const error = x.mul(Decimal(a).div(b).pow(x)).div(c).mul(d).sub(1).abs();
                assert(error.lte(maxError), `error = ${error.toFixed()}`);
            }
            else {
                await Utilities.assertRevert(testContract[methodName](a, b, c, d));
            }
        });
    }

    function testSuccess(methodName, percent, minVal, maxVal, maxError) {
        it(`${methodName}(${percent}%)`, async () => {
            const val = minVal.add(1).add(maxVal.sub(minVal.add(1)).mul(percent).divToInt(100));
            const actual = Decimal((await testContract[methodName](val.toFixed())).toString());
            const expected = lambertRatio(val.mul(SIGN[methodName]).div(FIXED_1)).mul(FIXED_1);
            if (!actual.eq(expected)) {
                const error = actual.div(expected).sub(1).abs();
                assert(error.lte(maxError), `error = ${error.toFixed()}`);
            }
        });
    }

    function testFailure(methodName, val, errorMsg) {
        it(`${methodName}(${val.toHex()})`, async () => {
            await Utilities.assertRevert(testContract[methodName](val.toFixed()), errorMsg);
        });
    }
});
