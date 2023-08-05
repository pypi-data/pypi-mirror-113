Object.defineProperty(exports, "__esModule", { value: true });
exports.callIfFunction = void 0;
var tslib_1 = require("tslib");
// Checks if `fn` is a function and calls it with `args`
function callIfFunction(fn) {
    var args = [];
    for (var _i = 1; _i < arguments.length; _i++) {
        args[_i - 1] = arguments[_i];
    }
    return typeof fn === 'function' && fn.apply(void 0, tslib_1.__spreadArray([], tslib_1.__read(args)));
}
exports.callIfFunction = callIfFunction;
//# sourceMappingURL=callIfFunction.jsx.map