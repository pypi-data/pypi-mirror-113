Object.defineProperty(exports, "__esModule", { value: true });
exports.loadSdkUpdates = void 0;
var tslib_1 = require("tslib");
var sdkUpdatesActions_1 = tslib_1.__importDefault(require("app/actions/sdkUpdatesActions"));
/**
 * Load SDK Updates for a specific organization
 */
function loadSdkUpdates(api, orgSlug) {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var updates;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, api.requestPromise("/organizations/" + orgSlug + "/sdk-updates/")];
                case 1:
                    updates = _a.sent();
                    sdkUpdatesActions_1.default.load(orgSlug, updates);
                    return [2 /*return*/];
            }
        });
    });
}
exports.loadSdkUpdates = loadSdkUpdates;
//# sourceMappingURL=sdkUpdates.jsx.map