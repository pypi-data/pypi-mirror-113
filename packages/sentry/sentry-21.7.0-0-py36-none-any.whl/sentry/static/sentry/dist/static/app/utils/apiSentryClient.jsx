Object.defineProperty(exports, "__esModule", { value: true });
exports.run = exports.init = void 0;
var tslib_1 = require("tslib");
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var hub;
function init(dsn) {
    // This client is used to track all API requests that use `app/api`
    // This is a bit noisy so we don't want it in the main project (yet)
    var client = new Sentry.BrowserClient({
        dsn: dsn,
    });
    hub = new Sentry.Hub(client);
}
exports.init = init;
var run = function (cb) {
    if (!hub) {
        return;
    }
    hub.run(cb);
};
exports.run = run;
//# sourceMappingURL=apiSentryClient.jsx.map