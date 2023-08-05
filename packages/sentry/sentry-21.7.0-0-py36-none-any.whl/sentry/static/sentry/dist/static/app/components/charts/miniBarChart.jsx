Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
// Import to ensure echarts components are loaded.
require("./components/markPoint");
var React = tslib_1.__importStar(require("react"));
var set_1 = tslib_1.__importDefault(require("lodash/set"));
var dates_1 = require("app/utils/dates");
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var barChart_1 = tslib_1.__importDefault(require("./barChart"));
var utils_1 = require("./utils");
var defaultProps = {
    /**
     * Colors to use on the chart.
     */
    colors: [theme_1.default.gray200, theme_1.default.purple300, theme_1.default.purple300],
    /**
     * Show max/min values on yAxis
     */
    labelYAxisExtents: false,
    /**
     * Whether not the series should be stacked.
     *
     * Some of our stats endpoints return data where the 'total' series includes
     * breakdown data (issues). For these results `stacked` should be false.
     * Other endpoints return decomposed results that need to be stacked (outcomes).
     */
    stacked: false,
};
var MiniBarChart = /** @class */ (function (_super) {
    tslib_1.__extends(MiniBarChart, _super);
    function MiniBarChart() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    MiniBarChart.prototype.render = function () {
        var _this = this;
        var _a = this.props, markers = _a.markers, emphasisColors = _a.emphasisColors, colors = _a.colors, _series = _a.series, labelYAxisExtents = _a.labelYAxisExtents, stacked = _a.stacked, series = _a.series, hideDelay = _a.hideDelay, tooltipFormatter = _a.tooltipFormatter, props = tslib_1.__rest(_a, ["markers", "emphasisColors", "colors", "series", "labelYAxisExtents", "stacked", "series", "hideDelay", "tooltipFormatter"]);
        var _ref = props.ref, barChartProps = tslib_1.__rest(props, ["ref"]);
        var chartSeries = [];
        // Ensure bars overlap and that empty values display as we're disabling the axis lines.
        if (series && series.length) {
            chartSeries = series.map(function (original, i) {
                var _a;
                var updated = tslib_1.__assign(tslib_1.__assign({}, original), { cursor: 'normal', type: 'bar' });
                if (i === 0) {
                    updated.barMinHeight = 1;
                    if (stacked === false) {
                        updated.barGap = '-100%';
                    }
                }
                if (stacked) {
                    updated.stack = 'stack1';
                }
                set_1.default(updated, 'itemStyle.color', colors[i]);
                set_1.default(updated, 'itemStyle.opacity', 0.6);
                set_1.default(updated, 'itemStyle.emphasis.opacity', 1.0);
                set_1.default(updated, 'itemStyle.emphasis.color', (_a = emphasisColors === null || emphasisColors === void 0 ? void 0 : emphasisColors[i]) !== null && _a !== void 0 ? _a : colors[i]);
                return updated;
            });
        }
        if (markers) {
            var markerTooltip_1 = {
                show: true,
                trigger: 'item',
                formatter: function (_a) {
                    var _b;
                    var data = _a.data;
                    var time = dates_1.getFormattedDate(data.coord[0], 'MMM D, YYYY LT', {
                        local: !_this.props.utc,
                    });
                    var name = utils_1.truncationFormatter(data.name, (_b = props === null || props === void 0 ? void 0 : props.xAxis) === null || _b === void 0 ? void 0 : _b.truncate);
                    return [
                        '<div class="tooltip-series">',
                        "<div><span class=\"tooltip-label\"><strong>" + name + "</strong></span></div>",
                        '</div>',
                        '<div class="tooltip-date">',
                        time,
                        '</div>',
                        '</div>',
                        '<div class="tooltip-arrow"></div>',
                    ].join('');
                },
            };
            var markPoint = {
                data: markers.map(function (marker) {
                    var _a;
                    return ({
                        name: marker.name,
                        coord: [marker.value, 0],
                        tooltip: markerTooltip_1,
                        symbol: 'circle',
                        symbolSize: (_a = marker.symbolSize) !== null && _a !== void 0 ? _a : 8,
                        itemStyle: {
                            color: marker.color,
                            borderColor: '#ffffff',
                        },
                    });
                }),
            };
            chartSeries[0].markPoint = markPoint;
        }
        var yAxisOptions = labelYAxisExtents
            ? {
                showMinLabel: true,
                showMaxLabel: true,
                interval: Infinity,
            }
            : {
                axisLabel: {
                    show: false,
                },
            };
        var chartOptions = {
            tooltip: {
                trigger: 'axis',
                hideDelay: hideDelay,
                valueFormatter: tooltipFormatter
                    ? function (value) { return tooltipFormatter(value); }
                    : undefined,
            },
            yAxis: tslib_1.__assign({ max: function (value) {
                    // This keeps small datasets from looking 'scary'
                    // by having full bars for < 10 values.
                    return Math.max(10, value.max);
                }, splitLine: {
                    show: false,
                } }, yAxisOptions),
            grid: {
                // Offset to ensure there is room for the marker symbols at the
                // default size.
                top: labelYAxisExtents ? 6 : 0,
                bottom: markers || labelYAxisExtents ? 4 : 0,
                left: markers ? 4 : 0,
                right: markers ? 4 : 0,
            },
            xAxis: {
                axisLine: {
                    show: false,
                },
                axisTick: {
                    show: false,
                    alignWithLabel: true,
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
            },
            options: {
                animation: false,
            },
        };
        return <barChart_1.default series={chartSeries} {...chartOptions} {...barChartProps}/>;
    };
    MiniBarChart.defaultProps = defaultProps;
    return MiniBarChart;
}(React.Component));
exports.default = MiniBarChart;
//# sourceMappingURL=miniBarChart.jsx.map