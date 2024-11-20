const TestContract = artifacts.require("BondingCurveUser");
const Decimal = require("decimal.js");

const ONE        = Decimal(1);
const MAX_WEIGHT = Decimal(1000000);

const lte = max => arg => Decimal(arg).lte(max);

const buy      = (supply, balance, weight, amount)              => supply.mul((ONE.add(amount.div(balance))).pow(weight.div(MAX_WEIGHT)).sub(ONE));
const sell     = (supply, balance, weight, amount)              => balance.mul(ONE.sub(ONE.sub(amount.div(supply)).pow((MAX_WEIGHT.div(weight)))));
const convert  = (balance1, weight1, balance2, weight2, amount) => balance2.mul(ONE.sub(balance1.div(balance1.add(amount)).pow(weight1.div(weight2))));
const deposit  = (supply, balance, weights, amount)             => supply.mul(amount.div(balance).add(ONE).pow(weights.div(MAX_WEIGHT)).sub(ONE));
const withdraw = (supply, balance, weights, amount)             => balance.mul(ONE.sub(supply.sub(amount).div(supply).pow(MAX_WEIGHT.div(weights))));
const invest   = (supply, balance, weights, amount)             => balance.mul(supply.add(amount).div(supply).pow(MAX_WEIGHT.div(weights)).sub(ONE));

describe(TestContract.contractName, () => {
    let testContract;

    before(async () => {
        testContract = await TestContract.new();
    });

    for (const supply of [1, 2, 3, 4].map(n => `${n}`.repeat(21 + n)))
        for (const balance of [1, 2, 3, 4].map(n => `${n}`.repeat(21 + n)))
            for (const weight of [10, 20, 90, 100].map(p => `${p * 10000}`))
                for (const amount of [1, 2, 3, 4].map(n => `${n}`.repeat(18 + n)))
                    test(buy, "0.000000000000015", supply, balance, weight, amount);

    for (const supply of [1, 2, 3, 4].map(n => `${n}`.repeat(21 + n)))
        for (const balance of [1, 2, 3, 4].map(n => `${n}`.repeat(21 + n)))
            for (const weight of [10, 20, 90, 100].map(p => `${p * 10000}`))
                for (const amount of [1, 2, 3, 4].map(n => `${n}`.repeat(18 + n)).filter(lte(supply)))
                    test(sell, "0.000000000000003", supply, balance, weight, amount);

    for (const balance1 of [1, 2, 3, 4].map(n => `${n}`.repeat(21 + n)))
        for (const weight1 of [10, 20, 50, 100].map(p => `${p * 10000}`))
            for (const balance2 of [1, 2, 3, 4].map(n => `${n}`.repeat(21 + n)))
                for (const weight2 of [10, 20, 50, 100].map(p => `${p * 10000}`))
                    for (const amount of [1, 2, 3, 4].map(n => `${n}`.repeat(18 + n)))
                        test(convert, "0.000000000000014", balance1, weight1, balance2, weight2, amount);

    for (const supply of [1, 2, 3, 4].map(n => `${n}`.repeat(21 + n)))
        for (const balance of [1, 2, 3, 4].map(n => `${n}`.repeat(21 + n)))
            for (const weights of [10, 50, 100, 200].map(p => `${p * 10000}`))
                for (const amount of [1, 2, 3, 4].map(n => `${n}`.repeat(18 + n)))
                    test(deposit, "0.000000000000010", supply, balance, weights, amount);

    for (const supply of [1, 2, 3, 4].map(n => `${n}`.repeat(21 + n)))
        for (const balance of [1, 2, 3, 4].map(n => `${n}`.repeat(21 + n)))
            for (const weights of [10, 50, 100, 200].map(p => `${p * 10000}`))
                for (const amount of [1, 2, 3, 4].map(n => `${n}`.repeat(18 + n)).filter(lte(supply)))
                    test(withdraw, "0.000000000000004", supply, balance, weights, amount);

    for (const supply of [1, 2, 3, 4].map(n => `${n}`.repeat(21 + n)))
        for (const balance of [1, 2, 3, 4].map(n => `${n}`.repeat(21 + n)))
            for (const weights of [10, 50, 100, 200].map(p => `${p * 10000}`))
                for (const amount of [1, 2, 3, 4].map(n => `${n}`.repeat(18 + n)))
                    test(invest, "0.000000000000005", supply, balance, weights, amount);

    function test(method, maxError, ...args) {
        it(`${method.name}(${args.join(", ")})`, async () => {
            const expected = method(...args.map(x => Decimal(x)));
            const actual = Decimal((await testContract[method.name](...args)).toString());
            if (!actual.eq(expected)) {
                const error = actual.div(expected).sub(1).abs();
                assert(error.lte(maxError), `error = ${error.toFixed()}`);
            }
        });
    }
});
