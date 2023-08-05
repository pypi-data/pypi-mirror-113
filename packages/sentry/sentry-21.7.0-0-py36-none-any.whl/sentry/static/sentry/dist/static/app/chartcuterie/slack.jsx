Object.defineProperty(exports, "__esModule", { value: true });
exports.slackChartDefaults = exports.slackChartSize = void 0;
var tslib_1 = require("tslib");
var grid_1 = tslib_1.__importDefault(require("app/components/charts/components/grid"));
var legend_1 = tslib_1.__importDefault(require("app/components/charts/components/legend"));
var xAxis_1 = tslib_1.__importDefault(require("app/components/charts/components/xAxis"));
var yAxis_1 = tslib_1.__importDefault(require("app/components/charts/components/yAxis"));
var theme_1 = require("app/utils/theme");
/**
 * Size configuration for SLACK_* type charts
 */
exports.slackChartSize = {
    height: 150,
    width: 450,
};
/**
 * Default echarts option config for slack charts
 */
exports.slackChartDefaults = {
    grid: grid_1.default({ left: 5, right: 5, bottom: 5 }),
    backgroundColor: theme_1.lightTheme.background,
    legend: legend_1.default({ theme: theme_1.lightTheme, itemHeight: 6, top: 2, right: 10 }),
    yAxis: yAxis_1.default({ theme: theme_1.lightTheme, splitNumber: 3, axisLabel: { fontSize: 11 } }),
    xAxis: xAxis_1.default({ theme: theme_1.lightTheme, nameGap: 5, isGroupedByDate: true, axisLabel: { fontSize: 11 } }),
};
//# sourceMappingURL=slack.jsx.map