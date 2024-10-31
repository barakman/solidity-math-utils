const TestContract = artifacts.require("AdvancedMathUser");
const Constants = require("./helpers/Constants.js");
const Utilities = require("./helpers/Utilities.js");
const Decimal = require("decimal.js");

const W_MIN_X = Decimal(-1).exp().neg();
const FIXED_1 = Decimal(Constants.FIXED_1);

const SECTIONS = [
    Decimal(0),
    Decimal(Constants.LAMBERT_CONV_RADIUS),
    Decimal(Constants.LAMBERT_POS2_MAXVAL),
    Decimal(Constants.LAMBERT_POS2_MAXVAL).mul(100)
];

function solvable(a, b, c, d) {
    return Decimal(a).div(b).ln().mul(c).div(d).gte(W_MIN_X);
}

function lambertRatio(x) {
    assert(x.gte(W_MIN_X));
    let a = x.lt(1) ? x : x.ln();
    for (let n = 0; n < 8; n++) {
        const e = a.exp();
        const f = a.mul(e);
        if (f.eq(x)) break;
        a = a.mul(f).add(x).div(f.add(e));
    }
    return a.div(x);
}

describe(TestContract.contractName, () => {
    let testContract;

    before(async () => {
        testContract = await TestContract.new();
    });

    for (const a of [1, 2, 3, 4, 5])
        for (const b of [1, 2, 3, 4, 5])
            for (const c of [1, 2, 3, 4, 5])
                for (const d of [1, 2, 3, 4, 5])
                    testSolve(a, b, c, d, "0.00883");

    for (const a of [1, 2, 3, 4, 5].map(n => n + 1000))
        for (const b of [1, 2, 3, 4, 5].map(n => n + 1000))
            for (const c of [1, 2, 3, 4, 5].map(n => n + 1000))
                for (const d of [1, 2, 3, 4, 5].map(n => n + 1000))
                    testSolve(a, b, c, d, "0.000000000000000000000000000000002");

    for (let percent = 0; percent <= 100; percent++) {
        testSuccess("lambertNeg", percent, -1, 0, 1, "0.13251");
        testSuccess("lambertPos", percent, +1, 0, 3, "0.00261");
        testSuccess("lambertPos", percent, +1, 0, 1, "0.00353");
        testSuccess("lambertPos", percent, +1, 1, 2, "0.00203");
        testSuccess("lambertPos", percent, +1, 2, 3, "0.00262");
    }

    testFailure("lambertNeg", 0, 0, "lambertNeg: x < min");
    testFailure("lambertPos", 0, 0, "lambertPos: x < min");
    testFailure("lambertNeg", 1, 1, "lambertNeg: x > max");

    function testSolve(a, b, c, d, maxError) {
        it(`solve(${a}, ${b}, ${c}, ${d})`, async () => {
            if (solvable(a, b, c, d)) {
                const result = await testContract.solve(a, b, c, d);
                const x = Decimal(result[0].toString()).div(result[1].toString());
                const error = x.mul(Decimal(a).div(b).pow(x)).div(c).mul(d).sub(1).abs();
                assert(error.lte(maxError), `error = ${error.toFixed()}`);
            }
            else {
                await Utilities.assertRevert(testContract.solve(a, b, c, d));
            }
        });
    }

    function testSuccess(methodName, percent, sign, bgn, end, maxError) {
        it(`${methodName}(${percent}%)`, async () => {
            const x = SECTIONS[bgn].add(1).add(SECTIONS[end].sub(SECTIONS[bgn].add(1)).mul(percent).divToInt(100));
            const actual = Decimal((await testContract[methodName](x.toFixed())).toString());
            const expected = lambertRatio(x.mul(sign).div(FIXED_1)).mul(FIXED_1);
            if (!actual.eq(expected)) {
                const error = actual.div(expected).sub(1).abs();
                assert(error.lte(maxError), `error = ${error.toFixed()}`);
            }
        });
    }

    function testFailure(methodName, index, add, errorMessage) {
        it(`${methodName} should revert with '${errorMessage}'`, async () => {
            await Utilities.assertRevert(testContract[methodName](SECTIONS[index].add(add).toFixed()), errorMessage);
        });
    }
});
