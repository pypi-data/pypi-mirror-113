Object.defineProperty(exports, "__esModule", { value: true });
exports.saveToStorage = exports.fetchFromStorage = void 0;
var tslib_1 = require("tslib");
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var localStorage_1 = tslib_1.__importDefault(require("app/utils/localStorage"));
var ADVANCED_DATA_SCRUBBING_LOCALSTORAGE_KEY = 'advanced-data-scrubbing';
// TODO(Priscila): add the method below in app/utils
function fetchFromStorage() {
    var storage = localStorage_1.default.getItem(ADVANCED_DATA_SCRUBBING_LOCALSTORAGE_KEY);
    if (!storage) {
        return undefined;
    }
    try {
        return JSON.parse(storage);
    }
    catch (err) {
        Sentry.withScope(function (scope) {
            scope.setExtra('storage', storage);
            Sentry.captureException(err);
        });
        return undefined;
    }
}
exports.fetchFromStorage = fetchFromStorage;
function saveToStorage(obj) {
    try {
        localStorage_1.default.setItem(ADVANCED_DATA_SCRUBBING_LOCALSTORAGE_KEY, JSON.stringify(obj));
    }
    catch (err) {
        Sentry.captureException(err);
        Sentry.withScope(function (scope) {
            scope.setExtra('storage', obj);
            Sentry.captureException(err);
        });
    }
}
exports.saveToStorage = saveToStorage;
//# sourceMappingURL=localStorage.jsx.map