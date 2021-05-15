const DynamicCurve = artifacts.require("DynamicCurve");

const Decimal = require("decimal.js");

function convert(t, s, r, q, p, w1, w2) {
    [t, s, r, q, p, w1, w2] = [t, s, r, q, p, w1, w2].map(x => Decimal(x));
    const x1 = t.sub(s);
    const x2 = r.mul(Decimal(1).sub(s.div(s.add(x1)).pow(w1.div(w2))));
    const y1 = s.add(x1).mul(q).div(w1);
    const y2 = r.sub(x2).mul(p).div(w2);
    return [y1, y2];
}

contract("DynamicCurve", () => {
    let dynamicCurve;

    before(async () => {
        dynamicCurve = await DynamicCurve.new();
        await dynamicCurve.init();
    });

    async function equalize(t, s, r, q, p) {
        try {
            return await dynamicCurve.equalize(t, s, r, q, p);
        }
        catch (error) {
            return null;
        }
    }

    for (const t of [1, 2, 3, 4, 5])
        for (const s of [1, 2, 3, 4, 5])
            for (const r of [1, 2, 3, 4, 5])
                for (const q of [1, 2, 3, 4, 5])
                    for (const p of [1, 2, 3, 4, 5])
                        test(t, s, r, q, p, "0.16235");

    for (const t of [1, 2, 3, 4, 5].map(n => `${n}`.repeat(21 + (n >> 1))))
        for (const s of [1, 2, 3, 4, 5].map(n => `${n}`.repeat(21 + (n >> 1))))
            for (const r of [1, 2, 3, 4, 5].map(n => `${n}`.repeat(21 + (n >> 1))))
                for (const q of [1, 2, 3, 4, 5].map(n => `${n}`.repeat(21 + (n >> 1))))
                    for (const p of [1, 2, 3, 4, 5].map(n => `${n}`.repeat(21 + (n >> 1))))
                        test(t, s, r, q, p, "0.16235");

    function test(t, s, r, q, p, maxError) {
        it(`equalize(${[t, s, r, q, p]})`, async () => {
            const weights = await equalize(t, s, r, q, p);
            if (weights) {
                const w = [0, 1].map(n => weights[n].toString());
                const equities = convert(t, s, r, q, p, w[0], w[1]);
                const error = equities[0].div(equities[1]).sub(1).abs();
                assert(error.lte(maxError), `error = ${error.toFixed()}`);
            }
        });
    }
});
