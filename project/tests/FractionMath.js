const TestContract = artifacts.require("FractionMathUser");
const Decimal = require("decimal.js");

const MAX_EXP     = Decimal(2).pow(4).sub(1);
const MAX_UINT128 = Decimal(2).pow(128).sub(1);
const MAX_UINT256 = Decimal(2).pow(256).sub(1);

const poweredRatio    = (n, d, exp)      => [n.pow(exp), d.pow(exp)];
const productRatio    = (xn, yn, xd, yd) => [xn.mul(yn), xd.mul(yd)];
const reducedRatio    = (n, d, max)      => [n, d].map(x => x.div(Decimal.max(n, d).div(max).ceil()));
const normalizedRatio = (n, d, scale)    => [n, d].map(x => x.mul(scale).div(n.add(d)));

const poweredRatioCheck    = ()      => (n, d) => true;
const productRatioCheck    = ()      => (n, d) => true;
const reducedRatioCheck    = (max)   => (n, d) => [n, d].every((x) => Decimal(x.toString()).lte(max));
const normalizedRatioCheck = (scale) => (n, d) => [n, d].reduce((sum, x) => sum.add(x.toString()), Decimal(0)).eq(scale);

describe(TestContract.contractName, () => {
    let testContract;

    before(async () => {
        testContract = await TestContract.new();
    });

    for (const fast of [0, 1]) {
        for (let exp = 0; exp <= MAX_EXP; exp++) {
            for (let n = 0; n < 10; n++) {
                for (let d = 1; d <= 10; d++) {
                    test(poweredRatio, poweredRatioCheck, "0", n, d, exp, fast);
                }
            }
        }
    }

    for (const fast of [0, 1]) {
        const maxError = fast ? "0.000000000000000000000002" : "0.000000000000000000000000000000000000000000000000000000000000007";
        for (let exp = 0; exp <= MAX_EXP; exp++) {
            for (let i = 1; i <= 10; i++) {
                const n = MAX_UINT128.mul(i).add(1);
                for (let j = 1; j <= 10; j++) {
                    const d = MAX_UINT128.mul(j).add(1);
                    test(poweredRatio, poweredRatioCheck, maxError, n.toFixed(), d.toFixed(), exp, fast);
                }
            }
        }
    }

    for (const fast of [0, 1]) {
        const maxError = fast ? "0.000000000000000000000002" : "0.000000000000000000000000000000000000000000000000000000000000009";
        for (let exp = 0; exp <= MAX_EXP; exp++) {
            for (let i = 1; i <= 10; i++) {
                const n = MAX_UINT256.sub(MAX_UINT128).divToInt(i);
                for (let j = 1; j <= 10; j++) {
                    const d = MAX_UINT256.sub(MAX_UINT128).divToInt(j);
                    test(poweredRatio, poweredRatioCheck, maxError, n.toFixed(), d.toFixed(), exp, fast);
                }
            }
        }
    }

    for (const xn of [MAX_UINT128, MAX_UINT256.divToInt(2), MAX_UINT256.sub(MAX_UINT128), MAX_UINT256]) {
        for (const yn of [MAX_UINT128, MAX_UINT256.divToInt(2), MAX_UINT256.sub(MAX_UINT128), MAX_UINT256]) {
            for (const xd of [MAX_UINT128, MAX_UINT256.divToInt(2), MAX_UINT256.sub(MAX_UINT128), MAX_UINT256]) {
                for (const yd of [MAX_UINT128, MAX_UINT256.divToInt(2), MAX_UINT256.sub(MAX_UINT128), MAX_UINT256]) {
                    test(productRatio, productRatioCheck, "0.000000000000000000000000000000000000006", xn.toHex(), xd.toHex(), yn.toHex(), yd.toHex());
                }
            }
        }
    }

    for (const z of [Decimal("1e6"), Decimal("1e18"), Decimal("1e30"), MAX_UINT128]) {
        for (let n = 0; n < 10; n++) {
            for (let d = 1; d <= 10; d++) {
                test(reducedRatio   , reducedRatioCheck(z)   , "0.0000000", n, d, z.toFixed());
                test(normalizedRatio, normalizedRatioCheck(z), "0.0000025", n, d, z.toFixed());
            }
        }
    }

    for (const z of [Decimal("1e6"), Decimal("1e18"), Decimal("1e30"), MAX_UINT128]) {
        for (let i = Decimal(1); i.lte(z); i = i.mul(10)) {
            const n = MAX_UINT256.divToInt(z).mul(i).add(1);
            for (let j = Decimal(1); j.lte(z); j = j.mul(10)) {
                const d = MAX_UINT256.divToInt(z).mul(j).add(1);
                test(reducedRatio   , reducedRatioCheck(z)   , "0.135", n.toFixed(), d.toFixed(), z.toFixed());
                test(normalizedRatio, normalizedRatioCheck(z), "0.135", n.toFixed(), d.toFixed(), z.toFixed());
            }
        }
    }

    for (const z of [1023, 1024, 1025]) {
        for (const n of [
            MAX_UINT256.div(5),
            MAX_UINT256.div(3),
            MAX_UINT256.div(2).floor(),
            MAX_UINT256.div(2).ceil(),
            MAX_UINT256.mul(2).div(3),
            MAX_UINT256.mul(3).div(4).floor(),
            MAX_UINT256.mul(3).div(4).ceil(),
            MAX_UINT256.sub(MAX_UINT128),
            MAX_UINT256.sub(1),
            MAX_UINT256
        ]) {
            for (const d of [MAX_UINT256.sub(1), MAX_UINT256]) {
                test(reducedRatio   , reducedRatioCheck(z)   , "0.004", n.toFixed(), d.toFixed(), z);
                test(normalizedRatio, normalizedRatioCheck(z), "0.004", n.toFixed(), d.toFixed(), z);
            }
        }
    }

    for (const z of [1, 2, 3, 4]) {
        for (const n of [1, 2, 3, 4]) {
            for (const d of [MAX_UINT256.sub(1), MAX_UINT256]) {
                test(reducedRatio   , reducedRatioCheck(z)   , "0.0000000000000000000000000000000000000000000000000000000000000000000000000005", n.toFixed(), d.toFixed(), z);
                test(normalizedRatio, normalizedRatioCheck(z), "0.0000000000000000000000000000000000000000000000000000000000000000000000000006", n.toFixed(), d.toFixed(), z);
            }
        }
    }

    function test(method, check, maxError, ...args) {
        it(`${method.name}(${args.join(", ")})`, async () => {
            const expected = method(...args.map(x => Decimal(x)));
            const actual = await testContract[method.name](...args);
            const x = expected[0].mul(actual[1].toString());
            const y = expected[1].mul(actual[0].toString());
            const delta = x.sub(y).abs();
            const error = x.mul(y).gt(0) ? delta.div(y) : delta;
            assert(check(actual[0], actual[1]), "critical error");
            assert(error.lte(maxError), `error = ${error.toFixed()}`);
        });
    }
});
