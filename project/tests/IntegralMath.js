const IntegralMath = artifacts.require("IntegralMathUser");

const Decimal = require("decimal.js");

const roundDiv  = (n, d) => n.div(d).add(0.5).floor();
const floorLog2 = (n) => n.log(2).floor();
const floorSqrt = (n) => n.sqrt().floor();
const ceilSqrt  = (n) => n.sqrt().ceil();

contract("IntegralMath", () => {
    let integralMath;

    before(async () => {
        integralMath = await IntegralMath.new();
    });

    for (let i = 0; i < 10; i++) {
        const x = Decimal(2).pow(256).sub(i + 1).toHex();
        for (let j = 1; j <= 10; j++) {
            const y = Decimal(2).pow(256).sub(j).toHex();
            for (const [n, d] of [[i, j], [x, j], [i, y], [x, y]]) {
                test(roundDiv, n, d);
            }
        }
    }

    for (let n = 1; n <= 256; n++) {
        for (const k of n < 256 ? [-1, 0, +1] : [-1]) {
            test(floorLog2, Decimal(2).pow(n).add(k).toHex());
        }
    }

    for (let n = 1; n <= 256; n++) {
        for (const k of n < 256 ? [-1, 0, +1] : [-1]) {
            test(floorSqrt, Decimal(2).pow(n).add(k).toHex());
        }
    }

    for (let n = 1; n <= 256; n++) {
        for (const k of n < 256 ? [-1, 0, +1] : [-1]) {
            test(ceilSqrt, Decimal(2).pow(n).add(k).toHex());
        }
    }

    function test(method, ...args) {
        it(`${method.name}(${args.join(", ")})`, async () => {
            const expected = method(...args.map(x => Decimal(x)));
            const actual = await integralMath[method.name](...args);
            assert(expected.eq(actual.toString()), `expected ${expected.toFixed()} but got ${actual.toString()}`);
        });
    }
});
