module.exports.assertRevert = async function (promise, reason) {
    try {
        await promise;
        throw null;
    }
    catch (error) {
        assert(error, "expected an error but did not get one");
        assert.include(error.message, "revert");
        if (reason)
            assert.include(error.message, reason);
    }
};
