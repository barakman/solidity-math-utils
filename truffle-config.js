const Decimal = require("decimal.js");

Decimal.set({precision: 100, rounding: Decimal.ROUND_DOWN});

module.exports = {
    contracts_directory: "./project",
    contracts_build_directory: "./project/artifacts",
    test_directory: "./project/tests",
    networks: {
        production: {
            host: "127.0.0.1",
            port: 8545,
            network_id: "*",
            gasPrice: 20000000000,
            gas: 6721975
        }
    },
    mocha: {
        useColors: true,
        enableTimeouts: false,
        reporter: "list" // See <https://mochajs.org/#reporters>
    },
    compilers: {
        solc: {
            version: "0.8.4",
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
