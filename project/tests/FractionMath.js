const FractionMath = artifacts.require("FractionMathUser");

const Decimal = require("decimal.js");

const MAX_EXP     = Decimal(2).pow(4).sub(1);
const MAX_UINT128 = Decimal(2).pow(128).sub(1);
const MAX_UINT256 = Decimal(2).pow(256).sub(1);

const poweredRatio    = (n, d, exp) => [n, d].map(x => x.pow(exp));
const productRatio    = (xn, yn, xd, yd) => [Decimal(xn).mul(yn), Decimal(xd).mul(yd)];
const reducedRatio    = (n, d, max) => normalizedRatio(n, d, Decimal.min(n.add(d), max));
const normalizedRatio = (n, d, scale) => [n, d].map(x => x.mul(scale).div(n.add(d)));

contract("FractionMath", () => {
    let fractionMath;

    before(async () => {
        fractionMath = await FractionMath.new();
    });

    for (const fast of [0, 1]) {
        for (let exp = 0; exp <= MAX_EXP; exp++) {
            for (let n = 0; n < 10; n++) {
                for (let d = 1; d <= 10; d++) {
                    test(poweredRatio, "0", "0", n, d, exp, fast);
                }
            }
        }
    }

    for (const fast of [0, 1]) {
        const maxRelativeError = fast ? "0.000000000000000000000001" : "0.00000000000000000000000000000000000000000000000000000000000001";
        for (let exp = 0; exp <= MAX_EXP; exp++) {
            for (let i = 1; i <= 10; i++) {
                const n = MAX_UINT128.mul(i).add(1);
                for (let j = 1; j <= 10; j++) {
                    const d = MAX_UINT128.mul(j).add(1);
                    test(poweredRatio, "0", maxRelativeError, n.toFixed(), d.toFixed(), exp, fast);
                }
            }
        }
    }

    for (const fast of [0, 1]) {
        const maxRelativeError = fast ? "0.000000000000000000000001" : "0.00000000000000000000000000000000000000000000000000000000000001";
        for (let exp = 0; exp <= MAX_EXP; exp++) {
            for (let i = 1; i <= 10; i++) {
                const n = MAX_UINT256.sub(MAX_UINT128).divToInt(i);
                for (let j = 1; j <= 10; j++) {
                    const d = MAX_UINT256.sub(MAX_UINT128).divToInt(j);
                    test(poweredRatio, "0", maxRelativeError, n.toFixed(), d.toFixed(), exp, fast);
                }
            }
        }
    }

    for (const xn of [MAX_UINT128, MAX_UINT256.divToInt(2), MAX_UINT256.sub(MAX_UINT128), MAX_UINT256]) {
        for (const yn of [MAX_UINT128, MAX_UINT256.divToInt(2), MAX_UINT256.sub(MAX_UINT128), MAX_UINT256]) {
            for (const xd of [MAX_UINT128, MAX_UINT256.divToInt(2), MAX_UINT256.sub(MAX_UINT128), MAX_UINT256]) {
                for (const yd of [MAX_UINT128, MAX_UINT256.divToInt(2), MAX_UINT256.sub(MAX_UINT128), MAX_UINT256]) {
                    test(productRatio, "0", "0.00000000000000000000000000000000000001", xn.toHex(), xd.toHex(), yn.toHex(), yd.toHex());
                }
            }
        }
    }

    for (const max of [Decimal("1e6"), Decimal("1e18"), Decimal("1e30"), MAX_UINT128]) {
        for (let n = 0; n < 10; n++) {
            for (let d = 1; d <= 10; d++) {
                test(reducedRatio, "0", "0", n, d, max.toFixed());
            }
        }
    }

    for (const max of [Decimal("1e6"), Decimal("1e18"), Decimal("1e30"), MAX_UINT128]) {
        for (let i = Decimal(1); i.lte(max); i = i.mul(10)) {
            const n = MAX_UINT256.divToInt(max).mul(i).add(1);
            for (let j = Decimal(1); j.lte(max); j = j.mul(10)) {
                const d = MAX_UINT256.divToInt(max).mul(j).add(1);
                test(reducedRatio, "0", "0.135", n.toFixed(), d.toFixed(), max.toFixed());
            }
        }
    }

    for (let max = 1; max <= 4; max++) {
        for (const n of [
            MAX_UINT256.div(3).floor(),
            MAX_UINT256.div(3).ceil(),
            MAX_UINT256.div(2).floor(),
            MAX_UINT256.div(2).ceil(),
            MAX_UINT256.mul(2).div(3).floor(),
            MAX_UINT256.mul(2).div(3).ceil(),
            MAX_UINT256.mul(3).div(4).floor(),
            MAX_UINT256.mul(3).div(4).ceil(),
            MAX_UINT256.sub(1),
            MAX_UINT256
        ]) {
            for (const d of [MAX_UINT256.sub(1), MAX_UINT256]) {
                test(reducedRatio, "1.6", "0", n.toFixed(), d.toFixed(), max);
            }
        }
    }

    for (const scale of [Decimal("1e6"), Decimal("1e18"), Decimal("1e30"), MAX_UINT128]) {
        for (let n = 0; n < 10; n++) {
            for (let d = 1; d <= 10; d++) {
                test(normalizedRatio, "0", "0.0000025", n, d, scale.toFixed());
            }
        }
    }

    for (const scale of [Decimal("1e6"), Decimal("1e18"), Decimal("1e30"), MAX_UINT128]) {
        for (let i = Decimal(1); i.lte(scale); i = i.mul(10)) {
            const n = MAX_UINT256.divToInt(scale).mul(i).add(1);
            for (let j = Decimal(1); j.lte(scale); j = j.mul(10)) {
                const d = MAX_UINT256.divToInt(scale).mul(j).add(1);
                test(normalizedRatio, "0", "0.135", n.toFixed(), d.toFixed(), scale.toFixed());
            }
        }
    }

    for (let scale = 1; scale <= 4; scale++) {
        for (const n of [
            MAX_UINT256.div(3).floor(),
            MAX_UINT256.div(3).ceil(),
            MAX_UINT256.div(2).floor(),
            MAX_UINT256.div(2).ceil(),
            MAX_UINT256.mul(2).div(3).floor(),
            MAX_UINT256.mul(2).div(3).ceil(),
            MAX_UINT256.mul(3).div(4).floor(),
            MAX_UINT256.mul(3).div(4).ceil(),
            MAX_UINT256.sub(1),
            MAX_UINT256
        ]) {
            for (const d of [MAX_UINT256.sub(1), MAX_UINT256]) {
                test(normalizedRatio, "1.6", "0", n.toFixed(), d.toFixed(), scale);
            }
        }
    }

    function test(method, maxAbsoluteError, maxRelativeError, ...args) {
        it(`${method.name}(${args.join(", ")})`, async () => {
            const expected = method(...args.map(x => Decimal(x)));
            const actual = await fractionMath[method.name](...args);
            const x = Decimal(actual[0].toString()).mul(expected[1]);
            const y = Decimal(actual[1].toString()).mul(expected[0]);
            if (!x.eq(y)) {
                const absoluteError = x.sub(y).abs();
                const relativeError = x.div(y).sub(1).abs();
                const ok = absoluteError.lte(maxAbsoluteError) || relativeError.lte(maxRelativeError);
                assert(ok, `\nabsoluteError = ${absoluteError.toFixed()}\nrelativeError = ${relativeError.toFixed()}`);
            }
        });
    }
});
