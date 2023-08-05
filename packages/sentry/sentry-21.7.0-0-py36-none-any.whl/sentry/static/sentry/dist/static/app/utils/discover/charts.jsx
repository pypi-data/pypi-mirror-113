Object.defineProperty(exports, "__esModule", { value: true });
exports.axisDuration = exports.axisLabelFormatter = exports.tooltipFormatter = void 0;
var locale_1 = require("app/locale");
var fields_1 = require("app/utils/discover/fields");
var formatters_1 = require("app/utils/formatters");
/**
 * Formatter for chart tooltips that handle a variety of discover result values
 */
function tooltipFormatter(value, seriesName) {
    if (seriesName === void 0) { seriesName = ''; }
    switch (fields_1.aggregateOutputType(seriesName)) {
        case 'integer':
        case 'number':
            return value.toLocaleString();
        case 'percentage':
            return formatters_1.formatPercentage(value, 2);
        case 'duration':
            return formatters_1.getDuration(value / 1000, 2, true);
        default:
            return value.toString();
    }
}
exports.tooltipFormatter = tooltipFormatter;
/**
 * Formatter for chart axis labels that handle a variety of discover result values
 * This function is *very similar* to tooltipFormatter but outputs data with less precision.
 */
function axisLabelFormatter(value, seriesName, abbreviation) {
    if (abbreviation === void 0) { abbreviation = false; }
    switch (fields_1.aggregateOutputType(seriesName)) {
        case 'integer':
        case 'number':
            return abbreviation ? formatters_1.formatAbbreviatedNumber(value) : value.toLocaleString();
        case 'percentage':
            return formatters_1.formatPercentage(value, 0);
        case 'duration':
            return axisDuration(value);
        default:
            return value.toString();
    }
}
exports.axisLabelFormatter = axisLabelFormatter;
/**
 * Specialized duration formatting for axis labels.
 * In that context we are ok sacrificing accuracy for more
 * consistent sizing.
 *
 * @param value Number of milliseconds to format.
 */
function axisDuration(value) {
    if (value === 0) {
        return '0';
    }
    if (value >= formatters_1.WEEK) {
        var label_1 = (value / formatters_1.WEEK).toFixed(0);
        return locale_1.t('%swk', label_1);
    }
    if (value >= formatters_1.DAY) {
        var label_2 = (value / formatters_1.DAY).toFixed(0);
        return locale_1.t('%sd', label_2);
    }
    if (value >= formatters_1.HOUR) {
        var label_3 = (value / formatters_1.HOUR).toFixed(0);
        return locale_1.t('%shr', label_3);
    }
    if (value >= formatters_1.MINUTE) {
        var label_4 = (value / formatters_1.MINUTE).toFixed(0);
        return locale_1.t('%smin', label_4);
    }
    if (value >= formatters_1.SECOND) {
        var label_5 = (value / formatters_1.SECOND).toFixed(0);
        return locale_1.t('%ss', label_5);
    }
    var label = value.toFixed(0);
    return locale_1.t('%sms', label);
}
exports.axisDuration = axisDuration;
//# sourceMappingURL=charts.jsx.map