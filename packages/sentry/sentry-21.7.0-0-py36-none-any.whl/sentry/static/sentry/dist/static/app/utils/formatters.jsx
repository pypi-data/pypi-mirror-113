Object.defineProperty(exports, "__esModule", { value: true });
exports.formatAbbreviatedNumber = exports.formatPercentage = exports.formatFloat = exports.getExactDuration = exports.getDuration = exports.SECOND = exports.MINUTE = exports.HOUR = exports.DAY = exports.WEEK = exports.MONTH = exports.formatVersion = exports.userDisplayName = void 0;
var tslib_1 = require("tslib");
var release_parser_1 = require("@sentry/release-parser");
var round_1 = tslib_1.__importDefault(require("lodash/round"));
var locale_1 = require("app/locale");
function userDisplayName(user, includeEmail) {
    var _a, _b;
    if (includeEmail === void 0) { includeEmail = true; }
    var displayName = String((_a = user === null || user === void 0 ? void 0 : user.name) !== null && _a !== void 0 ? _a : locale_1.t('Unknown author')).trim();
    if (displayName.length <= 0) {
        displayName = locale_1.t('Unknown author');
    }
    var email = String((_b = user === null || user === void 0 ? void 0 : user.email) !== null && _b !== void 0 ? _b : '').trim();
    if (email.length > 0 && email !== displayName && includeEmail) {
        displayName += ' (' + email + ')';
    }
    return displayName;
}
exports.userDisplayName = userDisplayName;
var formatVersion = function (rawVersion, withPackage) {
    if (withPackage === void 0) { withPackage = false; }
    try {
        var parsedVersion = new release_parser_1.Release(rawVersion);
        var versionToDisplay = parsedVersion.describe();
        if (versionToDisplay.length) {
            return "" + versionToDisplay + (withPackage && parsedVersion.package ? ", " + parsedVersion.package : '');
        }
        return rawVersion;
    }
    catch (_a) {
        return rawVersion;
    }
};
exports.formatVersion = formatVersion;
function roundWithFixed(value, fixedDigits) {
    var label = value.toFixed(fixedDigits);
    var result = fixedDigits <= 0 ? Math.round(value) : value;
    return { label: label, result: result };
}
// in milliseconds
exports.MONTH = 2629800000;
exports.WEEK = 604800000;
exports.DAY = 86400000;
exports.HOUR = 3600000;
exports.MINUTE = 60000;
exports.SECOND = 1000;
function getDuration(seconds, fixedDigits, abbreviation, extraShort) {
    if (fixedDigits === void 0) { fixedDigits = 0; }
    if (abbreviation === void 0) { abbreviation = false; }
    if (extraShort === void 0) { extraShort = false; }
    // value in milliseconds
    var msValue = seconds * 1000;
    var value = Math.abs(msValue);
    if (value >= exports.MONTH && !extraShort) {
        var _a = roundWithFixed(msValue / exports.MONTH, fixedDigits), label_1 = _a.label, result = _a.result;
        return "" + label_1 + (abbreviation ? locale_1.tn('mo', 'mos', result) : " " + locale_1.tn('month', 'months', result));
    }
    if (value >= exports.WEEK) {
        var _b = roundWithFixed(msValue / exports.WEEK, fixedDigits), label_2 = _b.label, result = _b.result;
        if (extraShort) {
            return "" + label_2 + locale_1.t('w');
        }
        if (abbreviation) {
            return "" + label_2 + locale_1.t('wk');
        }
        return label_2 + " " + locale_1.tn('week', 'weeks', result);
    }
    if (value >= 172800000) {
        var _c = roundWithFixed(msValue / exports.DAY, fixedDigits), label_3 = _c.label, result = _c.result;
        return "" + label_3 + (abbreviation || extraShort ? locale_1.t('d') : " " + locale_1.tn('day', 'days', result));
    }
    if (value >= 7200000) {
        var _d = roundWithFixed(msValue / exports.HOUR, fixedDigits), label_4 = _d.label, result = _d.result;
        if (extraShort) {
            return "" + label_4 + locale_1.t('h');
        }
        if (abbreviation) {
            return "" + label_4 + locale_1.t('hr');
        }
        return label_4 + " " + locale_1.tn('hour', 'hours', result);
    }
    if (value >= 120000) {
        var _e = roundWithFixed(msValue / exports.MINUTE, fixedDigits), label_5 = _e.label, result = _e.result;
        if (extraShort) {
            return "" + label_5 + locale_1.t('m');
        }
        if (abbreviation) {
            return "" + label_5 + locale_1.t('min');
        }
        return label_5 + " " + locale_1.tn('minute', 'minutes', result);
    }
    if (value >= exports.SECOND) {
        var _f = roundWithFixed(msValue / exports.SECOND, fixedDigits), label_6 = _f.label, result = _f.result;
        if (extraShort || abbreviation) {
            return "" + label_6 + locale_1.t('s');
        }
        return label_6 + " " + locale_1.tn('second', 'seconds', result);
    }
    var label = roundWithFixed(msValue, fixedDigits).label;
    return label + locale_1.t('ms');
}
exports.getDuration = getDuration;
function getExactDuration(seconds, abbreviation) {
    if (abbreviation === void 0) { abbreviation = false; }
    var convertDuration = function (secs, abbr) {
        // value in milliseconds
        var msValue = round_1.default(secs * 1000);
        var value = round_1.default(Math.abs(secs * 1000));
        var divideBy = function (time) {
            return {
                quotient: msValue < 0 ? Math.ceil(msValue / time) : Math.floor(msValue / time),
                remainder: msValue % time,
            };
        };
        if (value >= exports.WEEK) {
            var _a = divideBy(exports.WEEK), quotient = _a.quotient, remainder = _a.remainder;
            return "" + quotient + (abbr ? locale_1.t('wk') : " " + locale_1.tn('week', 'weeks', quotient)) + " " + convertDuration(remainder / 1000, abbr);
        }
        if (value >= exports.DAY) {
            var _b = divideBy(exports.DAY), quotient = _b.quotient, remainder = _b.remainder;
            return "" + quotient + (abbr ? locale_1.t('d') : " " + locale_1.tn('day', 'days', quotient)) + " " + convertDuration(remainder / 1000, abbr);
        }
        if (value >= exports.HOUR) {
            var _c = divideBy(exports.HOUR), quotient = _c.quotient, remainder = _c.remainder;
            return "" + quotient + (abbr ? locale_1.t('hr') : " " + locale_1.tn('hour', 'hours', quotient)) + " " + convertDuration(remainder / 1000, abbr);
        }
        if (value >= exports.MINUTE) {
            var _d = divideBy(exports.MINUTE), quotient = _d.quotient, remainder = _d.remainder;
            return "" + quotient + (abbr ? locale_1.t('min') : " " + locale_1.tn('minute', 'minutes', quotient)) + " " + convertDuration(remainder / 1000, abbr);
        }
        if (value >= exports.SECOND) {
            var _e = divideBy(exports.SECOND), quotient = _e.quotient, remainder = _e.remainder;
            return "" + quotient + (abbr ? locale_1.t('s') : " " + locale_1.tn('second', 'seconds', quotient)) + " " + convertDuration(remainder / 1000, abbr);
        }
        if (value === 0) {
            return '';
        }
        return "" + msValue + (abbr ? locale_1.t('ms') : " " + locale_1.tn('millisecond', 'milliseconds', value));
    };
    var result = convertDuration(seconds, abbreviation).trim();
    if (result.length) {
        return result;
    }
    return "0" + (abbreviation ? locale_1.t('ms') : " " + locale_1.t('milliseconds'));
}
exports.getExactDuration = getExactDuration;
function formatFloat(number, places) {
    var multi = Math.pow(10, places);
    return parseInt((number * multi).toString(), 10) / multi;
}
exports.formatFloat = formatFloat;
/**
 * Format a value between 0 and 1 as a percentage
 */
function formatPercentage(value, places) {
    if (places === void 0) { places = 2; }
    if (value === 0) {
        return '0%';
    }
    return (round_1.default(value * 100, places).toLocaleString(undefined, {
        maximumFractionDigits: places,
    }) + '%');
}
exports.formatPercentage = formatPercentage;
var numberFormats = [
    [1000000000, 'b'],
    [1000000, 'm'],
    [1000, 'k'],
];
function formatAbbreviatedNumber(number) {
    number = Number(number);
    var lookup;
    // eslint-disable-next-line no-cond-assign
    for (var i = 0; (lookup = numberFormats[i]); i++) {
        var _a = tslib_1.__read(lookup, 2), suffixNum = _a[0], suffix = _a[1];
        var shortValue = Math.floor(number / suffixNum);
        var fitsBound = number % suffixNum;
        if (shortValue <= 0) {
            continue;
        }
        return shortValue / 10 > 1 || !fitsBound
            ? "" + shortValue + suffix
            : "" + formatFloat(number / suffixNum, 1) + suffix;
    }
    return number.toLocaleString();
}
exports.formatAbbreviatedNumber = formatAbbreviatedNumber;
//# sourceMappingURL=formatters.jsx.map