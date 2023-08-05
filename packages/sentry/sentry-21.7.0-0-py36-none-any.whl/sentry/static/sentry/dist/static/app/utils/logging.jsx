Object.defineProperty(exports, "__esModule", { value: true });
exports.logException = void 0;
var tslib_1 = require("tslib");
var Sentry = tslib_1.__importStar(require("@sentry/react"));
function logException(ex, context) {
    Sentry.withScope(function (scope) {
        if (context) {
            scope.setExtra('context', context);
        }
        Sentry.captureException(ex);
    });
    /* eslint no-console:0 */
    window.console && console.error && console.error(ex);
}
exports.logException = logException;
//# sourceMappingURL=logging.jsx.map