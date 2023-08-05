Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var moment_1 = tslib_1.__importDefault(require("moment"));
var markLine_1 = tslib_1.__importDefault(require("app/components/charts/components/markLine"));
var markPoint_1 = tslib_1.__importDefault(require("app/components/charts/components/markPoint"));
var lineChart_1 = tslib_1.__importDefault(require("app/components/charts/lineChart"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var closedSymbol_1 = tslib_1.__importDefault(require("./closedSymbol"));
var startedSymbol_1 = tslib_1.__importDefault(require("./startedSymbol"));
function truthy(value) {
    return !!value;
}
/**
 * So we'll have to see how this looks with real data, but echarts requires
 * an explicit (x,y) value to draw a symbol (incident started/closed bubble).
 *
 * This uses the closest date *without* going over.
 *
 * AFAICT we can't give it an x-axis value and have it draw on the line,
 * so we probably need to calculate the y-axis value ourselves if we want it placed
 * at the exact time.
 *
 * @param data Data array
 * @param needle the target timestamp
 */
function getNearbyIndex(data, needle) {
    // `data` is sorted, return the first index whose value (timestamp) is > `needle`
    var index = data.findIndex(function (_a) {
        var _b = tslib_1.__read(_a, 1), ts = _b[0];
        return ts > needle;
    });
    // this shouldn't happen, as we try to buffer dates before start/end dates
    if (index === 0) {
        return 0;
    }
    return index !== -1 ? index - 1 : data.length - 1;
}
var Chart = function (props) {
    var aggregate = props.aggregate, data = props.data, started = props.started, closed = props.closed, triggers = props.triggers, resolveThreshold = props.resolveThreshold;
    var startedTs = started && moment_1.default.utc(started).unix();
    var closedTs = closed && moment_1.default.utc(closed).unix();
    var chartData = data.map(function (_a) {
        var _b = tslib_1.__read(_a, 2), ts = _b[0], val = _b[1];
        return [
            ts * 1000,
            val.length ? val.reduce(function (acc, _a) {
                var _b = _a === void 0 ? { count: 0 } : _a, count = _b.count;
                return acc + count;
            }, 0) : 0,
        ];
    });
    var startedCoordinate = startedTs
        ? chartData[getNearbyIndex(data, startedTs)]
        : undefined;
    var showClosedMarker = data && closedTs && data[data.length - 1] && data[data.length - 1][0] >= closedTs
        ? true
        : false;
    var closedCoordinate = closedTs && showClosedMarker ? chartData[getNearbyIndex(data, closedTs)] : undefined;
    var seriesName = aggregate;
    var warningTrigger = triggers === null || triggers === void 0 ? void 0 : triggers.find(function (trig) { return trig.label === 'warning'; });
    var criticalTrigger = triggers === null || triggers === void 0 ? void 0 : triggers.find(function (trig) { return trig.label === 'critical'; });
    var warningTriggerAlertThreshold = typeof (warningTrigger === null || warningTrigger === void 0 ? void 0 : warningTrigger.alertThreshold) === 'number'
        ? warningTrigger === null || warningTrigger === void 0 ? void 0 : warningTrigger.alertThreshold
        : undefined;
    var criticalTriggerAlertThreshold = typeof (criticalTrigger === null || criticalTrigger === void 0 ? void 0 : criticalTrigger.alertThreshold) === 'number'
        ? criticalTrigger === null || criticalTrigger === void 0 ? void 0 : criticalTrigger.alertThreshold
        : undefined;
    var alertResolveThreshold = typeof resolveThreshold === 'number' ? resolveThreshold : undefined;
    var marklinePrecision = Math.max.apply(Math, tslib_1.__spreadArray([], tslib_1.__read([
        warningTriggerAlertThreshold,
        criticalTriggerAlertThreshold,
        alertResolveThreshold,
    ].map(function (decimal) {
        if (!decimal || !isFinite(decimal))
            return 0;
        var e = 1;
        var p = 0;
        while (Math.round(decimal * e) / e !== decimal) {
            e *= 10;
            p += 1;
        }
        return p;
    }))));
    var lineSeries = [
        {
            // e.g. Events or Users
            seriesName: seriesName,
            dataArray: chartData,
            data: [],
            markPoint: markPoint_1.default({
                data: tslib_1.__spreadArray([
                    {
                        labelForValue: seriesName,
                        seriesName: seriesName,
                        symbol: "image://" + startedSymbol_1.default,
                        name: locale_1.t('Alert Triggered'),
                        coord: startedCoordinate,
                    }
                ], tslib_1.__read((closedTs
                    ? [
                        {
                            labelForValue: seriesName,
                            seriesName: seriesName,
                            symbol: "image://" + closedSymbol_1.default,
                            symbolSize: 24,
                            name: locale_1.t('Alert Resolved'),
                            coord: closedCoordinate,
                        },
                    ]
                    : []))), // TODO(ts): data on this type is likely incomplete (needs @types/echarts@4.6.2)
            }),
        },
        warningTrigger &&
            warningTriggerAlertThreshold && {
            seriesName: 'Warning Alert',
            type: 'line',
            markLine: markLine_1.default({
                silent: true,
                lineStyle: { color: theme_1.default.yellow300 },
                data: [
                    {
                        yAxis: warningTriggerAlertThreshold,
                    },
                ],
                precision: marklinePrecision,
                label: {
                    show: true,
                    position: 'insideEndTop',
                    formatter: 'WARNING',
                    color: theme_1.default.yellow300,
                    fontSize: 10,
                }, // TODO(ts): Color is not an exposed option for label,
            }),
            data: [],
        },
        criticalTrigger &&
            criticalTriggerAlertThreshold && {
            seriesName: 'Critical Alert',
            type: 'line',
            markLine: markLine_1.default({
                silent: true,
                lineStyle: { color: theme_1.default.red200 },
                data: [
                    {
                        yAxis: criticalTriggerAlertThreshold,
                    },
                ],
                precision: marklinePrecision,
                label: {
                    show: true,
                    position: 'insideEndTop',
                    formatter: 'CRITICAL',
                    color: theme_1.default.red300,
                    fontSize: 10,
                }, // TODO(ts): Color is not an exposed option for label,
            }),
            data: [],
        },
        criticalTrigger &&
            alertResolveThreshold && {
            seriesName: 'Critical Resolve',
            type: 'line',
            markLine: markLine_1.default({
                silent: true,
                lineStyle: { color: theme_1.default.gray200 },
                data: [
                    {
                        yAxis: alertResolveThreshold,
                    },
                ],
                precision: marklinePrecision,
                label: {
                    show: true,
                    position: 'insideEndBottom',
                    formatter: 'CRITICAL RESOLUTION',
                    color: theme_1.default.gray200,
                    fontSize: 10,
                }, // TODO(ts): Color is not an option for label,
            }),
            data: [],
        },
    ].filter(truthy);
    return (<lineChart_1.default isGroupedByDate showTimeInTooltip grid={{
            left: 0,
            right: 0,
            top: space_1.default(2),
            bottom: 0,
        }} series={lineSeries}/>);
};
exports.default = Chart;
//# sourceMappingURL=chart.jsx.map