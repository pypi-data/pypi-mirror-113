Object.defineProperty(exports, "__esModule", { value: true });
exports.isEqualWithDates = void 0;
var tslib_1 = require("tslib");
var isDate_1 = tslib_1.__importDefault(require("lodash/isDate"));
var isEqualWith_1 = tslib_1.__importDefault(require("lodash/isEqualWith"));
// `lodash.isEqual` does not compare date objects
function dateComparator(value, other) {
    if (isDate_1.default(value) && isDate_1.default(other)) {
        return +value === +other;
    }
    // Loose checking
    if (!value && !other) {
        return true;
    }
    // returning undefined will use default comparator
    return undefined;
}
var isEqualWithDates = function (a, b) { return isEqualWith_1.default(a, b, dateComparator); };
exports.isEqualWithDates = isEqualWithDates;
//# sourceMappingURL=isEqualWithDates.jsx.map