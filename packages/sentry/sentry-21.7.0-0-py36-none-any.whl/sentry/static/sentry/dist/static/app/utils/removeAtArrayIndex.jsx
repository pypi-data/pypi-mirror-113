Object.defineProperty(exports, "__esModule", { value: true });
exports.removeAtArrayIndex = void 0;
var tslib_1 = require("tslib");
/**
 * Remove item at `index` in `array` without mutating `array`
 */
function removeAtArrayIndex(array, index) {
    var newArray = tslib_1.__spreadArray([], tslib_1.__read(array));
    newArray.splice(index, 1);
    return newArray;
}
exports.removeAtArrayIndex = removeAtArrayIndex;
//# sourceMappingURL=removeAtArrayIndex.jsx.map