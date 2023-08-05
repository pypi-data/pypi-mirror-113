Object.defineProperty(exports, "__esModule", { value: true });
exports.fetchSentryAppComponents = void 0;
var tslib_1 = require("tslib");
var sentryAppComponentActions_1 = tslib_1.__importDefault(require("app/actions/sentryAppComponentActions"));
function fetchSentryAppComponents(api, orgSlug, projectId) {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var componentsUri, res;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    componentsUri = "/organizations/" + orgSlug + "/sentry-app-components/?projectId=" + projectId;
                    return [4 /*yield*/, api.requestPromise(componentsUri)];
                case 1:
                    res = _a.sent();
                    sentryAppComponentActions_1.default.loadComponents(res);
                    return [2 /*return*/, res];
            }
        });
    });
}
exports.fetchSentryAppComponents = fetchSentryAppComponents;
//# sourceMappingURL=sentryAppComponents.jsx.map