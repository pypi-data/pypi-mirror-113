Object.defineProperty(exports, "__esModule", { value: true });
exports.getFormattedTimestamp = void 0;
var tslib_1 = require("tslib");
var moment_1 = tslib_1.__importDefault(require("moment"));
var locale_1 = require("app/locale");
var utils_1 = require("app/utils");
var dates_1 = require("app/utils/dates");
var formatters_1 = require("app/utils/formatters");
var timeFormat = 'HH:mm:ss';
var timeDateFormat = "ll " + timeFormat;
var getRelativeTime = function (parsedTime, parsedTimeToCompareWith, displayRelativeTime) {
    // ll is necessary here, otherwise moment(x).from will throw an error
    var formattedTime = moment_1.default(parsedTime.format(timeDateFormat));
    var formattedTimeToCompareWith = parsedTimeToCompareWith.format(timeDateFormat);
    var timeDiff = Math.abs(formattedTime.diff(formattedTimeToCompareWith));
    var shortRelativeTime = formatters_1.getDuration(Math.round(timeDiff / 1000), 0, true).replace(/\s/g, '');
    if (timeDiff !== 0) {
        return displayRelativeTime
            ? "-" + shortRelativeTime
            : locale_1.t('%s before', shortRelativeTime);
    }
    return "\u00A0" + shortRelativeTime;
};
var getAbsoluteTimeFormat = function (format) {
    if (dates_1.use24Hours()) {
        return format;
    }
    return format + " A";
};
var getFormattedTimestamp = function (timestamp, relativeTimestamp, displayRelativeTime) {
    var parsedTimestamp = moment_1.default(timestamp);
    var date = parsedTimestamp.format('ll');
    var displayMilliSeconds = utils_1.defined(parsedTimestamp.milliseconds());
    var relativeTime = getRelativeTime(parsedTimestamp, moment_1.default(relativeTimestamp), displayRelativeTime);
    if (!displayRelativeTime) {
        return {
            date: date + " " + parsedTimestamp.format(getAbsoluteTimeFormat('HH:mm')),
            time: relativeTime,
            displayTime: parsedTimestamp.format(timeFormat),
        };
    }
    return {
        date: date,
        time: parsedTimestamp.format(getAbsoluteTimeFormat(displayMilliSeconds ? timeFormat + ".SSS" : timeFormat)),
        displayTime: relativeTime,
    };
};
exports.getFormattedTimestamp = getFormattedTimestamp;
//# sourceMappingURL=utils.jsx.map