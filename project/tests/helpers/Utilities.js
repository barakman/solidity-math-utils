module.exports.assertRevert = async function (promise, message) {
    try {
        await promise;
        throw null;
    }
    catch (error) {
        assert(error, "expected an error but did not get one");
        assert.include(error.message, "revert");
        if (message)
            assert.include(error.message, message);
    }
};
