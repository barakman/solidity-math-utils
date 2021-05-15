const AdvancedMath = artifacts.require("AdvancedMathAdapter");

const Constants = require("./helpers/AnalyticMathConstants.js");

const assertRevert = require("./helpers/Utilities.js").assertRevert;

const Decimal = require("decimal.js");

const W_MIN_X = Decimal(-1).exp().neg();
const FIXED_1 = Decimal(2).pow(Constants.MAX_PRECISION);

function solvable(a, b, c, d) {
    return Decimal(a).div(b).ln().mul(c).div(d).gte(W_MIN_X);
}

function W(x) {
    if (x.gte(W_MIN_X)) {
        let a = x;
        for (let n = 0; n < 215; n++) {
            const e = a.exp();
            a = a.mul(a).mul(e).add(x).div(a.mul(e).add(e));
        }
        return a;
    }
    assert(false);
}

contract("AdvancedMath", () => {
    let advancedMath;
    let sections;

    before(async () => {
        advancedMath = await AdvancedMath.new();
        await advancedMath.init();
        const maxInputValues = await advancedMath.maxInputValues();
        sections = [Decimal(0), ...maxInputValues.map(x => Decimal(x.toString()))];
    });

    for (const a of [1, 2, 3, 4, 5])
        for (const b of [1, 2, 3, 4, 5])
            for (const c of [1, 2, 3, 4, 5])
                for (const d of [1, 2, 3, 4, 5])
                    solveTest(a, b, c, d, "0.19382");

    for (const a of [1, 2, 3, 4, 5].map(n => n + 1000))
        for (const b of [1, 2, 3, 4, 5].map(n => n + 1000))
            for (const c of [1, 2, 3, 4, 5].map(n => n + 1000))
                for (const d of [1, 2, 3, 4, 5].map(n => n + 1000))
                    solveTest(a, b, c, d, "0.00000000000000000000000000000001");

    for (let percent = 0; percent <= 100; percent++) {
        testSuccess("lambertNegTest" , percent, -1, 0, 1, "0.13573");
        testSuccess("lambertPosTest" , percent, +1, 0, 3, "0.07888");
        testSuccess("lambertNeg1Test", percent, -1, 0, 1, "0.13573");
        testSuccess("lambertPos1Test", percent, +1, 0, 1, "0.00353");
        testSuccess("lambertPos2Test", percent, +1, 1, 2, "0.00006");
        testSuccess("lambertPos3Test", percent, +1, 2, 3, "0.07448");
    }

    testFailure("lambertNegTest", 0, 0, "lambertNeg: x < min");
    testFailure("lambertNegTest", 1, 1, "lambertNeg: x > max");
    testFailure("lambertPosTest", 0, 0, "lambertPos: x < min");
    testFailure("lambertPosTest", 3, 1, "lambertPos: x > max");

    function solveTest(a, b, c, d, maxError) {
        if (solvable(a, b, c, d)) {
            it(`solveTest(${a}, ${b}, ${c}, ${d})`, async () => {
                const result = await advancedMath.solveTest(a, b, c, d);
                const x = Decimal(result[0].toString()).div(result[1].toString());
                const error = x.mul(Decimal(a).div(b).pow(x)).div(c).mul(d).sub(1).abs();
                assert(error.lte(maxError), `error = ${error.toFixed()}`);
            });
        }
    }

    function testSuccess(methodName, percent, sign, bgn, end, maxError) {
        it(`${methodName}(${percent}%)`, async () => {
            const x = sections[bgn].add(1).add(sections[end].sub(sections[bgn].add(1)).mul(percent).divToInt(100));
            const expected = W(x.mul(sign).div(FIXED_1)).div(x.mul(sign).div(FIXED_1)).mul(FIXED_1);
            const actual = Decimal((await advancedMath[methodName](x.toFixed())).toString());
            if (!actual.eq(expected)) {
                const error = actual.div(expected).sub(1).abs();
                assert(error.lte(maxError), `error = ${error.toFixed()}`);
            }
        });
    }

    function testFailure(methodName, index, add, errorMessage) {
        it(`${methodName} should revert with '${errorMessage}'`, async () => {
            await assertRevert(advancedMath[methodName](sections[index].add(add).toFixed()), errorMessage);
        });
    }
});
