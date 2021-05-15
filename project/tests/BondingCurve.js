const BondingCurve = artifacts.require("BondingCurve");

const Decimal = require("decimal.js");

const ONE        = Decimal(1);
const MAX_WEIGHT = Decimal(1000000);

const buy      = (supply, balance, weight, amount) => supply.mul((ONE.add(amount.div(balance))).pow(weight.div(MAX_WEIGHT)).sub(ONE));
const sell     = (supply, balance, weight, amount) => balance.mul(ONE.sub(ONE.sub(amount.div(supply)).pow((MAX_WEIGHT.div(weight)))));
const convert  = (balance1, weight1, balance2, weight2, amount) => balance2.mul(ONE.sub(balance1.div(balance1.add(amount)).pow(weight1.div(weight2))));
const deposit  = (supply, balance, weights, amount) => supply.mul(amount.div(balance).add(ONE).pow(weights.div(MAX_WEIGHT)).sub(ONE));
const withdraw = (supply, balance, weights, amount) => balance.mul(ONE.sub(supply.sub(amount).div(supply).pow(MAX_WEIGHT.div(weights))));
const invest   = (supply, balance, weights, amount) => balance.mul(supply.add(amount).div(supply).pow(MAX_WEIGHT.div(weights)).sub(ONE));

contract("BondingCurve", () => {
    let bondingCurve;

    before(async () => {
        bondingCurve = await BondingCurve.new();
        await bondingCurve.init();
    });

    for (const supply of [1, 2, 3, 4].map(n => `${n}`.repeat(21 + n)))
        for (const balance of [1, 2, 3, 4].map(n => `${n}`.repeat(21 + n)))
            for (const weight of [10, 20, 90, 100].map(p => `${p * 10000}`))
                for (const amount of [1, 2, 3, 4].map(n => `${n}`.repeat(18 + n)))
                    test(buy, "0.0000000000001", supply, balance, weight, amount);

    for (const supply of [1, 2, 3, 4].map(n => `${n}`.repeat(21 + n)))
        for (const balance of [1, 2, 3, 4].map(n => `${n}`.repeat(21 + n)))
            for (const weight of [10, 20, 90, 100].map(p => `${p * 10000}`))
                for (const amount of [1, 2, 3, 4].map(n => `${n}`.repeat(18 + n)))
                    if (Decimal(amount).lte(supply))
                        test(sell, "0.00000000000001", supply, balance, weight, amount);

    for (const balance1 of [1, 2, 3, 4].map(n => `${n}`.repeat(21 + n)))
        for (const weight1 of [10, 20, 50, 100].map(p => `${p * 10000}`))
            for (const balance2 of [1, 2, 3, 4].map(n => `${n}`.repeat(21 + n)))
                for (const weight2 of [10, 20, 50, 100].map(p => `${p * 10000}`))
                    for (const amount of [1, 2, 3, 4].map(n => `${n}`.repeat(18 + n)))
                        test(convert, "0.00000000001", balance1, weight1, balance2, weight2, amount);

    for (const supply of [1, 2, 3, 4].map(n => `${n}`.repeat(21 + n)))
        for (const balance of [1, 2, 3, 4].map(n => `${n}`.repeat(21 + n)))
            for (const weights of [10, 50, 100, 200].map(p => `${p * 10000}`))
                for (const amount of [1, 2, 3, 4].map(n => `${n}`.repeat(18 + n)))
                    test(deposit, "0.00000000000001", supply, balance, weights, amount);

    for (const supply of [1, 2, 3, 4].map(n => `${n}`.repeat(21 + n)))
        for (const balance of [1, 2, 3, 4].map(n => `${n}`.repeat(21 + n)))
            for (const weights of [10, 50, 100, 200].map(p => `${p * 10000}`))
                for (const amount of [1, 2, 3, 4].map(n => `${n}`.repeat(18 + n)))
                    if (Decimal(amount).lte(supply))
                        test(withdraw, "0.00000000000001", supply, balance, weights, amount);

    for (const supply of [1, 2, 3, 4].map(n => `${n}`.repeat(21 + n)))
        for (const balance of [1, 2, 3, 4].map(n => `${n}`.repeat(21 + n)))
            for (const weights of [10, 50, 100, 200].map(p => `${p * 10000}`))
                for (const amount of [1, 2, 3, 4].map(n => `${n}`.repeat(18 + n)))
                    test(invest, "0.0001", supply, balance, weights, amount);

    function test(method, maxError, ...args) {
        it(`${method.name}(${args.join(", ")})`, async () => {
            const expected = method(...args.map(x => Decimal(x)));
            const actual = Decimal((await bondingCurve[method.name](...args)).toString());
            if (!actual.eq(expected)) {
                const error = actual.div(expected).sub(1).abs();
                assert(error.lte(maxError), `error = ${error.toFixed()}`);
            }
        });
    }
});
