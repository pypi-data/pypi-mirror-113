Object.defineProperty(exports, "__esModule", { value: true });
exports.getParams = exports.parseStatsPeriod = void 0;
var tslib_1 = require("tslib");
var moment_1 = tslib_1.__importDefault(require("moment"));
var constants_1 = require("app/constants");
var utils_1 = require("app/utils");
var STATS_PERIOD_PATTERN = '^(\\d+)([hdmsw])?$';
function parseStatsPeriod(input) {
    var result = input.match(STATS_PERIOD_PATTERN);
    if (!result) {
        return undefined;
    }
    var period = result[1];
    var periodLength = result[2];
    if (!periodLength) {
        // default to seconds.
        // this behaviour is based on src/sentry/utils/dates.py
        periodLength = 's';
    }
    return {
        period: period,
        periodLength: periodLength,
    };
}
exports.parseStatsPeriod = parseStatsPeriod;
function coerceStatsPeriod(input) {
    var result = parseStatsPeriod(input);
    if (!result) {
        return undefined;
    }
    var period = result.period, periodLength = result.periodLength;
    return "" + period + periodLength;
}
function getStatsPeriodValue(maybe) {
    if (Array.isArray(maybe)) {
        if (maybe.length <= 0) {
            return undefined;
        }
        var result = maybe.find(coerceStatsPeriod);
        if (!result) {
            return undefined;
        }
        return coerceStatsPeriod(result);
    }
    if (typeof maybe === 'string') {
        return coerceStatsPeriod(maybe);
    }
    return undefined;
}
// We normalize potential datetime strings into the form that would be valid
// if it were to be parsed by datetime.strptime using the format %Y-%m-%dT%H:%M:%S.%f
// This format was transformed to the form that moment.js understands using
// https://gist.github.com/asafge/0b13c5066d06ae9a4446
var normalizeDateTimeString = function (input) {
    if (!input) {
        return undefined;
    }
    var parsed = moment_1.default.utc(input);
    if (!parsed.isValid()) {
        return undefined;
    }
    return parsed.format('YYYY-MM-DDTHH:mm:ss.SSS');
};
var getDateTimeString = function (maybe) {
    if (Array.isArray(maybe)) {
        if (maybe.length <= 0) {
            return undefined;
        }
        var result = maybe.find(function (needle) { return moment_1.default.utc(needle).isValid(); });
        return normalizeDateTimeString(result);
    }
    return normalizeDateTimeString(maybe);
};
var parseUtcValue = function (utc) {
    if (utils_1.defined(utc)) {
        return utc === true || utc === 'true' ? 'true' : 'false';
    }
    return undefined;
};
var getUtcValue = function (maybe) {
    if (Array.isArray(maybe)) {
        if (maybe.length <= 0) {
            return undefined;
        }
        return maybe.find(function (needle) { return !!parseUtcValue(needle); });
    }
    return parseUtcValue(maybe);
};
function getParams(params, _a) {
    var _b, _c;
    var _d = _a === void 0 ? {} : _a, _e = _d.allowEmptyPeriod, allowEmptyPeriod = _e === void 0 ? false : _e, _f = _d.allowAbsoluteDatetime, allowAbsoluteDatetime = _f === void 0 ? true : _f, _g = _d.allowAbsolutePageDatetime, allowAbsolutePageDatetime = _g === void 0 ? false : _g, _h = _d.defaultStatsPeriod, defaultStatsPeriod = _h === void 0 ? constants_1.DEFAULT_STATS_PERIOD : _h;
    var pageStatsPeriod = params.pageStatsPeriod, pageStart = params.pageStart, pageEnd = params.pageEnd, pageUtc = params.pageUtc, start = params.start, end = params.end, period = params.period, statsPeriod = params.statsPeriod, utc = params.utc, otherParams = tslib_1.__rest(params, ["pageStatsPeriod", "pageStart", "pageEnd", "pageUtc", "start", "end", "period", "statsPeriod", "utc"]);
    // `statsPeriod` takes precedence for now
    var coercedPeriod = getStatsPeriodValue(pageStatsPeriod) ||
        getStatsPeriodValue(statsPeriod) ||
        getStatsPeriodValue(period);
    var dateTimeStart = allowAbsoluteDatetime
        ? allowAbsolutePageDatetime
            ? (_b = getDateTimeString(pageStart)) !== null && _b !== void 0 ? _b : getDateTimeString(start)
            : getDateTimeString(start)
        : null;
    var dateTimeEnd = allowAbsoluteDatetime
        ? allowAbsolutePageDatetime
            ? (_c = getDateTimeString(pageEnd)) !== null && _c !== void 0 ? _c : getDateTimeString(end)
            : getDateTimeString(end)
        : null;
    if (!(dateTimeStart && dateTimeEnd)) {
        if (!coercedPeriod && !allowEmptyPeriod) {
            coercedPeriod = defaultStatsPeriod;
        }
    }
    return Object.fromEntries(Object.entries(tslib_1.__assign({ statsPeriod: coercedPeriod, start: coercedPeriod ? null : dateTimeStart, end: coercedPeriod ? null : dateTimeEnd, 
        // coerce utc into a string (it can be both: a string representation from router,
        // or a boolean from time range picker)
        utc: getUtcValue(pageUtc !== null && pageUtc !== void 0 ? pageUtc : utc) }, otherParams))
        // Filter null values
        .filter(function (_a) {
        var _b = tslib_1.__read(_a, 2), _key = _b[0], value = _b[1];
        return utils_1.defined(value);
    }));
}
exports.getParams = getParams;
//# sourceMappingURL=getParams.jsx.map