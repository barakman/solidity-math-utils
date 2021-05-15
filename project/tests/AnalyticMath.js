const AnalyticMath = artifacts.require("AnalyticMathAdapter");

const Constants = require("./helpers/AnalyticMathConstants.js");

const assertRevert = require("./helpers/Utilities.js").assertRevert;

const Decimal = require("decimal.js");

const BN = web3.utils.BN;

function assertAlmostEqual(actual, expected, maxError) {
    if (!actual.eq(expected)) {
        assert(actual.lt(expected), "critical error");
        const error = actual.div(expected).sub(1).abs();
        assert(error.lte(maxError), `error = ${error.toFixed()}`);
    }
}

contract("AnalyticMath", () => {
    let analyticMath;

    before(async () => {
        analyticMath = await AnalyticMath.new();
        await analyticMath.init();
    });

    describe("exponentiation tests:", () => {
        const MAX_BASE = Decimal(2).pow(256 - Constants.MAX_PRECISION).sub(1);
        const MAX_EXP  = Decimal(2).pow(32).sub(1);

        for (let percent = 1; percent <= 100; percent++) {
            powTestSuccess(
                MAX_BASE,
                MAX_BASE.sub(1),
                MAX_EXP.mul(percent).divToInt(100),
                MAX_EXP,
                "0.00000000000000000000000000000000000001"
            );
        }

        for (let percent = 1; percent <= 100; percent++) {
            powTestSuccess(
                MAX_BASE,
                MAX_BASE.sub(1),
                MAX_EXP,
                MAX_EXP.mul(percent).divToInt(100),
                "0.000000000000000000000000000000000001"
            );
        }

        for (let percent = 1; percent <= 17; percent++) {
            powTestSuccess(
                MAX_BASE,
                Decimal(1),
                MAX_EXP.mul(percent).divToInt(100),
                MAX_EXP,
                "0.00000000000000000000000000000000001"
            );
        }

        for (let percent = 64; percent <= 100; percent++) {
            powTestFailure(
                MAX_BASE,
                Decimal(1),
                MAX_EXP.mul(percent).divToInt(100),
                MAX_EXP,
                "findPosition: x > max"
            );
        }

        for (let percent = 1; percent <= 100; percent++) {
            powTestFailure(
                MAX_BASE,
                Decimal(1),
                MAX_EXP,
                MAX_EXP.mul(percent).divToInt(100),
                "findPosition: x > max"
            );
        }
    });

    describe("overflow tests:", () => {
        const MULTIPLIER = Decimal(2).pow(256 - Constants.MAX_PRECISION).toFixed();
        overflowTest("pow", MULTIPLIER, 1, 1, 1);
        overflowTest("pow", 1, MULTIPLIER, 1, 1);
        overflowTest("log", MULTIPLIER, 1);
        overflowTest("exp", MULTIPLIER, 1);
    });

    describe("precision tests:", () => {
        const LOG_MIN = Decimal(1);
        const EXP_MIN = Decimal(0);
        const LOG_MAX = Decimal.exp(Constants.LOG_MAX_HI_TERM_VAL);
        const EXP_MAX = Decimal(2).pow(Constants.EXP_MAX_HI_TERM_VAL);
        const FIXED_1 = Decimal(2).pow(Constants.MAX_PRECISION);

        for (let n = 0; n < 256 - Constants.MAX_PRECISION; n++) {
            for (const x of [
                Decimal(2).pow(n),
                Decimal(2).pow(n).add(1),
                Decimal(2).pow(n).mul(1.5),
                Decimal(2).pow(n + 1).sub(1),
            ]) {
                it(`generalLog(${x.toFixed()})`, async () => {
                    const output = await analyticMath.generalLogTest(x.mul(FIXED_1).toFixed(0));
                    const actual = Decimal(output.toString());
                    const expected = x.ln().mul(FIXED_1);
                    assertAlmostEqual(actual, expected, "0.000000000000000000000000000000000001");
                });
            }
        }

        for (let percent = 0; percent < 100; percent++) {
            const x = Decimal(percent).div(100).mul(LOG_MAX.sub(LOG_MIN)).add(LOG_MIN);

            it(`optimalLog(${x.toFixed()})`, async () => {
                const output = await analyticMath.optimalLogTest(x.mul(FIXED_1).toFixed(0));
                const actual = Decimal(output.toString());
                const expected = x.ln().mul(FIXED_1);
                assertAlmostEqual(actual, expected, "0.00000000000000000000000000000000001");
            });
        }

        for (let percent = 0; percent < 100; percent++) {
            const x = Decimal(percent).div(100).mul(EXP_MAX.sub(EXP_MIN)).add(EXP_MIN);

            it(`optimalExp(${x.toFixed()})`, async () => {
                const output = await analyticMath.optimalExpTest(x.mul(FIXED_1).toFixed(0));
                const actual = Decimal(output.toString());
                const expected = x.exp().mul(FIXED_1);
                assertAlmostEqual(actual, expected, "0.00000000000000000000000000000000001");
            });
        }

        it(`optimalLog with max input value`, async () => {
            const input = LOG_MAX.mul(FIXED_1).sub(1).ceil().toFixed();
            const output = await analyticMath.optimalLogTest(input);
            const actual = Decimal(output.toString());
            const expected = LOG_MAX.ln().mul(FIXED_1);
            assertAlmostEqual(actual, expected, "0.0000000000000000000000000000000000001");
        });

        it(`optimalExp with max input value`, async () => {
            const input = EXP_MAX.mul(FIXED_1).sub(1).ceil().toFixed();
            const output = await analyticMath.optimalExpTest(input);
            const actual = Decimal(output.toString());
            const expected = EXP_MAX.exp().mul(FIXED_1);
            assertAlmostEqual(actual, expected, "0.00000000000000000000000000000000001");
        });
    });

    describe("internal tests:", () => {
        for (let precision = Constants.MAX_PRECISION + 1; precision <= 256; precision++) {
            const input = new BN(1).shln(precision).subn(1);

            it(`generalLog(0x${input.toString(16)})`, async () => {
                const output = await analyticMath.generalLogTest(input);
                assert(output.shrn(256 - 32).eqn(0));
            });
        }

        for (let precision = 1; precision <= Constants.MAX_PRECISION; precision++) {
            const minExp = new BN(Constants.maxExpArray[precision - 1].slice(2), 16).addn(1);
            const minVal = new BN(1).shln(precision);

            it(`generalExp(0x${minExp.toString(16)}, ${precision})`, async () => {
                const output = await analyticMath.generalExpTest(minExp, precision);
                assert(output.gte(minVal));
            });
        }

        for (let precision = 0; precision <= Constants.MAX_PRECISION; precision++) {
            const maxExp = new BN(Constants.maxExpArray[precision].slice(2), 16);
            const maxVal = new BN(Constants.maxValArray[precision].slice(2), 16);

            it(`generalExp(0x${maxExp.toString(16)}, ${precision})`, async () => {
                const output = await analyticMath.generalExpTest(maxExp, precision);
                assert(output.eq(maxVal));
            });

            it(`generalExp(0x${maxExp.addn(1).toString(16)}, ${precision})`, async () => {
                const output = await analyticMath.generalExpTest(maxExp.addn(1), precision);
                assert(output.lt(maxVal));
            });
        }

        for (let precision = 0; precision <= Constants.MAX_PRECISION; precision++) {
            const maxExp = new BN(Constants.maxExpArray[precision].slice(2), 16);
            const mulVal = new BN(1).shln(Constants.MAX_PRECISION - precision);

            for (const testCase of [
                {input: maxExp.addn(0).mul(mulVal).subn(1), expectedOutput: precision - 0},
                {input: maxExp.addn(0).mul(mulVal).subn(0), expectedOutput: precision - 0},
                {input: maxExp.addn(1).mul(mulVal).subn(1), expectedOutput: precision - 0},
                {input: maxExp.addn(1).mul(mulVal).subn(0), expectedOutput: precision - 1},
            ]) {
                it(`findPosition(0x${testCase.input.toString(16)})`, async () => {
                    if (testCase.expectedOutput >= Constants.MIN_PRECISION) {
                        const output = await analyticMath.findPositionTest(testCase.input);
                        assert(output.eqn(testCase.expectedOutput));
                    }
                    else {
                        await assertRevert(analyticMath.findPositionTest(testCase.input), "findPosition: x > max");
                    }
                });
            }
        }
    });

    function powTestSuccess(a, b, c, d, maxError) {
        it(`pow(${[a, b, c, d].map(x => x.toFixed()).join(", ")})`, async () => {
            const output = await analyticMath.powTest(...[a, b, c, d].map(x => x.toFixed()));
            const actual = Decimal(output[0].toString()).div(output[1].toString());
            const expected = a.div(b).pow(c.div(d));
            assertAlmostEqual(actual, expected, maxError);
        });
    }

    function powTestFailure(a, b, c, d, errorMsg) {
        it(`pow(${[a, b, c, d].map(x => x.toFixed()).join(", ")})`, async () => {
            await assertRevert(analyticMath.powTest(...[a, b, c, d].map(x => x.toFixed())), errorMsg);
        });
    }

    function overflowTest(methodName, ...args) {
        it(`${methodName}(${args.join(", ")}) should revert`, async () => {
            await assertRevert(analyticMath[methodName + "Test"](...args), "");
        });
    }
});
