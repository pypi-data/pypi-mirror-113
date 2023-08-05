Object.defineProperty(exports, "__esModule", { value: true });
exports.getXAxisLabelInterval = exports.getTooltipFormatter = exports.getXAxisDates = exports.getDateFromUnixTimestamp = exports.getDateFromMoment = exports.FORMAT_DATETIME_HOURLY = exports.FORMAT_DATETIME_DAILY = void 0;
var tslib_1 = require("tslib");
var moment_1 = tslib_1.__importDefault(require("moment"));
var getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
var types_1 = require("app/types");
var dates_1 = require("app/utils/dates");
var utils_1 = require("../utils");
/**
 * Avoid changing "MMM D" format as X-axis labels on UsageChart are naively
 * truncated by date.slice(0, 6). This avoids "..." when truncating by ECharts.
 */
exports.FORMAT_DATETIME_DAILY = 'MMM D';
exports.FORMAT_DATETIME_HOURLY = 'MMM D LT';
/**
 * Used to generate X-axis data points and labels for UsageChart
 * Ensure that this method is idempotent and doesn't change the moment object
 * that is passed in
 *
 * If hours are not shown, this method will need to use UTC to avoid oddities
 * caused by the user being ahead/behind UTC.
 */
function getDateFromMoment(m, interval, useUtc) {
    if (interval === void 0) { interval = '1d'; }
    if (useUtc === void 0) { useUtc = false; }
    var days = dates_1.parsePeriodToHours(interval) / 24;
    if (days >= 1) {
        return moment_1.default.utc(m).format(exports.FORMAT_DATETIME_DAILY);
    }
    var parsedInterval = getParams_1.parseStatsPeriod(interval);
    var datetime = useUtc ? moment_1.default(m).utc() : moment_1.default(m).local();
    return parsedInterval
        ? datetime.format(exports.FORMAT_DATETIME_HOURLY) + " - " + datetime
            .add(parsedInterval.period, parsedInterval.periodLength)
            .format('LT (Z)')
        : datetime.format(exports.FORMAT_DATETIME_HOURLY);
}
exports.getDateFromMoment = getDateFromMoment;
function getDateFromUnixTimestamp(timestamp) {
    var date = moment_1.default.unix(timestamp);
    return getDateFromMoment(date);
}
exports.getDateFromUnixTimestamp = getDateFromUnixTimestamp;
function getXAxisDates(dateStart, dateEnd, dateUtc, interval) {
    var _a;
    if (dateUtc === void 0) { dateUtc = true; }
    if (interval === void 0) { interval = '1d'; }
    var range = [];
    var start = moment_1.default(dateStart).utc().startOf('h');
    var end = moment_1.default(dateEnd).startOf('h');
    if (!start.isValid() || !end.isValid()) {
        return range;
    }
    var _b = (_a = getParams_1.parseStatsPeriod(interval)) !== null && _a !== void 0 ? _a : {
        period: 1,
        periodLength: 'd',
    }, period = _b.period, periodLength = _b.periodLength;
    while (!start.isAfter(end)) {
        range.push(getDateFromMoment(start, interval, dateUtc));
        start.add(period, periodLength); // FIXME(ts): Something odd with momentjs types
    }
    return range;
}
exports.getXAxisDates = getXAxisDates;
function getTooltipFormatter(dataCategory) {
    if (dataCategory === types_1.DataCategory.ATTACHMENTS) {
        return function (val) {
            if (val === void 0) { val = 0; }
            return utils_1.formatUsageWithUnits(val, types_1.DataCategory.ATTACHMENTS, { useUnitScaling: true });
        };
    }
    return function (val) {
        if (val === void 0) { val = 0; }
        return val.toLocaleString();
    };
}
exports.getTooltipFormatter = getTooltipFormatter;
var MAX_NUMBER_OF_LABELS = 10;
/**
 *
 * @param dataPeriod - Quantity of hours covered by the data
 * @param numBars - Quantity of data points covered by the dataPeriod
 */
function getXAxisLabelInterval(dataPeriod, numBars) {
    return dataPeriod > 7 * 24
        ? getLabelIntervalLongPeriod(dataPeriod, numBars)
        : getLabelIntervalShortPeriod(dataPeriod, numBars);
}
exports.getXAxisLabelInterval = getXAxisLabelInterval;
/**
 * @param dataPeriod - Quantity of hours covered by data, expected 7+ days
 */
function getLabelIntervalLongPeriod(dataPeriod, numBars) {
    var days = dataPeriod / 24;
    if (days <= 7) {
        throw new Error('This method should be used for periods > 7 days');
    }
    // Use 1 tick per day
    var numTicks = days;
    var numLabels = numTicks;
    var daysBetweenLabels = [2, 4, 7, 14];
    var daysBetweenTicks = [1, 2, 7, 7];
    for (var i = 0; i < daysBetweenLabels.length && numLabels > MAX_NUMBER_OF_LABELS; i++) {
        numLabels = numTicks / daysBetweenLabels[i];
        numTicks = days / daysBetweenTicks[i];
    }
    return {
        xAxisTickInterval: numBars / numTicks - 1,
        xAxisLabelInterval: numBars / numLabels - 1,
    };
}
/**
 * @param dataPeriod - Quantity of hours covered by data, expected <7 days
 */
function getLabelIntervalShortPeriod(dataPeriod, numBars) {
    var days = dataPeriod / 24;
    if (days > 7) {
        throw new Error('This method should be used for periods <= 7 days');
    }
    // Use 1 tick/label per day, since it's guaranteed to be 7 or less
    var numTicks = days;
    var interval = numBars / numTicks;
    return {
        xAxisTickInterval: interval - 1,
        xAxisLabelInterval: interval - 1,
    };
}
//# sourceMappingURL=utils.jsx.map