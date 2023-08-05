var _this = this;
Object.defineProperty(exports, "__esModule", { value: true });
exports.recordInteraction = void 0;
var tslib_1 = require("tslib");
var api_1 = require("app/api");
var recordInteraction = function (sentryAppSlug, field, data) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
    var api, endpoint;
    return tslib_1.__generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                api = new api_1.Client();
                endpoint = "/sentry-apps/" + sentryAppSlug + "/interaction/";
                return [4 /*yield*/, api.requestPromise(endpoint, {
                        method: 'POST',
                        data: tslib_1.__assign({ tsdbField: field }, data),
                    })];
            case 1: return [2 /*return*/, _a.sent()];
        }
    });
}); };
exports.recordInteraction = recordInteraction;
//# sourceMappingURL=recordSentryAppInteraction.jsx.map