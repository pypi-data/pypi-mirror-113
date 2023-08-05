Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_2 = require("@emotion/react");
var max_1 = tslib_1.__importDefault(require("lodash/max"));
var min_1 = tslib_1.__importDefault(require("lodash/min"));
var areaChart_1 = tslib_1.__importDefault(require("app/components/charts/areaChart"));
var chartZoom_1 = tslib_1.__importDefault(require("app/components/charts/chartZoom"));
var charts_1 = require("app/utils/discover/charts");
var fields_1 = require("app/utils/discover/fields");
// adapted from https://stackoverflow.com/questions/11397239/rounding-up-for-a-graph-maximum
function computeAxisMax(data) {
    // assumes min is 0
    var valuesDict = data.map(function (value) { return value.data.map(function (point) { return point.value; }); });
    var maxValue = max_1.default(valuesDict.map(max_1.default));
    if (maxValue <= 1) {
        return 1;
    }
    var power = Math.log10(maxValue);
    var magnitude = min_1.default([max_1.default([Math.pow(10, (power - Math.floor(power))), 0]), 10]);
    var scale;
    if (magnitude <= 2.5) {
        scale = 0.2;
    }
    else if (magnitude <= 5) {
        scale = 0.5;
    }
    else if (magnitude <= 7.5) {
        scale = 1.0;
    }
    else {
        scale = 2.0;
    }
    var step = Math.pow(10, Math.floor(power)) * scale;
    return Math.round(Math.ceil(maxValue / step) * step);
}
var Chart = /** @class */ (function (_super) {
    tslib_1.__extends(Chart, _super);
    function Chart() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Chart.prototype.render = function () {
        var _a = this.props, theme = _a.theme, data = _a.data, router = _a.router, statsPeriod = _a.statsPeriod, start = _a.start, end = _a.end, utc = _a.utc, loading = _a.loading, height = _a.height, grid = _a.grid, disableMultiAxis = _a.disableMultiAxis;
        if (!data || data.length <= 0) {
            return null;
        }
        var colors = theme.charts.getColorPalette(4);
        var durationOnly = data.every(function (value) { return fields_1.aggregateOutputType(value.seriesName) === 'duration'; });
        var dataMax = durationOnly ? computeAxisMax(data) : undefined;
        var xAxes = disableMultiAxis
            ? undefined
            : [
                {
                    gridIndex: 0,
                    type: 'time',
                },
                {
                    gridIndex: 1,
                    type: 'time',
                },
            ];
        var yAxes = disableMultiAxis
            ? [
                {
                    axisLabel: {
                        color: theme.chartLabel,
                        formatter: function (value) {
                            return charts_1.axisLabelFormatter(value, data[0].seriesName);
                        },
                    },
                },
            ]
            : [
                {
                    gridIndex: 0,
                    scale: true,
                    max: dataMax,
                    axisLabel: {
                        color: theme.chartLabel,
                        formatter: function (value) {
                            return charts_1.axisLabelFormatter(value, data[0].seriesName);
                        },
                    },
                },
                {
                    gridIndex: 1,
                    scale: true,
                    max: dataMax,
                    axisLabel: {
                        color: theme.chartLabel,
                        formatter: function (value) {
                            return charts_1.axisLabelFormatter(value, data[1].seriesName);
                        },
                    },
                },
            ];
        var axisPointer = disableMultiAxis
            ? undefined
            : {
                // Link the two series x-axis together.
                link: [{ xAxisIndex: [0, 1] }],
            };
        var areaChartProps = {
            seriesOptions: {
                showSymbol: false,
            },
            grid: disableMultiAxis
                ? grid
                : [
                    {
                        top: '8px',
                        left: '24px',
                        right: '52%',
                        bottom: '16px',
                    },
                    {
                        top: '8px',
                        left: '52%',
                        right: '24px',
                        bottom: '16px',
                    },
                ],
            axisPointer: axisPointer,
            xAxes: xAxes,
            yAxes: yAxes,
            utc: utc,
            isGroupedByDate: true,
            showTimeInTooltip: true,
            colors: [colors[0], colors[1]],
            tooltip: {
                valueFormatter: function (value, seriesName) {
                    return charts_1.tooltipFormatter(value, seriesName);
                },
                nameFormatter: function (value) {
                    return value === 'epm()' ? 'tpm()' : value;
                },
            },
        };
        if (loading) {
            return <areaChart_1.default height={height} series={[]} {...areaChartProps}/>;
        }
        var series = data.map(function (values, i) { return (tslib_1.__assign(tslib_1.__assign({}, values), { yAxisIndex: i, xAxisIndex: i })); });
        return (<chartZoom_1.default router={router} period={statsPeriod} start={start} end={end} utc={utc} xAxisIndex={disableMultiAxis ? undefined : [0, 1]}>
        {function (zoomRenderProps) { return (<areaChart_1.default height={height} {...zoomRenderProps} series={series} {...areaChartProps}/>); }}
      </chartZoom_1.default>);
    };
    return Chart;
}(react_1.Component));
exports.default = react_2.withTheme(Chart);
//# sourceMappingURL=chart.jsx.map