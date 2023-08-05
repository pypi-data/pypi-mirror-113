Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var js_cookie_1 = tslib_1.__importDefault(require("js-cookie"));
var queryString = tslib_1.__importStar(require("query-string"));
function getPendingInvite() {
    var data = js_cookie_1.default.get('pending-invite');
    if (!data) {
        return null;
    }
    return queryString.parse(data);
}
exports.default = getPendingInvite;
//# sourceMappingURL=getPendingInvite.jsx.map