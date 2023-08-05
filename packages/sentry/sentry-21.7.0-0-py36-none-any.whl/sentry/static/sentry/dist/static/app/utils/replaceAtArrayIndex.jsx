Object.defineProperty(exports, "__esModule", { value: true });
exports.replaceAtArrayIndex = void 0;
var tslib_1 = require("tslib");
/**
 * Replace item at `index` in `array` with `obj`
 */
function replaceAtArrayIndex(array, index, obj) {
    var newArray = tslib_1.__spreadArray([], tslib_1.__read(array));
    newArray.splice(index, 1, obj);
    return newArray;
}
exports.replaceAtArrayIndex = replaceAtArrayIndex;
//# sourceMappingURL=replaceAtArrayIndex.jsx.map