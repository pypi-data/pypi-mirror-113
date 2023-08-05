Object.defineProperty(exports, "__esModule", { value: true });
exports.commonInitialization = void 0;
var tslib_1 = require("tslib");
require("focus-visible");
var constants_1 = require("app/constants");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var matchMedia_1 = require("app/utils/matchMedia");
function commonInitialization(config) {
    if (constants_1.NODE_ENV === 'development') {
        Promise.resolve().then(function () { return tslib_1.__importStar(require(/* webpackMode: "eager" */ 'app/utils/silence-react-unsafe-warnings')); });
    }
    configStore_1.default.loadInitialData(config);
    // setup darkmode + favicon
    matchMedia_1.setupColorScheme();
}
exports.commonInitialization = commonInitialization;
//# sourceMappingURL=commonInitialization.jsx.map