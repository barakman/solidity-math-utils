require("@nomiclabs/hardhat-truffle5");
require("solidity-coverage");

const Decimal = require("decimal.js");

Decimal.set({precision: 155, rounding: Decimal.ROUND_DOWN});

module.exports = {
    solidity: {
        version: "0.8.28",
        settings: {
            optimizer: {
                enabled: true,
                runs: 20000
            }
        }
    },
    paths: {
        sources: "./project/contracts",
        tests: "./project/tests",
        cache: "./project/cache",
        artifacts: "./project/artifacts"
    },
    mocha: {
        timeout: 0,
        useColors: true,
        reporter: "list" // https://mochajs.org/#reporters
    }
};
