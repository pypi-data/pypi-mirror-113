Object.defineProperty(exports, "__esModule", { value: true });
exports.getDimensionValue = exports.isMultiSeriesStats = exports.getSeriesSelection = exports.canIncludePreviousPeriod = exports.getDiffInMinutes = exports.getSeriesApiInterval = exports.getInterval = exports.useShortInterval = exports.truncationFormatter = exports.RELEASE_LINES_THRESHOLD = exports.ONE_HOUR = exports.TWENTY_FOUR_HOURS = exports.ONE_WEEK = exports.TWO_WEEKS = exports.THIRTY_DAYS = exports.SIXTY_DAYS = void 0;
var tslib_1 = require("tslib");
var moment_1 = tslib_1.__importDefault(require("moment"));
var constants_1 = require("app/constants");
var utils_1 = require("app/utils");
var dates_1 = require("app/utils/dates");
var queryString_1 = require("app/utils/queryString");
var DEFAULT_TRUNCATE_LENGTH = 80;
// In minutes
exports.SIXTY_DAYS = 86400;
exports.THIRTY_DAYS = 43200;
exports.TWO_WEEKS = 20160;
exports.ONE_WEEK = 10080;
exports.TWENTY_FOUR_HOURS = 1440;
exports.ONE_HOUR = 60;
/**
 * If there are more releases than this number we hide "Releases" series by default
 */
exports.RELEASE_LINES_THRESHOLD = 50;
function truncationFormatter(value, truncate) {
    if (!truncate) {
        return utils_1.escape(value);
    }
    var truncationLength = truncate && typeof truncate === 'number' ? truncate : DEFAULT_TRUNCATE_LENGTH;
    var truncated = value.length > truncationLength ? value.substring(0, truncationLength) + '…' : value;
    return utils_1.escape(truncated);
}
exports.truncationFormatter = truncationFormatter;
/**
 * Use a shorter interval if the time difference is <= 24 hours.
 */
function useShortInterval(datetimeObj) {
    var diffInMinutes = getDiffInMinutes(datetimeObj);
    return diffInMinutes <= exports.TWENTY_FOUR_HOURS;
}
exports.useShortInterval = useShortInterval;
function getInterval(datetimeObj, highFidelity) {
    if (highFidelity === void 0) { highFidelity = false; }
    var diffInMinutes = getDiffInMinutes(datetimeObj);
    if (diffInMinutes >= exports.SIXTY_DAYS) {
        // Greater than or equal to 60 days
        return highFidelity ? '4h' : '1d';
    }
    if (diffInMinutes >= exports.THIRTY_DAYS) {
        // Greater than or equal to 30 days
        return highFidelity ? '1h' : '4h';
    }
    if (diffInMinutes > exports.TWENTY_FOUR_HOURS) {
        // Greater than 24 hours
        return highFidelity ? '30m' : '1h';
    }
    if (diffInMinutes > exports.ONE_HOUR) {
        // Between 1 hour and 24 hours
        return highFidelity ? '5m' : '15m';
    }
    // Less than or equal to 1 hour
    return highFidelity ? '1m' : '5m';
}
exports.getInterval = getInterval;
/**
 * Duplicate of getInterval, except that we do not support <1h granularity
 * Used by SessionsV2 and OrgStatsV2 API
 */
function getSeriesApiInterval(datetimeObj) {
    var diffInMinutes = getDiffInMinutes(datetimeObj);
    if (diffInMinutes >= exports.SIXTY_DAYS) {
        // Greater than or equal to 60 days
        return '1d';
    }
    if (diffInMinutes >= exports.THIRTY_DAYS) {
        // Greater than or equal to 30 days
        return '4h';
    }
    return '1h';
}
exports.getSeriesApiInterval = getSeriesApiInterval;
function getDiffInMinutes(datetimeObj) {
    var period = datetimeObj.period, start = datetimeObj.start, end = datetimeObj.end;
    if (start && end) {
        return moment_1.default(end).diff(start, 'minutes');
    }
    return (dates_1.parsePeriodToHours(typeof period === 'string' ? period : constants_1.DEFAULT_STATS_PERIOD) * 60);
}
exports.getDiffInMinutes = getDiffInMinutes;
// Max period (in hours) before we can no long include previous period
var MAX_PERIOD_HOURS_INCLUDE_PREVIOUS = 45 * 24;
function canIncludePreviousPeriod(includePrevious, period) {
    if (!includePrevious) {
        return false;
    }
    if (period && dates_1.parsePeriodToHours(period) > MAX_PERIOD_HOURS_INCLUDE_PREVIOUS) {
        return false;
    }
    // otherwise true
    return !!includePrevious;
}
exports.canIncludePreviousPeriod = canIncludePreviousPeriod;
/**
 * Generates a series selection based on the query parameters defined by the location.
 */
function getSeriesSelection(location, parameter) {
    if (parameter === void 0) { parameter = 'unselectedSeries'; }
    var unselectedSeries = queryString_1.decodeList(location === null || location === void 0 ? void 0 : location.query[parameter]);
    return unselectedSeries.reduce(function (selection, series) {
        selection[series] = false;
        return selection;
    }, {});
}
exports.getSeriesSelection = getSeriesSelection;
function isMultiSeriesStats(data) {
    return utils_1.defined(data) && data.data === undefined && data.totals === undefined;
}
exports.isMultiSeriesStats = isMultiSeriesStats;
// If dimension is a number convert it to pixels, otherwise use dimension
// without transform
var getDimensionValue = function (dimension) {
    if (typeof dimension === 'number') {
        return dimension + "px";
    }
    if (dimension === null) {
        return undefined;
    }
    return dimension;
};
exports.getDimensionValue = getDimensionValue;
//# sourceMappingURL=utils.jsx.map