Object.defineProperty(exports, "__esModule", { value: true });
exports.initializeApp = void 0;
var tslib_1 = require("tslib");
require("bootstrap/js/alert");
require("bootstrap/js/tab");
require("bootstrap/js/dropdown");
require("./exportGlobals");
var routes_1 = tslib_1.__importDefault(require("app/routes"));
var analytics_1 = require("app/utils/analytics");
var commonInitialization_1 = require("./commonInitialization");
var initializeSdk_1 = require("./initializeSdk");
var processInitQueue_1 = require("./processInitQueue");
var renderMain_1 = require("./renderMain");
var renderOnDomReady_1 = require("./renderOnDomReady");
function initializeApp(config) {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        return tslib_1.__generator(this, function (_a) {
            commonInitialization_1.commonInitialization(config);
            initializeSdk_1.initializeSdk(config, { routes: routes_1.default });
            // Used for operational metrics to determine that the application js
            // bundle was loaded by browser.
            analytics_1.metric.mark({ name: 'sentry-app-init' });
            renderOnDomReady_1.renderOnDomReady(renderMain_1.renderMain);
            processInitQueue_1.processInitQueue();
            return [2 /*return*/];
        });
    });
}
exports.initializeApp = initializeApp;
//# sourceMappingURL=initializeApp.jsx.map