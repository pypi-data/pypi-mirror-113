Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var Sentry = tslib_1.__importStar(require("@sentry/react"));
function handleXhrErrorResponse(message) {
    return function (resp) {
        if (!resp) {
            return;
        }
        if (!resp.responseJSON) {
            return;
        }
        var responseJSON = resp.responseJSON;
        // If this is a string then just capture it as error
        if (typeof responseJSON.detail === 'string') {
            Sentry.withScope(function (scope) {
                scope.setExtra('status', resp.status);
                scope.setExtra('detail', responseJSON.detail);
                Sentry.captureException(new Error(message));
            });
            return;
        }
        // Ignore sudo-required errors
        if (responseJSON.detail && responseJSON.detail.code === 'sudo-required') {
            return;
        }
        if (responseJSON.detail && typeof responseJSON.detail.message === 'string') {
            Sentry.withScope(function (scope) {
                scope.setExtra('status', resp.status);
                scope.setExtra('detail', responseJSON.detail);
                scope.setExtra('code', responseJSON.detail.code);
                Sentry.captureException(new Error(message));
            });
            return;
        }
    };
}
exports.default = handleXhrErrorResponse;
//# sourceMappingURL=handleXhrErrorResponse.jsx.map