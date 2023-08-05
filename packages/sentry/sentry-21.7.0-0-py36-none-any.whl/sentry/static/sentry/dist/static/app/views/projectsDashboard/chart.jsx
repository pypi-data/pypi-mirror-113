Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var baseChart_1 = tslib_1.__importDefault(require("app/components/charts/baseChart"));
var locale_1 = require("app/locale");
var charts_1 = require("app/utils/discover/charts");
var noEvents_1 = tslib_1.__importDefault(require("./noEvents"));
var Chart = function (_a) {
    var theme = _a.theme, firstEvent = _a.firstEvent, stats = _a.stats, transactionStats = _a.transactionStats;
    var series = [];
    var hasTransactions = transactionStats !== undefined;
    if (transactionStats) {
        var transactionSeries = transactionStats.map(function (_a) {
            var _b = tslib_1.__read(_a, 2), timestamp = _b[0], value = _b[1];
            return [
                timestamp * 1000,
                value,
            ];
        });
        series.push({
            cursor: 'normal',
            name: locale_1.t('Transactions'),
            type: 'bar',
            data: transactionSeries,
            barMinHeight: 1,
            xAxisIndex: 1,
            yAxisIndex: 1,
            itemStyle: {
                color: theme.gray200,
                opacity: 0.8,
                emphasis: {
                    color: theme.gray200,
                    opacity: 1.0,
                },
            },
        });
    }
    if (stats) {
        series.push({
            cursor: 'normal',
            name: locale_1.t('Errors'),
            type: 'bar',
            data: stats.map(function (_a) {
                var _b = tslib_1.__read(_a, 2), timestamp = _b[0], value = _b[1];
                return [timestamp * 1000, value];
            }),
            barMinHeight: 1,
            xAxisIndex: 0,
            yAxisIndex: 0,
            itemStyle: {
                color: theme.purple300,
                opacity: 0.6,
                emphasis: {
                    color: theme.purple300,
                    opacity: 0.8,
                },
            },
        });
    }
    var grid = hasTransactions
        ? [
            {
                top: 10,
                bottom: 60,
                left: 2,
                right: 2,
            },
            {
                top: 105,
                bottom: 0,
                left: 2,
                right: 2,
            },
        ]
        : [
            {
                top: 10,
                bottom: 0,
                left: 2,
                right: 2,
            },
        ];
    var chartOptions = {
        series: series,
        colors: [],
        height: 150,
        isGroupedByDate: true,
        showTimeInTooltip: true,
        grid: grid,
        tooltip: {
            trigger: 'axis',
        },
        xAxes: Array.from(new Array(series.length)).map(function (_i, index) { return ({
            gridIndex: index,
            boundaryGap: true,
            axisLine: {
                show: false,
            },
            axisTick: {
                show: false,
            },
            axisLabel: {
                show: false,
            },
            axisPointer: {
                type: 'line',
                label: {
                    show: false,
                },
                lineStyle: {
                    width: 0,
                },
            },
        }); }),
        yAxes: Array.from(new Array(series.length)).map(function (_i, index) { return ({
            gridIndex: index,
            interval: Infinity,
            max: function (value) {
                // This keeps small datasets from looking 'scary'
                // by having full bars for < 10 values.
                return Math.max(10, value.max);
            },
            axisLabel: {
                margin: 2,
                showMaxLabel: true,
                showMinLabel: false,
                color: theme.chartLabel,
                fontFamily: theme.text.family,
                inside: true,
                lineHeight: 12,
                formatter: function (value) { return charts_1.axisLabelFormatter(value, 'count()', true); },
                textBorderColor: theme.backgroundSecondary,
                textBorderWidth: 1,
            },
            splitLine: {
                show: false,
            },
            zlevel: theme.zIndex.header,
        }); }),
        axisPointer: {
            // Link each x-axis together.
            link: [{ xAxisIndex: [0, 1] }],
        },
        options: {
            animation: false,
        },
    };
    return (<React.Fragment>
      <baseChart_1.default {...chartOptions}/>
      {!firstEvent && <noEvents_1.default seriesCount={series.length}/>}
    </React.Fragment>);
};
exports.default = react_1.withTheme(Chart);
//# sourceMappingURL=chart.jsx.map