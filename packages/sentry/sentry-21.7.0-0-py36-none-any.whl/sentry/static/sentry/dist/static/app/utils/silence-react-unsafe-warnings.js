Object.defineProperty(exports, "__esModule", { value: true });
exports.silencedWarn = exports.originalConsoleWarn = void 0;
var tslib_1 = require("tslib");
// eslint-disable-next-line no-console
exports.originalConsoleWarn = console.warn;
var REACT_UNSAFE_WARNING_REGEX = /componentWill.* has been renamed, and is not recommended for use.*/;
var MOMENT_INVALID_INPUT_REGEX = /moment construction falls back/;
window.console.warn = function (message) {
    var args = [];
    for (var _i = 1; _i < arguments.length; _i++) {
        args[_i - 1] = arguments[_i];
    }
    if (typeof message === 'string' &&
        (REACT_UNSAFE_WARNING_REGEX.test(message) || MOMENT_INVALID_INPUT_REGEX.test(message))) {
        return;
    }
    exports.originalConsoleWarn.apply(void 0, tslib_1.__spreadArray([message], tslib_1.__read(args)));
};
exports.silencedWarn = window.console.warn;
//# sourceMappingURL=silence-react-unsafe-warnings.js.map