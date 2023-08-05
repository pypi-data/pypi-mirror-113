Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var requestError_1 = tslib_1.__importDefault(require("./requestError"));
var ERROR_MAP = {
    0: 'CancelledError',
    400: 'BadRequestError',
    401: 'UnauthorizedError',
    403: 'ForbiddenError',
    404: 'NotFoundError',
    426: 'UpgradeRequiredError',
    429: 'TooManyRequestsError',
    500: 'InternalServerError',
    501: 'NotImplementedError',
    502: 'BadGatewayError',
    503: 'ServiceUnavailableError',
    504: 'GatewayTimeoutError',
};
/**
 * Create a RequestError whose name is equal to HTTP status text defined above
 *
 * @param {Object} resp A XHR response object
 * @param {String} stack The stack trace to use. Helpful for async calls and we want to preserve a different stack.
 */
function createRequestError(resp, stack, method, path) {
    var err = new requestError_1.default(method, path);
    if (resp) {
        var errorName = ERROR_MAP[resp.status];
        if (errorName) {
            err.setName(errorName);
        }
        err.setResponse(resp);
    }
    if (stack) {
        err.setStack(stack);
    }
    return err;
}
exports.default = createRequestError;
//# sourceMappingURL=createRequestError.jsx.map