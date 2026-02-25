const TestContract = artifacts.require("BondingCurveUser");
const Decimal = require("decimal.js");

const ONE = Decimal(1);

const lt = max => arg => Decimal(arg).lt(max);

const mintGain = (supply, balance, weightT, weightB, amount)    => supply.mul((ONE.add(amount.div(balance))).pow(weightT.div(weightB)).sub(ONE));
const mintCost = (supply, balance, weightT, weightB, amount)    => balance.mul((ONE.add(amount.div(supply))).pow(weightB.div(weightT)).sub(ONE));
const burnGain = (supply, balance, weightT, weightB, amount)    => balance.mul(ONE.sub(ONE.sub(amount.div(supply)).pow((weightB.div(weightT)))));
const burnCost = (supply, balance, weightT, weightB, amount)    => supply.mul(ONE.sub(ONE.sub(amount.div(balance)).pow((weightT.div(weightB)))));
const swapGain = (balance1, balance2, weight1, weight2, amount) => balance2.mul(ONE.sub(balance1.div(balance1.add(amount)).pow(weight1.div(weight2))));
const swapCost = (balance1, balance2, weight1, weight2, amount) => balance1.mul(balance2.div(balance2.sub(amount)).pow(weight2.div(weight1)).sub(ONE));


describe(TestContract.contractName, () => {
    let testContract;

    before(async () => {
        testContract = await TestContract.new();
    });

    for (const supply of [1, 2, 3, 4].map(n => `${n}`.repeat(21 + n))) {
        for (const balance of [1, 2, 3, 4].map(n => `${n}`.repeat(21 + n))) {
            for (const weightT of [10, 20, 90, 100].map(p => `${p * 10000}`)) {
                for (const weightB of [100, 133, 166, 200].map(p => `${p * 10000}`)) {
                    for (const amount of [0, 1, 2, 3, 4].map(n => `${n}`.repeat(18 + n))) {
                        test(mintGain, "0.0000000000000433", supply, balance, weightT, weightB, amount);
                    }
                }
            }
        }
    }

    for (const supply of [1, 2, 3, 4].map(n => `${n}`.repeat(21 + n))) {
        for (const balance of [1, 2, 3, 4].map(n => `${n}`.repeat(21 + n))) {
            for (const weightT of [10, 20, 90, 100].map(p => `${p * 10000}`)) {
                for (const weightB of [100, 133, 166, 200].map(p => `${p * 10000}`)) {
                    for (const amount of [0, 1, 2, 3, 4].map(n => `${n}`.repeat(18 + n))) {
                        test(mintCost, "0.0000000000000017", supply, balance, weightT, weightB, amount);
                    }
                }
            }
        }
    }

    for (const supply of [1, 2, 3, 4].map(n => `${n}`.repeat(21 + n))) {
        for (const balance of [1, 2, 3, 4].map(n => `${n}`.repeat(21 + n))) {
            for (const weightT of [10, 20, 90, 100].map(p => `${p * 10000}`)) {
                for (const weightB of [100, 133, 166, 200].map(p => `${p * 10000}`)) {
                    for (const amount of [0, 1, 2, 3, 4].map(n => `${n}`.repeat(18 + n)).filter(lt(supply)).concat(supply)) {
                        test(burnGain, "0.0000000000000028", supply, balance, weightT, weightB, amount);
                    }
                }
            }
        }
    }

    for (const supply of [1, 2, 3, 4].map(n => `${n}`.repeat(21 + n))) {
        for (const balance of [1, 2, 3, 4].map(n => `${n}`.repeat(21 + n))) {
            for (const weightT of [10, 20, 90, 100].map(p => `${p * 10000}`)) {
                for (const weightB of [100, 133, 166, 200].map(p => `${p * 10000}`)) {
                    for (const amount of [0, 1, 2, 3, 4].map(n => `${n}`.repeat(18 + n)).filter(lt(balance)).concat(balance)) {
                        test(burnCost, "0.0000000000000262", supply, balance, weightT, weightB, amount);
                    }
                }
            }
        }
    }

    for (const balance1 of [1, 2, 3, 4].map(n => `${n}`.repeat(21 + n))) {
        for (const balance2 of [1, 2, 3, 4].map(n => `${n}`.repeat(21 + n))) {
            for (const weight1 of [10, 20, 50, 100].map(p => `${p * 10000}`)) {
                for (const weight2 of [10, 20, 50, 100].map(p => `${p * 10000}`)) {
                    for (const amount of [0, 1, 2, 3, 4].map(n => `${n}`.repeat(18 + n))) {
                        test(swapGain, "0.0000000000000135", balance1, balance2, weight1, weight2, amount);
                    }
                }
            }
        }
    }

    for (const balance1 of [1, 2, 3, 4].map(n => `${n}`.repeat(21 + n))) {
        for (const balance2 of [1, 2, 3, 4].map(n => `${n}`.repeat(21 + n))) {
            for (const weight1 of [10, 20, 50, 100].map(p => `${p * 10000}`)) {
                for (const weight2 of [10, 20, 50, 100].map(p => `${p * 10000}`)) {
                    for (const amount of [0, 1, 2, 3, 4].map(n => `${n}`.repeat(18 + n)).filter(lt(balance2))) {
                        test(swapCost, "0.0000000000000106", balance1, balance2, weight1, weight2, amount);
                    }
                }
            }
        }
    }

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
