Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var getCookie_1 = tslib_1.__importDefault(require("app/utils/getCookie"));
function getCsrfToken() {
    var _a, _b;
    return (_b = getCookie_1.default((_a = window.csrfCookieName) !== null && _a !== void 0 ? _a : 'sc')) !== null && _b !== void 0 ? _b : '';
}
exports.default = getCsrfToken;
//# sourceMappingURL=getCsrfToken.jsx.map