Object.defineProperty(exports, "__esModule", { value: true });
exports.initializeMain = void 0;
var tslib_1 = require("tslib");
var initializeLocale_1 = require("./initializeLocale");
function initializeMain(config) {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var initializeApp;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0: 
                // This needs to be loaded as early as possible, or else the locale library can
                // throw an exception and prevent the application from being loaded.
                //
                // e.g. `app/constants` uses `t()` and is imported quite early
                return [4 /*yield*/, initializeLocale_1.initializeLocale(config)];
                case 1:
                    // This needs to be loaded as early as possible, or else the locale library can
                    // throw an exception and prevent the application from being loaded.
                    //
                    // e.g. `app/constants` uses `t()` and is imported quite early
                    _a.sent();
                    return [4 /*yield*/, Promise.resolve().then(function () { return tslib_1.__importStar(require('./initializeApp')); })];
                case 2:
                    initializeApp = (_a.sent()).initializeApp;
                    return [4 /*yield*/, initializeApp(config)];
                case 3:
                    _a.sent();
                    return [2 /*return*/];
            }
        });
    });
}
exports.initializeMain = initializeMain;
//# sourceMappingURL=initializeMain.jsx.map