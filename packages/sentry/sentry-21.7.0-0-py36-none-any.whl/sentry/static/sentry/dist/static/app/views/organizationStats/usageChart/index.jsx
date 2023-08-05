Object.defineProperty(exports, "__esModule", { value: true });
exports.UsageChart = exports.SeriesTypes = exports.CHART_OPTIONS_DATA_TRANSFORM = exports.ChartDataTransform = exports.CHART_OPTIONS_DATACATEGORY = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var color_1 = tslib_1.__importDefault(require("color"));
var baseChart_1 = tslib_1.__importDefault(require("app/components/charts/baseChart"));
var legend_1 = tslib_1.__importDefault(require("app/components/charts/components/legend"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/charts/components/tooltip"));
var xAxis_1 = tslib_1.__importDefault(require("app/components/charts/components/xAxis"));
var barSeries_1 = tslib_1.__importDefault(require("app/components/charts/series/barSeries"));
var styles_1 = require("app/components/charts/styles");
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var panel_1 = tslib_1.__importDefault(require("app/components/panels/panel"));
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var types_1 = require("app/types");
var dates_1 = require("app/utils/dates");
var formatters_1 = require("app/utils/formatters");
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var utils_1 = require("../utils");
var utils_2 = require("./utils");
var COLOR_ERRORS = color_1.default(theme_1.default.dataCategory.errors).lighten(0.25).string();
var COLOR_TRANSACTIONS = color_1.default(theme_1.default.dataCategory.transactions)
    .lighten(0.35)
    .string();
var COLOR_ATTACHMENTS = color_1.default(theme_1.default.dataCategory.attachments)
    .lighten(0.65)
    .string();
var COLOR_DROPPED = theme_1.default.red300;
var COLOR_PROJECTED = theme_1.default.gray100;
var COLOR_FILTERED = theme_1.default.pink100;
exports.CHART_OPTIONS_DATACATEGORY = [
    {
        label: types_1.DataCategoryName[types_1.DataCategory.ERRORS],
        value: types_1.DataCategory.ERRORS,
        disabled: false,
    },
    {
        label: types_1.DataCategoryName[types_1.DataCategory.TRANSACTIONS],
        value: types_1.DataCategory.TRANSACTIONS,
        disabled: false,
    },
    {
        label: types_1.DataCategoryName[types_1.DataCategory.ATTACHMENTS],
        value: types_1.DataCategory.ATTACHMENTS,
        disabled: false,
    },
];
var ChartDataTransform;
(function (ChartDataTransform) {
    ChartDataTransform["CUMULATIVE"] = "cumulative";
    ChartDataTransform["PERIODIC"] = "periodic";
})(ChartDataTransform = exports.ChartDataTransform || (exports.ChartDataTransform = {}));
exports.CHART_OPTIONS_DATA_TRANSFORM = [
    {
        label: locale_1.t('Cumulative'),
        value: ChartDataTransform.CUMULATIVE,
        disabled: false,
    },
    {
        label: locale_1.t('Periodic'),
        value: ChartDataTransform.PERIODIC,
        disabled: false,
    },
];
var SeriesTypes;
(function (SeriesTypes) {
    SeriesTypes["ACCEPTED"] = "Accepted";
    SeriesTypes["DROPPED"] = "Dropped";
    SeriesTypes["PROJECTED"] = "Projected";
    SeriesTypes["FILTERED"] = "Filtered";
})(SeriesTypes = exports.SeriesTypes || (exports.SeriesTypes = {}));
var UsageChart = /** @class */ (function (_super) {
    tslib_1.__extends(UsageChart, _super);
    function UsageChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            xAxisDates: [],
        };
        return _this;
    }
    /**
     * UsageChart needs to generate the X-Axis dates as props.usageStats may
     * not pass the complete range of X-Axis data points
     *
     * E.g. usageStats.accepted covers day 1-15 of a month, usageStats.projected
     * either covers day 16-30 or may not be available at all.
     */
    UsageChart.getDerivedStateFromProps = function (nextProps, prevState) {
        var usageDateStart = nextProps.usageDateStart, usageDateEnd = nextProps.usageDateEnd, usageDateShowUtc = nextProps.usageDateShowUtc, usageDateInterval = nextProps.usageDateInterval;
        return tslib_1.__assign(tslib_1.__assign({}, prevState), { xAxisDates: utils_2.getXAxisDates(usageDateStart, usageDateEnd, usageDateShowUtc, usageDateInterval) });
    };
    Object.defineProperty(UsageChart.prototype, "chartColors", {
        get: function () {
            var dataCategory = this.props.dataCategory;
            if (dataCategory === types_1.DataCategory.ERRORS) {
                return [COLOR_ERRORS, COLOR_FILTERED, COLOR_DROPPED, COLOR_PROJECTED];
            }
            if (dataCategory === types_1.DataCategory.ATTACHMENTS) {
                return [COLOR_ATTACHMENTS, COLOR_FILTERED, COLOR_DROPPED, COLOR_PROJECTED];
            }
            return [COLOR_TRANSACTIONS, COLOR_FILTERED, COLOR_DROPPED, COLOR_PROJECTED];
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(UsageChart.prototype, "chartMetadata", {
        get: function () {
            var _a = this.props, usageDateStart = _a.usageDateStart, usageDateEnd = _a.usageDateEnd;
            var _b = this.props, usageDateInterval = _b.usageDateInterval, usageStats = _b.usageStats, dataCategory = _b.dataCategory, dataTransform = _b.dataTransform, handleDataTransformation = _b.handleDataTransformation;
            var xAxisDates = this.state.xAxisDates;
            var selectDataCategory = exports.CHART_OPTIONS_DATACATEGORY.find(function (o) { return o.value === dataCategory; });
            if (!selectDataCategory) {
                throw new Error('Selected item is not supported');
            }
            // Do not assume that handleDataTransformation is a pure function
            var chartData = tslib_1.__assign({}, handleDataTransformation(usageStats, dataTransform));
            Object.keys(chartData).forEach(function (k) {
                var isProjected = k === SeriesTypes.PROJECTED;
                // Map the array and destructure elements to avoid side-effects
                chartData[k] = chartData[k].map(function (stat) {
                    return tslib_1.__assign(tslib_1.__assign({}, stat), { tooltip: { show: false }, itemStyle: { opacity: isProjected ? 0.6 : 1 } });
                });
            });
            // Use hours as common units
            var dataPeriod = dates_1.statsPeriodToDays(undefined, usageDateStart, usageDateEnd) * 24;
            var barPeriod = dates_1.parsePeriodToHours(usageDateInterval);
            if (dataPeriod < 0 || barPeriod < 0) {
                throw new Error('UsageChart: Unable to parse data time period');
            }
            var _c = utils_2.getXAxisLabelInterval(dataPeriod, dataPeriod / barPeriod), xAxisTickInterval = _c.xAxisTickInterval, xAxisLabelInterval = _c.xAxisLabelInterval;
            var label = selectDataCategory.label, value = selectDataCategory.value;
            if (value === types_1.DataCategory.ERRORS || value === types_1.DataCategory.TRANSACTIONS) {
                return {
                    chartLabel: label,
                    chartData: chartData,
                    xAxisData: xAxisDates,
                    xAxisTickInterval: xAxisTickInterval,
                    xAxisLabelInterval: xAxisLabelInterval,
                    yAxisMinInterval: 100,
                    yAxisFormatter: formatters_1.formatAbbreviatedNumber,
                    tooltipValueFormatter: utils_2.getTooltipFormatter(dataCategory),
                };
            }
            return {
                chartLabel: label,
                chartData: chartData,
                xAxisData: xAxisDates,
                xAxisTickInterval: xAxisTickInterval,
                xAxisLabelInterval: xAxisLabelInterval,
                yAxisMinInterval: 0.5 * utils_1.GIGABYTE,
                yAxisFormatter: function (val) {
                    return utils_1.formatUsageWithUnits(val, types_1.DataCategory.ATTACHMENTS, {
                        isAbbreviated: true,
                        useUnitScaling: true,
                    });
                },
                tooltipValueFormatter: utils_2.getTooltipFormatter(dataCategory),
            };
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(UsageChart.prototype, "chartSeries", {
        get: function () {
            var chartSeries = this.props.chartSeries;
            var chartData = this.chartMetadata.chartData;
            var series = [
                barSeries_1.default({
                    name: SeriesTypes.ACCEPTED,
                    data: chartData.accepted,
                    barMinHeight: 1,
                    stack: 'usage',
                    legendHoverLink: false,
                }),
                barSeries_1.default({
                    name: SeriesTypes.FILTERED,
                    data: chartData.filtered,
                    barMinHeight: 1,
                    stack: 'usage',
                    legendHoverLink: false,
                }),
                barSeries_1.default({
                    name: SeriesTypes.DROPPED,
                    data: chartData.dropped,
                    stack: 'usage',
                    legendHoverLink: false,
                }),
                barSeries_1.default({
                    name: SeriesTypes.PROJECTED,
                    data: chartData.projected,
                    barMinHeight: 1,
                    stack: 'usage',
                    legendHoverLink: false,
                }),
            ];
            // Additional series passed by parent component
            if (chartSeries) {
                series = series.concat(chartSeries);
            }
            return series;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(UsageChart.prototype, "chartLegend", {
        get: function () {
            var chartData = this.chartMetadata.chartData;
            var legend = [
                {
                    name: SeriesTypes.ACCEPTED,
                },
            ];
            if (chartData.filtered && chartData.filtered.length > 0) {
                legend.push({
                    name: SeriesTypes.FILTERED,
                });
            }
            if (chartData.dropped.length > 0) {
                legend.push({
                    name: SeriesTypes.DROPPED,
                });
            }
            if (chartData.projected.length > 0) {
                legend.push({
                    name: SeriesTypes.PROJECTED,
                });
            }
            return legend;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(UsageChart.prototype, "chartTooltip", {
        get: function () {
            var chartTooltip = this.props.chartTooltip;
            if (chartTooltip) {
                return chartTooltip;
            }
            var tooltipValueFormatter = this.chartMetadata.tooltipValueFormatter;
            return tooltip_1.default({
                // Trigger to axis prevents tooltip from redrawing when hovering
                // over individual bars
                trigger: 'axis',
                valueFormatter: tooltipValueFormatter,
            });
        },
        enumerable: false,
        configurable: true
    });
    UsageChart.prototype.renderChart = function () {
        var _a = this.props, theme = _a.theme, title = _a.title, isLoading = _a.isLoading, isError = _a.isError, errors = _a.errors;
        if (isLoading) {
            return (<placeholder_1.default height="200px">
          <loadingIndicator_1.default mini/>
        </placeholder_1.default>);
        }
        if (isError) {
            return (<placeholder_1.default height="200px">
          <icons_1.IconWarning size={theme.fontSizeExtraLarge}/>
          <ErrorMessages>
            {errors &&
                    Object.keys(errors).map(function (k) { var _a; return <span key={k}>{(_a = errors[k]) === null || _a === void 0 ? void 0 : _a.message}</span>; })}
          </ErrorMessages>
        </placeholder_1.default>);
        }
        var _b = this.chartMetadata, xAxisData = _b.xAxisData, xAxisTickInterval = _b.xAxisTickInterval, xAxisLabelInterval = _b.xAxisLabelInterval, yAxisMinInterval = _b.yAxisMinInterval, yAxisFormatter = _b.yAxisFormatter;
        return (<React.Fragment>
        <styles_1.HeaderTitleLegend>{title || locale_1.t('Current Usage Period')}</styles_1.HeaderTitleLegend>
        <baseChart_1.default colors={this.chartColors} grid={{ bottom: '3px', left: '0px', right: '10px', top: '40px' }} xAxis={xAxis_1.default({
                show: true,
                type: 'category',
                name: 'Date',
                boundaryGap: true,
                data: xAxisData,
                axisTick: {
                    interval: xAxisTickInterval,
                    alignWithLabel: true,
                },
                axisLabel: {
                    interval: xAxisLabelInterval,
                    formatter: function (label) { return label.slice(0, 6); }, // Limit label to 6 chars
                },
                theme: theme,
            })} yAxis={{
                min: 0,
                minInterval: yAxisMinInterval,
                axisLabel: {
                    formatter: yAxisFormatter,
                    color: theme.chartLabel,
                },
            }} series={this.chartSeries} tooltip={this.chartTooltip} onLegendSelectChanged={function () { }} legend={legend_1.default({
                right: 10,
                top: 5,
                data: this.chartLegend,
                theme: theme,
            })}/>
      </React.Fragment>);
    };
    UsageChart.prototype.render = function () {
        var footer = this.props.footer;
        return (<panel_1.default id="usage-chart">
        <styles_1.ChartContainer>{this.renderChart()}</styles_1.ChartContainer>
        {footer}
      </panel_1.default>);
    };
    UsageChart.defaultProps = {
        usageDateShowUtc: true,
        usageDateInterval: '1d',
        handleDataTransformation: function (stats, transform) {
            var chartData = {
                accepted: [],
                dropped: [],
                projected: [],
                filtered: [],
            };
            var isCumulative = transform === ChartDataTransform.CUMULATIVE;
            Object.keys(stats).forEach(function (k) {
                var count = 0;
                chartData[k] = stats[k].map(function (stat) {
                    var _a = tslib_1.__read(stat.value, 2), x = _a[0], y = _a[1];
                    count = isCumulative ? count + y : y;
                    return tslib_1.__assign(tslib_1.__assign({}, stat), { value: [x, count] });
                });
            });
            return chartData;
        },
    };
    return UsageChart;
}(React.Component));
exports.UsageChart = UsageChart;
exports.default = react_1.withTheme(UsageChart);
var ErrorMessages = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n\n  margin-top: ", ";\n  font-size: ", ";\n"], ["\n  display: flex;\n  flex-direction: column;\n\n  margin-top: ", ";\n  font-size: ", ";\n"])), space_1.default(1), function (p) { return p.theme.fontSizeSmall; });
var templateObject_1;
//# sourceMappingURL=index.jsx.map