Object.defineProperty(exports, "__esModule", { value: true });
exports.getPreloadedDataPromise = void 0;
var tslib_1 = require("tslib");
function getPreloadedDataPromise(name, slug, fallback, isInitialFetch) {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var data, result, _1;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    _a.trys.push([0, 7, , 8]);
                    data = window.__sentry_preload;
                    if (!(!isInitialFetch ||
                        !data ||
                        !data.orgSlug ||
                        data.orgSlug.toLowerCase() !== slug.toLowerCase() ||
                        !data[name] ||
                        !data[name].then)) return [3 /*break*/, 2];
                    return [4 /*yield*/, fallback()];
                case 1: return [2 /*return*/, _a.sent()];
                case 2: return [4 /*yield*/, data[name].catch(fallback)];
                case 3:
                    result = _a.sent();
                    if (!!result) return [3 /*break*/, 5];
                    return [4 /*yield*/, fallback()];
                case 4: return [2 /*return*/, _a.sent()];
                case 5: return [4 /*yield*/, result];
                case 6: return [2 /*return*/, _a.sent()];
                case 7:
                    _1 = _a.sent();
                    return [3 /*break*/, 8];
                case 8: return [4 /*yield*/, fallback()];
                case 9: return [2 /*return*/, _a.sent()];
            }
        });
    });
}
exports.getPreloadedDataPromise = getPreloadedDataPromise;
//# sourceMappingURL=getPreloadedData.js.map