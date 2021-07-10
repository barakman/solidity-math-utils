const Decimal = require("decimal.js");

Decimal.set({precision: 155, rounding: Decimal.ROUND_DOWN});

module.exports = {
    contracts_directory: "./project",
    contracts_build_directory: "./project/artifacts",
    test_directory: "./project/tests",
    mocha: {
        useColors: true,
        enableTimeouts: false,
        reporter: "list" // See <https://mochajs.org/#reporters>
    },
    compilers: {
        solc: {
            version: "0.8.6",
            settings: {
                optimizer: {
                    enabled: true,
                    runs: 20000
                }
            }
        }
    },
    plugins: [
        "solidity-coverage"
    ]
};
