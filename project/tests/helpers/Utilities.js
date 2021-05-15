module.exports.assertRevert = async function (promise, suffix) {
    try {
        await promise;
        throw null;
    }
    catch (error) {
        const message = suffix.length > 0 ? " " + suffix : "";
        assert(error, "Expected an error but did not get one");
        const errorMessage = `Returned error: VM Exception while processing transaction: revert${message}`;
        assert(error.message == errorMessage, `Expected '${errorMessage}' but got '${error.message}' instead`);
    }
};
