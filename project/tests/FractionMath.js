const TestContract = artifacts.require("FractionMathUser");
const Decimal = require("decimal.js");

const MAX_EXP     = Decimal(2).pow(4).sub(1);
const MAX_UINT128 = Decimal(2).pow(128).sub(1);
const MAX_UINT256 = Decimal(2).pow(256).sub(1);

const poweredRatioExact = (n, d, exp)      => [n.pow(exp), d.pow(exp)];
const poweredRatioQuick = (n, d, exp)      => [n.pow(exp), d.pow(exp)];
const productRatio      = (xn, yn, xd, yd) => [xn.mul(yn), xd.mul(yd)];
const reducedRatio      = (n, d, max)      => [n, d].map(x => x.div(Decimal.max(n, d).div(max).ceil()));
const normalizedRatio   = (n, d, scale)    => [n, d].map(x => x.mul(scale).div(n.add(d)));

const noCheck              = ()      => (n, d) => true;
const reducedRatioCheck    = (max)   => (n, d) => [n, d].every((x) => Decimal(x.toString()).lte(max));
const normalizedRatioCheck = (scale) => (n, d) => [n, d].reduce((sum, x) => sum.add(x.toString()), Decimal(0)).eq(scale);

describe(TestContract.contractName, () => {
    let testContract;

    before(async () => {
        testContract = await TestContract.new();
    });

    for (let exp = 0; exp <= MAX_EXP; exp++) {
        for (let n = 0; n < 10; n++) {
            for (let d = 1; d <= 10; d++) {
                test(poweredRatioExact, noCheck, "0", n, d, exp);
                test(poweredRatioQuick, noCheck, "0", n, d, exp);
            }
        }
    }

    for (let exp = 0; exp <= MAX_EXP; exp++) {
        for (const n of [0, 1, 2, 3].map(k => MAX_UINT128.sub(k))) {
            for (const d of [0, 1, 2, 3].map(k => MAX_UINT128.sub(k))) {
                test(poweredRatioExact, noCheck, "0.00000000000000000000000000000000000000000000000000000000000000000000000000004", n.toHex(), d.toHex(), exp);
                test(poweredRatioQuick, noCheck, "0.00000000000000000000000000000000000000000000000000000000000000000000000000817", n.toHex(), d.toHex(), exp);
            }
        }
    }

    for (let exp = 0; exp <= MAX_EXP; exp++) {
        for (const n of [0, 1, 2, 3].map(k => MAX_UINT256.sub(k))) {
            for (const d of [0, 1, 2, 3].map(k => MAX_UINT256.sub(k))) {
                test(poweredRatioExact, noCheck, "0.00000000000000000000000000000000000000000000000000000000000000000000000000013", n.toHex(), d.toHex(), exp);
                test(poweredRatioQuick, noCheck, "0.00000000000000000000000000000000000000000000000000000000000000000000000000039", n.toHex(), d.toHex(), exp);
            }
        }
    }

    for (let exp = 0; exp <= MAX_EXP; exp++) {
        for (let i = 1; i <= 10; i++) {
            const n = MAX_UINT128.mul(i).add(1);
            for (let j = 1; j <= 10; j++) {
                const d = MAX_UINT128.mul(j).add(1);
                test(poweredRatioExact, noCheck, "0.00000000000000000000000000000000000000000000000000000000000000683775553857226", n.toHex(), d.toHex(), exp);
                test(poweredRatioQuick, noCheck, "0.00000000000000000000000115365434694928281518027476953063103593095316751502886", n.toHex(), d.toHex(), exp);
            }
        }
    }

    for (let exp = 0; exp <= MAX_EXP; exp++) {
        for (let i = 1; i <= 10; i++) {
            const n = MAX_UINT256.sub(MAX_UINT128).divToInt(i);
            for (let j = 1; j <= 10; j++) {
                const d = MAX_UINT256.sub(MAX_UINT128).divToInt(j);
                test(poweredRatioExact, noCheck, "0.00000000000000000000000000000000000000000000000000000000000000856782943372566", n.toHex(), d.toHex(), exp);
                test(poweredRatioQuick, noCheck, "0.00000000000000000000000115365434694932248811461502173402498083485327146452151", n.toHex(), d.toHex(), exp);
            }
        }
    }

    for (const xn of [MAX_UINT128, MAX_UINT256.divToInt(2), MAX_UINT256.sub(MAX_UINT128), MAX_UINT256]) {
        for (const yn of [MAX_UINT128, MAX_UINT256.divToInt(2), MAX_UINT256.sub(MAX_UINT128), MAX_UINT256]) {
            for (const xd of [MAX_UINT128, MAX_UINT256.divToInt(2), MAX_UINT256.sub(MAX_UINT128), MAX_UINT256]) {
                for (const yd of [MAX_UINT128, MAX_UINT256.divToInt(2), MAX_UINT256.sub(MAX_UINT128), MAX_UINT256]) {
                    test(productRatio, noCheck, "0.000000000000000000000000000000000000006", xn.toHex(), xd.toHex(), yn.toHex(), yd.toHex());
                }
            }
        }
    }

    for (const z of [Decimal("1e6"), Decimal("1e18"), Decimal("1e30"), MAX_UINT128]) {
        for (let n = 0; n < 10; n++) {
            for (let d = 1; d <= 10; d++) {
                test(reducedRatio   , reducedRatioCheck   (z), "0.0000000", n, d, z.toHex());
                test(normalizedRatio, normalizedRatioCheck(z), "0.0000025", n, d, z.toHex());
            }
        }
    }

    for (const z of [Decimal("1e6"), Decimal("1e18"), Decimal("1e30"), MAX_UINT128]) {
        for (let i = Decimal(1); i.lte(z); i = i.mul(10)) {
            const n = MAX_UINT256.divToInt(z).mul(i).add(1);
            for (let j = Decimal(1); j.lte(z); j = j.mul(10)) {
                const d = MAX_UINT256.divToInt(z).mul(j).add(1);
                test(reducedRatio   , reducedRatioCheck   (z), "0.1342746", n.toHex(), d.toHex(), z.toHex());
                test(normalizedRatio, normalizedRatioCheck(z), "0.1342746", n.toHex(), d.toHex(), z.toHex());
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
                test(reducedRatio   , reducedRatioCheck   (z), "0.0019513", n.toHex(), d.toHex(), z);
                test(normalizedRatio, normalizedRatioCheck(z), "0.0035088", n.toHex(), d.toHex(), z);
            }
        }
    }

    for (const n of [1, 2, 3, 4]) {
        for (const d of [0, 1, 2, 3].map(k => MAX_UINT128.sub(k))) {
            for (const z of [0, 1, 2, 3].map(k => MAX_UINT128.sub(k))) {
                test(reducedRatio   , reducedRatioCheck   (z), "0.00000000000000000000000000000000000000881620763116715630976552402916684258367", n, d.toHex(), z.toHex());
                test(normalizedRatio, normalizedRatioCheck(z), "0.00000000000000000000000000000000000002057115113939003138945288940138929936189", n, d.toHex(), z.toHex());
            }
        }
    }

    for (const n of [1, 2, 3, 4]) {
        for (const d of [0, 1, 2, 3].map(k => MAX_UINT256.sub(k))) {
            for (const z of [0, 1, 2, 3].map(k => MAX_UINT256.sub(k))) {
                test(reducedRatio   , reducedRatioCheck   (z), "0.00000000000000000000000000000000000000000000000000000000000000000000000000003", n, d.toHex(), z.toHex());
                test(normalizedRatio, normalizedRatioCheck(z), "0.00000000000000000000000000000000000000000000000000000000000000000000000000007", n, d.toHex(), z.toHex());
            }
        }
    }

    for (const n of [0, 1, 2, 3].map(k => MAX_UINT256.sub(k))) {
        for (const d of [0, 1, 2, 3].map(k => MAX_UINT256.sub(k))) {
            for (const z of [0, 1, 2, 3].map(k => MAX_UINT128.sub(k))) {
                test(reducedRatio   , reducedRatioCheck   (z), "0.00000000000000000000000000000000000000000000000000000000000000000000000000003", n.toHex(), d.toHex(), z.toHex());
                test(normalizedRatio, normalizedRatioCheck(z), "0.00000000000000000000000000000000000000587747175411143753984368268611122838918", n.toHex(), d.toHex(), z.toHex());
            }
        }
    }

    function test(method, check, maxError, ...args) {
        it(`${method.name}(${args.join(", ")})`, async () => {
            const expected = method(...args.map(x => Decimal(x)));
            const actual = await testContract[method.name](...args);
            const x = expected[0].mul(actual[1].toString());
            const y = expected[1].mul(actual[0].toString());
            if (!x.eq(y)) {
                const error = x.sub(y).abs().div(y);
                assert(check(actual[0], actual[1]), "critical error");
                assert(error.lte(maxError), `error = ${error.toFixed()}`);
            }
        });
    }
});
