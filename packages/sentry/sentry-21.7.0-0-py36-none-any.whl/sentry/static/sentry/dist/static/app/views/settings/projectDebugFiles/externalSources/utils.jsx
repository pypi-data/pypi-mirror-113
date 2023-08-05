Object.defineProperty(exports, "__esModule", { value: true });
exports.expandKeys = void 0;
var tslib_1 = require("tslib");
var forEach_1 = tslib_1.__importDefault(require("lodash/forEach"));
var set_1 = tslib_1.__importDefault(require("lodash/set"));
function expandKeys(obj) {
    var result = {};
    forEach_1.default(obj, function (value, key) {
        set_1.default(result, key.split('.'), value);
    });
    return result;
}
exports.expandKeys = expandKeys;
//# sourceMappingURL=utils.jsx.map