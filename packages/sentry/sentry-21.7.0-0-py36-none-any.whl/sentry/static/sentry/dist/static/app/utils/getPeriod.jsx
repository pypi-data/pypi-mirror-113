Object.defineProperty(exports, "__esModule", { value: true });
exports.getPeriod = void 0;
var tslib_1 = require("tslib");
var moment_1 = tslib_1.__importDefault(require("moment"));
var constants_1 = require("app/constants");
var dates_1 = require("app/utils/dates");
/**
 * Gets the period to query with if we need to double the initial period in order
 * to get data for the previous period
 *
 * Returns an object with either a period or start/end dates ({statsPeriod: string} or {start: string, end: string})
 */
var getPeriod = function (_a, _b) {
    var period = _a.period, start = _a.start, end = _a.end;
    var _c = _b === void 0 ? {} : _b, shouldDoublePeriod = _c.shouldDoublePeriod;
    if (!period && !start && !end) {
        period = constants_1.DEFAULT_STATS_PERIOD;
    }
    // you can not specify both relative and absolute periods
    // relative period takes precedence
    if (period) {
        if (!shouldDoublePeriod) {
            return { statsPeriod: period };
        }
        var _d = tslib_1.__read(period.match(/([0-9]+)([mhdw])/), 3), periodNumber = _d[1], periodLength = _d[2];
        return { statsPeriod: "" + parseInt(periodNumber, 10) * 2 + periodLength };
    }
    if (!start || !end) {
        throw new Error('start and end required');
    }
    var formattedStart = dates_1.getUtcDateString(start);
    var formattedEnd = dates_1.getUtcDateString(end);
    if (shouldDoublePeriod) {
        // get duration of end - start and double
        var diff = moment_1.default(end).diff(moment_1.default(start));
        var previousPeriodStart = moment_1.default(start).subtract(diff);
        // This is not as accurate as having 2 start/end objs
        return {
            start: dates_1.getUtcDateString(previousPeriodStart),
            end: formattedEnd,
        };
    }
    return {
        start: formattedStart,
        end: formattedEnd,
    };
};
exports.getPeriod = getPeriod;
//# sourceMappingURL=getPeriod.jsx.map