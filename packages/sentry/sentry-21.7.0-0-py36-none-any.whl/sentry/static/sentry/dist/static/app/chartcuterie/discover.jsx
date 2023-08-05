Object.defineProperty(exports, "__esModule", { value: true });
exports.discoverCharts = void 0;
var tslib_1 = require("tslib");
var xAxis_1 = tslib_1.__importDefault(require("app/components/charts/components/xAxis"));
var areaSeries_1 = tslib_1.__importDefault(require("app/components/charts/series/areaSeries"));
var barSeries_1 = tslib_1.__importDefault(require("app/components/charts/series/barSeries"));
var theme_1 = require("app/utils/theme");
var slack_1 = require("./slack");
var types_1 = require("./types");
var discoverxAxis = xAxis_1.default({
    theme: theme_1.lightTheme,
    boundaryGap: true,
    splitNumber: 3,
    isGroupedByDate: true,
    axisLabel: { fontSize: 11 },
});
exports.discoverCharts = [];
exports.discoverCharts.push(tslib_1.__assign({ key: types_1.ChartType.SLACK_DISCOVER_TOTAL_PERIOD, getOption: function (data) {
        var color = theme_1.lightTheme.charts.getColorPalette(data.stats.data.length - 2);
        var areaSeries = areaSeries_1.default({
            name: data.seriesName,
            data: data.stats.data.map(function (_a) {
                var _b = tslib_1.__read(_a, 2), timestamp = _b[0], countsForTimestamp = _b[1];
                return [
                    timestamp * 1000,
                    countsForTimestamp.reduce(function (acc, _a) {
                        var count = _a.count;
                        return acc + count;
                    }, 0),
                ];
            }),
            lineStyle: { color: color === null || color === void 0 ? void 0 : color[0], opacity: 1, width: 0.4 },
            areaStyle: { color: color === null || color === void 0 ? void 0 : color[0], opacity: 1 },
        });
        return tslib_1.__assign(tslib_1.__assign({}, slack_1.slackChartDefaults), { useUTC: true, color: color, series: [areaSeries] });
    } }, slack_1.slackChartSize));
exports.discoverCharts.push(tslib_1.__assign({ key: types_1.ChartType.SLACK_DISCOVER_TOTAL_DAILY, getOption: function (data) {
        var color = theme_1.lightTheme.charts.getColorPalette(data.stats.data.length - 2);
        var barSeries = barSeries_1.default({
            name: data.seriesName,
            data: data.stats.data.map(function (_a) {
                var _b = tslib_1.__read(_a, 2), timestamp = _b[0], countsForTimestamp = _b[1];
                return ({
                    value: [
                        timestamp * 1000,
                        countsForTimestamp.reduce(function (acc, _a) {
                            var count = _a.count;
                            return acc + count;
                        }, 0),
                    ],
                });
            }),
            itemStyle: { color: color === null || color === void 0 ? void 0 : color[0], opacity: 1 },
        });
        return tslib_1.__assign(tslib_1.__assign({}, slack_1.slackChartDefaults), { xAxis: discoverxAxis, useUTC: true, color: color, series: [barSeries] });
    } }, slack_1.slackChartSize));
exports.discoverCharts.push(tslib_1.__assign({ key: types_1.ChartType.SLACK_DISCOVER_TOP5_PERIOD, getOption: function (data) {
        var stats = Object.values(data.stats);
        var color = theme_1.lightTheme.charts.getColorPalette(stats.length - 2);
        var series = stats
            .sort(function (a, b) { var _a, _b; return ((_a = a.order) !== null && _a !== void 0 ? _a : 0) - ((_b = b.order) !== null && _b !== void 0 ? _b : 0); })
            .map(function (topSeries, i) {
            return areaSeries_1.default({
                stack: 'area',
                data: topSeries.data.map(function (_a) {
                    var _b = tslib_1.__read(_a, 2), timestamp = _b[0], countsForTimestamp = _b[1];
                    return [
                        timestamp * 1000,
                        countsForTimestamp.reduce(function (acc, _a) {
                            var count = _a.count;
                            return acc + count;
                        }, 0),
                    ];
                }),
                lineStyle: { color: color === null || color === void 0 ? void 0 : color[i], opacity: 1, width: 0.4 },
                areaStyle: { color: color === null || color === void 0 ? void 0 : color[i], opacity: 1 },
            });
        });
        return tslib_1.__assign(tslib_1.__assign({}, slack_1.slackChartDefaults), { xAxis: discoverxAxis, useUTC: true, color: color, series: series });
    } }, slack_1.slackChartSize));
exports.discoverCharts.push(tslib_1.__assign({ key: types_1.ChartType.SLACK_DISCOVER_TOP5_DAILY, getOption: function (data) {
        var stats = Object.values(data.stats);
        var color = theme_1.lightTheme.charts.getColorPalette(stats.length - 2);
        var series = stats
            .sort(function (a, b) { var _a, _b; return ((_a = a.order) !== null && _a !== void 0 ? _a : 0) - ((_b = b.order) !== null && _b !== void 0 ? _b : 0); })
            .map(function (topSeries, i) {
            return barSeries_1.default({
                stack: 'area',
                data: topSeries.data.map(function (_a) {
                    var _b = tslib_1.__read(_a, 2), timestamp = _b[0], countsForTimestamp = _b[1];
                    return [
                        timestamp * 1000,
                        countsForTimestamp.reduce(function (acc, _a) {
                            var count = _a.count;
                            return acc + count;
                        }, 0),
                    ];
                }),
                itemStyle: { color: color === null || color === void 0 ? void 0 : color[i], opacity: 1 },
            });
        });
        return tslib_1.__assign(tslib_1.__assign({}, slack_1.slackChartDefaults), { xAxis: discoverxAxis, useUTC: true, color: color, series: series });
    } }, slack_1.slackChartSize));
//# sourceMappingURL=discover.jsx.map