var _this = this;
Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var sentryAppInstallationsStore_1 = tslib_1.__importDefault(require("app/stores/sentryAppInstallationsStore"));
var fetchSentryAppInstallations = function (api, orgSlug) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
    var installsUri, installs;
    return tslib_1.__generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                installsUri = "/organizations/" + orgSlug + "/sentry-app-installations/";
                return [4 /*yield*/, api.requestPromise(installsUri)];
            case 1:
                installs = _a.sent();
                sentryAppInstallationsStore_1.default.load(installs);
                return [2 /*return*/];
        }
    });
}); };
exports.default = fetchSentryAppInstallations;
//# sourceMappingURL=fetchSentryAppInstallations.jsx.map