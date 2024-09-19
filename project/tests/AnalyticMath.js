const TestContract = artifacts.require("AnalyticMathUser");
const Constants = require("./helpers/Constants.js");
const Utilities = require("./helpers/Utilities.js");
const Decimal = require("decimal.js");

const ZERO = Decimal(0);
const ONE  = Decimal(1);
const TWO  = Decimal(2);

const FIXED_1 = Decimal(Constants.FIXED_1);
const LOG_MID = Decimal(Constants.LOG_MID);
const EXP_MID = Decimal(Constants.EXP_MID);
const EXP_MAX = Decimal(Constants.EXP_MAX);

const MAX_U32 = TWO.pow(32).sub(1)
const MAX_VAL = TWO.pow(256).sub(1);
const MAX_MUL = MAX_VAL.div(FIXED_1).floor();

const pow      = (a, b, c, d) => a.div(b).pow(c.div(d));
const log      = (a, b)       => a.div(b).ln();
const exp      = (a, b)       => a.div(b).exp();
const fixedLog = (x)          => log(x, FIXED_1).mul(FIXED_1);
const fixedExp = (x)          => exp(x, FIXED_1).mul(FIXED_1);

const equalTo    = (x, y)  => x.eq(y);
const lessThan   = (x, y)  => x.lt(y);
const moreThan   = (x, y)  => x.gt(y);
const toInteger  = (value) => Decimal(value.toString());
const toFraction = (tuple) => Decimal(tuple[0].toString()).div(tuple[1].toString());

const portion = (min, max, percent) => min.add(max.sub(min).mul(percent).divToInt(100));

describe(TestContract.contractName, () => {
    let testContract;

    before(async () => {
        testContract = await TestContract.new();
    });

    for (const a of [ZERO, ONE, MAX_VAL]) {
        for (const b of [ZERO, ONE, MAX_VAL]) {
            for (const c of [ZERO, ONE, MAX_VAL]) {
                for (const d of [ZERO, ONE, MAX_VAL]) {
                    if (b.eq(0) || d.eq(0)) {
                        testFailure(pow, "division by zero", a, b, c, d);
                    }
                    else if (a.eq(0) || c.eq(0)) {
                        testSuccess(pow, toFraction, equalTo, "0", a, b, c, d);
                    }
                }
            }
        }
    }

    for (let a = 1; a < 5; a++) {
        for (let b = 1; b <= a; b++) {
            for (let c = 1; c < 5; c++) {
                for (let d = 1; d < 5; d++) {
                    testSuccess(pow, toFraction, lessThan, "0.000000000000000000000000000000000000128", a, b, c, d);
                    testSuccess(pow, toFraction, lessThan, "0.000000000000000000000000000000000000541", 1000000 - a, b, c, d);
                    testSuccess(pow, toFraction, lessThan, "0.000000000000000000000000000000000000572", 1000000 + a, b, c, d);
                    testSuccess(pow, toFraction, moreThan, "0.000000000000000000000000000000000000128", b, a, c, d);
                    testSuccess(pow, toFraction, moreThan, "0.000000000000000000000000000000000000541", b, 1000000 - a, c, d);
                    testSuccess(pow, toFraction, moreThan, "0.000000000000000000000000000000000000572", b, 1000000 + a, c, d);
                }
            }
            testSuccess(log, toFraction, lessThan, "0.000000000000000000000000000000000000090", a, b);
            testSuccess(log, toFraction, lessThan, "0.000000000000000000000000000000000000018", 1000000 - a, 100000 + b);
            testSuccess(log, toFraction, lessThan, "0.000000000000000000000000000000000000018", 1000000 + a, 100000 - b);
            testSuccess(exp, toFraction, lessThan, "0.000000000000000000000000000000000000017", a, b);
            testSuccess(exp, toFraction, lessThan, "0.000000000000000000000000000000000000046", 1000000 - a, 100000 + b);
            testSuccess(exp, toFraction, lessThan, "0.000000000000000000000000000000000000045", 1000000 + a, 100000 - b);
        }
    }

    for (let percent = 1; percent <= 100; percent++) {
        testSuccess(pow, toFraction, lessThan, "0.000000000000000000000000000000000000002", MAX_MUL, MAX_MUL.sub(1), portion(ZERO, MAX_U32, percent), MAX_U32);
        testSuccess(pow, toFraction, lessThan, "0.000000000000000000000000000000000000147", MAX_MUL, MAX_MUL.sub(1), MAX_U32, portion(ZERO, MAX_U32, percent));
        testSuccess(pow, toFraction, lessThan, "0.000000000000000000000000000000000000068", MAX_MUL, portion(MAX_U32, MAX_MUL, percent), MAX_U32.sub(1), MAX_U32);
        testSuccess(pow, toFraction, lessThan, "0.000000000000000000000000000000000000069", MAX_MUL, portion(MAX_U32, MAX_MUL, percent), MAX_U32, MAX_U32.sub(1));
        testSuccess(pow, toFraction, lessThan, "0.000000000000000000000000000000000000584", MAX_MUL, MAX_U32, portion(ZERO, MAX_U32, percent), MAX_U32);
        testSuccess(pow, toFraction, lessThan, "0.000000000000000000000000000000000000787", MAX_MUL, ONE, portion(ZERO, MAX_U32, percent), MAX_U32);
    }

    for (let percent = 0; percent < 100; percent++) {
        testSuccess(fixedLog, toInteger, lessThan, "0.000000000000000000000000000000000000795", portion(FIXED_1, LOG_MID, percent));
        testSuccess(fixedLog, toInteger, lessThan, "0.000000000000000000000000000000000000041", portion(LOG_MID, FIXED_1.mul(4), percent));
        testSuccess(fixedLog, toInteger, lessThan, "0.000000000000000000000000000000000000006", portion(FIXED_1.mul(4), MAX_VAL, percent));
        testSuccess(fixedExp, toInteger, lessThan, "0.000000000000000000000000000000000000027", portion(ZERO, EXP_MID, percent));
        testSuccess(fixedExp, toInteger, lessThan, "0.000000000000000000000000000000000000061", portion(EXP_MID, EXP_MID.mul(2), percent));
        testSuccess(fixedExp, toInteger, lessThan, "0.000000000000000000000000000000000000293", portion(EXP_MID.mul(2), EXP_MAX, percent));
    }

    testSuccess(pow, toFraction, lessThan, "0.000000000000000000000000000000000000587", MAX_MUL, MAX_U32.sub(1), MAX_U32, MAX_U32);
    testSuccess(pow, toFraction, lessThan, "0.000000000000000000000000000000000000593", MAX_MUL, MAX_U32, MAX_U32.sub(1), MAX_U32);
    testSuccess(pow, toFraction, lessThan, "0.000000000000000000000000000000000000588", MAX_MUL, MAX_U32, MAX_U32, MAX_U32.sub(1));

    testSuccess(fixedLog, toInteger, lessThan, "0.000000000000000000000000000000000000014", LOG_MID.sub(1));
    testSuccess(fixedLog, toInteger, lessThan, "0.000000000000000000000000000000000000036", LOG_MID.add(1));
    testSuccess(fixedLog, toInteger, lessThan, "0.000000000000000000000000000000000000006", MAX_VAL);

    testSuccess(fixedExp, toInteger, lessThan, "0.000000000000000000000000000000000000027", EXP_MID.sub(1));
    testSuccess(fixedExp, toInteger, lessThan, "0.000000000000000000000000000000000000035", EXP_MID.add(1));
    testSuccess(fixedExp, toInteger, lessThan, "0.000000000000000000000000000000000000289", EXP_MAX.sub(1));

    testFailure(pow, "without a reason", MAX_MUL.add(1), ONE, ONE, ONE);
    testFailure(pow, "without a reason", ONE, MAX_MUL.add(1), ONE, ONE);
    testFailure(log, "without a reason", MAX_MUL.add(1), ONE);
    testFailure(exp, "without a reason", MAX_MUL.add(1), ONE);

    testFailure(log, "fixedLog: x < min", 1, 2);
    testFailure(exp, "fixedExp: x > max", 178, 1);
    testFailure(fixedLog, "fixedLog: x < min", FIXED_1.sub(1));
    testFailure(fixedExp, "fixedExp: x > max", EXP_MAX.sub(0));

    function testSuccess(method, toActual, check, maxError, ...args) {
        it(`${method.name}(${args.map(x => x.toFixed()).join(", ")})`, async () => {
            const actual = toActual(await testContract[method.name](...args.map(x => x.toFixed())));
            const expected = method(...args.map(x => Decimal(x)));
            if (!actual.eq(expected)) {
                const error = actual.div(expected).sub(1).abs();
                assert(check(actual, expected), "critical error");
                assert(error.lte(maxError), `error = ${error.toFixed()}`);
            }
        });
    }

    function testFailure(method, errorMsg, ...args) {
        it(`${method.name}(${args.map(x => x.toFixed()).join(", ")})`, async () => {
            await Utilities.assertRevert(testContract[method.name](...args.map(x => x.toFixed())), errorMsg);
        });
    }
});
