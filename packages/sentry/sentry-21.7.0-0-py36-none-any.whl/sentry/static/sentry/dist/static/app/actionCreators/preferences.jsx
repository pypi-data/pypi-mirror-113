Object.defineProperty(exports, "__esModule", { value: true });
exports.loadPreferencesState = exports.showSidebar = exports.hideSidebar = void 0;
var tslib_1 = require("tslib");
var js_cookie_1 = tslib_1.__importDefault(require("js-cookie"));
var preferencesActions_1 = tslib_1.__importDefault(require("../actions/preferencesActions"));
var SIDEBAR_COOKIE_KEY = 'sidebar_collapsed';
var COOKIE_ENABLED = '1';
var COOKIE_DISABLED = '0';
function hideSidebar() {
    preferencesActions_1.default.hideSidebar();
    js_cookie_1.default.set(SIDEBAR_COOKIE_KEY, COOKIE_ENABLED);
}
exports.hideSidebar = hideSidebar;
function showSidebar() {
    preferencesActions_1.default.showSidebar();
    js_cookie_1.default.set(SIDEBAR_COOKIE_KEY, COOKIE_DISABLED);
}
exports.showSidebar = showSidebar;
function loadPreferencesState() {
    // Set initial "collapsed" state to true or false
    preferencesActions_1.default.loadInitialState({
        collapsed: js_cookie_1.default.get(SIDEBAR_COOKIE_KEY) === COOKIE_ENABLED,
    });
}
exports.loadPreferencesState = loadPreferencesState;
//# sourceMappingURL=preferences.jsx.map