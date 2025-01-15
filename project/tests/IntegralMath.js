const TestContract = artifacts.require("IntegralMathUser");
const Utilities = require("./helpers/Utilities.js");
const Decimal = require("decimal.js");

const two_pow = k => Decimal(2).pow(k);

const MAX_UINT256 = two_pow(256).sub(1);

const floorLog2 = (n)          => n.log(2).floor();
const floorSqrt = (n)          => n.sqrt().floor();
const ceilSqrt  = (n)          => n.sqrt().ceil();
const floorCbrt = (n)          => n.cbrt().floor();
const ceilCbrt  = (n)          => n.cbrt().ceil();
const roundDiv  = (n, d)       => n.div(d).add(0.5).floor();
const mulShr    = (x, y, s)    => x.mul(y).div(two_pow(s)).floor();
const mulDivF   = (x, y, z)    => x.mul(y).div(z).floor();
const mulDivC   = (x, y, z)    => x.mul(y).div(z).ceil();
const mulDivR   = (x, y, z)    => x.mul(y).div(z).add(0.5).floor();
const mulDivExF = (x, y, z, w) => x.mul(y).div(z.mul(w)).floor();
const mulDivExC = (x, y, z, w) => x.mul(y).div(z.mul(w)).ceil();
const minFactor = (x, y)       => Decimal.max(mulDivC(x, y, MAX_UINT256), 1);

describe.only(TestContract.contractName, () => {
    let testContract;

    before(async () => {
        testContract = await TestContract.new();
    });

    test(floorSqrt, 0);
    test(ceilSqrt , 0);
    test(floorCbrt, 0);
    test(ceilCbrt , 0);

    for (let n = 0; n < 400; n++) {
        for (const x of [n + 1, MAX_UINT256.sub(n).toHex()]) {
            test(floorLog2, x);
            test(floorSqrt, x);
            test(ceilSqrt , x);
            test(floorCbrt, x);
            test(ceilCbrt , x);
        }
    }

    for (let n = 9; n <= 255; n++) {
        for (let k = -3; k <= 3; k++) {
            const x = two_pow(n).add(k).toHex();
            test(floorLog2, x);
            test(floorSqrt, x);
            test(ceilSqrt , x);
            test(floorCbrt, x);
            test(ceilCbrt , x);
        }
    }

    for (let n = 6; n <= 85; n++) {
        for (let k = -3; k <= 3; k++) {
            const x = Decimal(3).pow(n).add(k).toHex();
            test(floorSqrt, x);
            test(ceilSqrt , x);
            test(floorCbrt, x);
            test(ceilCbrt , x);
        }
    }

    for (let i = 0; i < 10; i++) {
        const x = two_pow(256).sub(i + 1).toHex();
        for (let j = 1; j <= 10; j++) {
            const y = two_pow(256).sub(j).toHex();
            for (const [n, d] of [[i, j], [x, j], [i, y], [x, y]]) {
                test(roundDiv, n, d);
            }
        }
    }

    for (const px of [0, 64, 128, 192, 255, 256]) {
        for (const py of [0, 64, 128, 192, 255, 256]) {
            for (const ax of px < 256 ? [-1, 0, +1] : [-1]) {
                for (const ay of py < 256 ? [-1, 0, +1] : [-1]) {
                    for (const s of [0, 1, 64, 127, 128, 191, 254, 255]) {
                        const x = two_pow(px).add(ax).toHex();
                        const y = two_pow(py).add(ay).toHex();
                        test(method, x, y, s);
                    }
                }
            }
        }
    }

    for (const px of [64, 128, 192, 256]) {
        for (const py of [64, 128, 192, 256]) {
            for (const ax of [two_pow(px >> 1), 1]) {
                for (const ay of [two_pow(py >> 1), 1]) {
                    for (const s of [0, 1, 64, 127, 128, 191, 254, 255]) {
                        const x = two_pow(px).sub(ax).toHex();
                        const y = two_pow(py).sub(ay).toHex();
                        test(method, x, y, s);
                    }
                }
            }
        }
    }

    for (const px of [128, 192, 256]) {
        for (const py of [128, 192, 256]) {
            for (const ax of [3, 5, 7]) {
                for (const ay of [3, 5, 7]) {
                    for (const s of [0, 1, 64, 127, 128, 191, 254, 255]) {
                        const x = two_pow(px).divToInt(ax).toHex();
                        const y = two_pow(py).divToInt(ay).toHex();
                        test(method, x, y, s);
                    }
                }
            }
        }
    }

    for (const px of [0, 64, 128, 192, 255, 256]) {
        for (const py of [0, 64, 128, 192, 255, 256]) {
            for (const ax of px < 256 ? [-1, 0, +1] : [-1]) {
                for (const ay of py < 256 ? [-1, 0, +1] : [-1]) {
                    const x = two_pow(px).add(ax).toHex();
                    const y = two_pow(py).add(ay).toHex();
                    test(minFactor, x, y);
                }
            }
        }
    }

    for (const px of [64, 128, 192, 256]) {
        for (const py of [64, 128, 192, 256]) {
            for (const ax of [two_pow(px >> 1), 1]) {
                for (const ay of [two_pow(py >> 1), 1]) {
                    const x = two_pow(px).sub(ax).toHex();
                    const y = two_pow(py).sub(ay).toHex();
                    test(minFactor, x, y);
                }
            }
        }
    }

    for (const method of [mulDivF, mulDivC, mulDivR, mulDivExF, mulDivExC]) {
        for (const px of [0, 64, 128, 192, 255, 256]) {
            for (const py of [0, 64, 128, 192, 255, 256]) {
                for (const pz of [1, 64, 128, 192, 255, 256]) {
                    for (const ax of px < 256 ? [-1, 0, +1] : [-1]) {
                        for (const ay of py < 256 ? [-1, 0, +1] : [-1]) {
                            for (const az of pz < 256 ? [-1, 0, +1] : [-1]) {
                                const x = two_pow(px).add(ax).toHex();
                                const y = two_pow(py).add(ay).toHex();
                                const z = two_pow(pz).add(az).toHex();
                                test(method, ...[x, y, z, MAX_UINT256.toHex()].slice(0, method.length));
                            }
                        }
                    }
                }
            }
        }
    }

    for (const method of [mulDivF, mulDivC, mulDivR, mulDivExF, mulDivExC]) {
        for (const px of [64, 128, 192, 256]) {
            for (const py of [64, 128, 192, 256]) {
                for (const pz of [64, 128, 192, 256]) {
                    for (const ax of [two_pow(px >> 1), 1]) {
                        for (const ay of [two_pow(py >> 1), 1]) {
                            for (const az of [two_pow(pz >> 1), 1]) {
                                const x = two_pow(px).sub(ax).toHex();
                                const y = two_pow(py).sub(ay).toHex();
                                const z = two_pow(pz).sub(az).toHex();
                                test(method, ...[x, y, z, MAX_UINT256.toHex()].slice(0, method.length));
                            }
                        }
                    }
                }
            }
        }
    }

    for (const method of [mulDivF, mulDivC, mulDivR, mulDivExF, mulDivExC]) {
        for (const px of [128, 192, 256]) {
            for (const py of [128, 192, 256]) {
                for (const pz of [128, 192, 256]) {
                    for (const ax of [3, 5, 7]) {
                        for (const ay of [3, 5, 7]) {
                            for (const az of [3, 5, 7]) {
                                const x = two_pow(px).divToInt(ax).toHex();
                                const y = two_pow(py).divToInt(ay).toHex();
                                const z = two_pow(pz).divToInt(az).toHex();
                                test(method, ...[x, y, z, MAX_UINT256.toHex()].slice(0, method.length));
                            }
                        }
                    }
                }
            }
        }
    }

    for (const method of [mulDivExF, mulDivExC]) {
        for (const pz of [128, 129, 130]) {
            for (const pw of [128, 129, 130]) {
                for (const az of [0, 1, 2]) {
                    for (const aw of [0, 1, 2]) {
                        const z = two_pow(pz).add(az).toHex();
                        const w = two_pow(pw).add(aw).toHex();
                        test(method, MAX_UINT256.toHex(), MAX_UINT256.toHex(), z, w);
                    }
                }
            }
        }
    }

    for (const method of [mulDivExF, mulDivExC]) {
        for (const d of [1, 7, 11, 17, 23]) {
            for (let pw = 1; pw <= 256 - d; pw++) {
                for (const aw of [-1, 0, +1]) {
                    const n = MAX_UINT256.divToInt(d).toHex();
                    const w = two_pow(pw).add(aw).toHex();
                    test(method, n, n, n, w);
                }
            }
        }
    }

    function test(method, ...args) {
        it(`${method.name}(${args.join(", ")})`, async () => {
            const expected = method(...args.map(x => Decimal(x)));
            if (expected.lte(MAX_UINT256)) {
                const actual = await testContract[method.name](...args);
                assert.equal(actual.toString(), expected.toFixed());
            }
            else {
                await Utilities.assertRevert(testContract[method.name](...args));
            }
        });
    }
});
