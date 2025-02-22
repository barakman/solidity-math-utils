const TestContract = artifacts.require("IntegralMathUser");
const Utilities = require("./helpers/Utilities.js");
const Decimal = require("decimal.js");

const pow2 = k => Decimal(2).pow(k);
const pow3 = k => Decimal(3).pow(k);

const MAX_UINT256 = pow2(256).sub(1);

const floorLog2 = (n)          => n.log(2).floor();
const floorSqrt = (n)          => n.sqrt().floor();
const ceilSqrt  = (n)          => n.sqrt().ceil();
const floorCbrt = (n)          => n.cbrt().floor();
const ceilCbrt  = (n)          => n.cbrt().ceil();
const roundDiv  = (n, d)       => n.div(d).add(0.5).floor();
const mulShrF   = (x, y, s)    => x.mul(y).div(pow2(s)).floor();
const mulShrC   = (x, y, s)    => x.mul(y).div(pow2(s)).ceil();
const mulDivF   = (x, y, z)    => x.mul(y).div(z).floor();
const mulDivC   = (x, y, z)    => x.mul(y).div(z).ceil();
const mulDivR   = (x, y, z)    => x.mul(y).div(z).add(0.5).floor();
const mulDivExF = (x, y, z, w) => x.mul(y).div(z.mul(w)).floor();
const mulDivExC = (x, y, z, w) => x.mul(y).div(z.mul(w)).ceil();
const minFactor = (x, y)       => Decimal.max(mulDivC(x, y, MAX_UINT256), 1);

describe(TestContract.contractName, () => {
    let testContract;

    before(async () => {
        testContract = await TestContract.new();
    });

    for (const method of [floorSqrt, ceilSqrt, floorCbrt, ceilCbrt]) {
        test(method, 0);
    }

    for (const method of [floorSqrt, ceilSqrt, floorCbrt, ceilCbrt, floorLog2]) {
        for (let i = 0; i < 400; i++) {
            for (const j of [i + 1, MAX_UINT256.sub(i).toHex()]) {
                test(method, j);
            }
        }
    }

    for (const method of [floorSqrt, ceilSqrt, floorCbrt, ceilCbrt, floorLog2]) {
        for (let i = 9; i <= 255; i++) {
            for (let j = -3; j <= 3; j++) {
                test(method, pow2(i).add(j).toHex());
            }
        }
    }

    for (const method of [floorSqrt, ceilSqrt, floorCbrt, ceilCbrt, floorLog2]) {
        for (let i = 6; i <= 85; i++) {
            for (let j = -3; j <= 3; j++) {
                test(method, pow3(i).add(j).toHex());
            }
        }
    }

    for (let i = 0; i < 10; i++) {
        const x = MAX_UINT256.sub(i).toHex();
        for (let j = 1; j <= 10; j++) {
            const y = MAX_UINT256.sub(j - 1).toHex();
            for (const [n, d] of [[i, j], [x, j], [i, y], [x, y]]) {
                test(roundDiv, n, d);
            }
        }
    }

    for (const px of [0, 64, 128, 192, 255, 256]) {
        for (const py of [0, 64, 128, 192, 255, 256]) {
            for (const ax of px < 256 ? [-1, 0, +1] : [-1]) {
                for (const ay of py < 256 ? [-1, 0, +1] : [-1]) {
                    const x = pow2(px).add(ax).toHex();
                    const y = pow2(py).add(ay).toHex();
                    test(minFactor, x, y);
                }
            }
        }
    }

    for (const px of [64, 128, 192, 256]) {
        for (const py of [64, 128, 192, 256]) {
            for (const ax of [pow2(px >> 1), 1]) {
                for (const ay of [pow2(py >> 1), 1]) {
                    const x = pow2(px).sub(ax).toHex();
                    const y = pow2(py).sub(ay).toHex();
                    test(minFactor, x, y);
                }
            }
        }
    }

    for (const px of [128, 192, 256]) {
        for (const py of [128, 192, 256]) {
            for (const ax of [3, 5, 7]) {
                for (const ay of [3, 5, 7]) {
                    const x = pow2(px).divToInt(ax).toHex();
                    const y = pow2(py).divToInt(ay).toHex();
                    test(minFactor, x, y);
                }
            }
        }
    }

    for (const method of [mulShrF, mulShrC]) {
        for (const px of [0, 64, 128, 192, 255, 256]) {
            for (const py of [0, 64, 128, 192, 255, 256]) {
                for (const ax of px < 256 ? [-1, 0, +1] : [-1]) {
                    for (const ay of py < 256 ? [-1, 0, +1] : [-1]) {
                        for (const s of [0, 1, 64, 127, 128, 191, 254, 255]) {
                            const x = pow2(px).add(ax).toHex();
                            const y = pow2(py).add(ay).toHex();
                            test(method, x, y, s);
                        }
                    }
                }
            }
        }
    }

    for (const method of [mulShrF, mulShrC]) {
        for (const px of [64, 128, 192, 256]) {
            for (const py of [64, 128, 192, 256]) {
                for (const ax of [pow2(px >> 1), 1]) {
                    for (const ay of [pow2(py >> 1), 1]) {
                        for (const s of [0, 1, 64, 127, 128, 191, 254, 255]) {
                            const x = pow2(px).sub(ax).toHex();
                            const y = pow2(py).sub(ay).toHex();
                            test(method, x, y, s);
                        }
                    }
                }
            }
        }
    }

    for (const method of [mulShrF, mulShrC]) {
        for (const px of [128, 192, 256]) {
            for (const py of [128, 192, 256]) {
                for (const ax of [3, 5, 7]) {
                    for (const ay of [3, 5, 7]) {
                        for (const s of [0, 1, 64, 127, 128, 191, 254, 255]) {
                            const x = pow2(px).divToInt(ax).toHex();
                            const y = pow2(py).divToInt(ay).toHex();
                            test(method, x, y, s);
                        }
                    }
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
                                const x = pow2(px).add(ax).toHex();
                                const y = pow2(py).add(ay).toHex();
                                const z = pow2(pz).add(az).toHex();
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
                    for (const ax of [pow2(px >> 1), 1]) {
                        for (const ay of [pow2(py >> 1), 1]) {
                            for (const az of [pow2(pz >> 1), 1]) {
                                const x = pow2(px).sub(ax).toHex();
                                const y = pow2(py).sub(ay).toHex();
                                const z = pow2(pz).sub(az).toHex();
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
                                const x = pow2(px).divToInt(ax).toHex();
                                const y = pow2(py).divToInt(ay).toHex();
                                const z = pow2(pz).divToInt(az).toHex();
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
                        const z = pow2(pz).add(az).toHex();
                        const w = pow2(pw).add(aw).toHex();
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
                    const w = pow2(pw).add(aw).toHex();
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
