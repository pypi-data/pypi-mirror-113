Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var merge_1 = tslib_1.__importDefault(require("lodash/merge"));
var dates_1 = require("app/utils/dates");
var utils_1 = require("../utils");
function XAxis(_a) {
    var isGroupedByDate = _a.isGroupedByDate, useShortDate = _a.useShortDate, theme = _a.theme, start = _a.start, end = _a.end, period = _a.period, utc = _a.utc, props = tslib_1.__rest(_a, ["isGroupedByDate", "useShortDate", "theme", "start", "end", "period", "utc"]);
    var axisLabelFormatter = function (value, index) {
        if (isGroupedByDate) {
            var timeFormat = dates_1.getTimeFormat();
            var dateFormat = useShortDate ? 'MMM Do' : "MMM D " + timeFormat;
            var firstItem = index === 0;
            var format = utils_1.useShortInterval({ start: start, end: end, period: period }) && !firstItem ? timeFormat : dateFormat;
            return dates_1.getFormattedDate(value, format, { local: !utc });
        }
        else if (props.truncate) {
            return utils_1.truncationFormatter(value, props.truncate);
        }
        else {
            return undefined;
        }
    };
    return merge_1.default({
        type: isGroupedByDate ? 'time' : 'category',
        boundaryGap: false,
        axisLine: {
            lineStyle: {
                color: theme.chartLabel,
            },
        },
        axisTick: {
            lineStyle: {
                color: theme.chartLabel,
            },
        },
        splitLine: {
            show: false,
        },
        axisLabel: {
            color: theme.chartLabel,
            fontFamily: theme.text.family,
            margin: 12,
            // This was default with ChartZoom, we are making it default for all charts now
            // Otherwise the xAxis can look congested when there is always a min/max label
            showMaxLabel: false,
            showMinLabel: false,
            formatter: axisLabelFormatter,
        },
        axisPointer: {
            show: true,
            type: 'line',
            label: {
                show: false,
            },
            lineStyle: {
                width: 0.5,
            },
        },
    }, props);
}
exports.default = XAxis;
//# sourceMappingURL=xAxis.jsx.map