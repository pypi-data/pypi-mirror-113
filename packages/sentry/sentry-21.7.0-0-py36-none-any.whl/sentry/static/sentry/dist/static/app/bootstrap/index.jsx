Object.defineProperty(exports, "__esModule", { value: true });
exports.bootstrap = void 0;
var tslib_1 = require("tslib");
var BOOTSTRAP_URL = '/api/client-config/';
var bootApplication = function (data) {
    window.csrfCookieName = data.csrfCookieName;
    return data;
};
function bootWithHydration() {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var response, data;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, fetch(BOOTSTRAP_URL)];
                case 1:
                    response = _a.sent();
                    return [4 /*yield*/, response.json()];
                case 2:
                    data = _a.sent();
                    window.__initialData = data;
                    return [2 /*return*/, bootApplication(data)];
            }
        });
    });
}
function bootstrap() {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var bootstrapData;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    bootstrapData = window.__initialData;
                    if (!(bootstrapData === undefined)) return [3 /*break*/, 2];
                    return [4 /*yield*/, bootWithHydration()];
                case 1: return [2 /*return*/, _a.sent()];
                case 2: return [2 /*return*/, bootApplication(bootstrapData)];
            }
        });
    });
}
exports.bootstrap = bootstrap;
//# sourceMappingURL=index.jsx.map