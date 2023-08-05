Object.defineProperty(exports, "__esModule", { value: true });
exports.ErrorType = void 0;
var tslib_1 = require("tslib");
var locale_1 = require("app/locale");
var ErrorType;
(function (ErrorType) {
    ErrorType["Unknown"] = "unknown";
    ErrorType["InvalidSelector"] = "invalid-selector";
    ErrorType["RegexParse"] = "regex-parse";
})(ErrorType = exports.ErrorType || (exports.ErrorType = {}));
function handleError(error) {
    var e_1, _a, e_2, _b;
    var _c;
    var errorMessage = (_c = error.responseJSON) === null || _c === void 0 ? void 0 : _c.relayPiiConfig[0];
    if (!errorMessage) {
        return {
            type: ErrorType.Unknown,
            message: locale_1.t('Unknown error occurred while saving data scrubbing rule'),
        };
    }
    if (errorMessage.startsWith('invalid selector: ')) {
        try {
            for (var _d = tslib_1.__values(errorMessage.split('\n')), _e = _d.next(); !_e.done; _e = _d.next()) {
                var line = _e.value;
                if (line.startsWith('1 | ')) {
                    var selector = line.slice(3);
                    return {
                        type: ErrorType.InvalidSelector,
                        message: locale_1.t('Invalid source value: %s', selector),
                    };
                }
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (_e && !_e.done && (_a = _d.return)) _a.call(_d);
            }
            finally { if (e_1) throw e_1.error; }
        }
    }
    if (errorMessage.startsWith('regex parse error:')) {
        try {
            for (var _f = tslib_1.__values(errorMessage.split('\n')), _g = _f.next(); !_g.done; _g = _f.next()) {
                var line = _g.value;
                if (line.startsWith('error:')) {
                    var regex = line.slice(6).replace(/at line \d+ column \d+/, '');
                    return {
                        type: ErrorType.RegexParse,
                        message: locale_1.t('Invalid regex: %s', regex),
                    };
                }
            }
        }
        catch (e_2_1) { e_2 = { error: e_2_1 }; }
        finally {
            try {
                if (_g && !_g.done && (_b = _f.return)) _b.call(_f);
            }
            finally { if (e_2) throw e_2.error; }
        }
    }
    return {
        type: ErrorType.Unknown,
        message: locale_1.t('An unknown error occurred while saving data scrubbing rule'),
    };
}
exports.default = handleError;
//# sourceMappingURL=handleError.jsx.map