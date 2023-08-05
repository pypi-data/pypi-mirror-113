Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var react_2 = require("@emotion/react");
var chartZoom_1 = tslib_1.__importDefault(require("app/components/charts/chartZoom"));
var lineChart_1 = tslib_1.__importDefault(require("app/components/charts/lineChart"));
var releaseSeries_1 = tslib_1.__importDefault(require("app/components/charts/releaseSeries"));
var transitionChart_1 = tslib_1.__importDefault(require("app/components/charts/transitionChart"));
var transparentLoadingMask_1 = tslib_1.__importDefault(require("app/components/charts/transparentLoadingMask"));
var getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
var locale_1 = require("app/locale");
var dates_1 = require("app/utils/dates");
var charts_1 = require("app/utils/discover/charts");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var queryString_1 = require("app/utils/queryString");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var releaseChartControls_1 = require("app/views/releases/detail/overview/chart/releaseChartControls");
var utils_1 = require("./utils");
var QUERY_KEYS = [
    'environment',
    'project',
    'query',
    'start',
    'end',
    'statsPeriod',
];
function transformEventStats(data, seriesName) {
    return [
        {
            seriesName: seriesName || 'Current',
            data: data.map(function (_a) {
                var _b = tslib_1.__read(_a, 2), timestamp = _b[0], countsForTimestamp = _b[1];
                return ({
                    name: timestamp * 1000,
                    value: countsForTimestamp.reduce(function (acc, _a) {
                        var count = _a.count;
                        return acc + count;
                    }, 0),
                });
            }),
        },
    ];
}
function getLegend(trendFunction) {
    return {
        right: 10,
        top: 0,
        itemGap: 12,
        align: 'left',
        data: [
            {
                name: 'Baseline',
                icon: 'path://M180 1000 l0 -40 200 0 200 0 0 40 0 40 -200 0 -200 0 0 -40z, M810 1000 l0 -40 200 0 200 0 0 40 0 40 -200 0 -200 0 0 -40zm, M1440 1000 l0 -40 200 0 200 0 0 40 0 40 -200 0 -200 0 0 -40z',
            },
            {
                name: 'Releases',
                icon: 'line',
            },
            {
                name: trendFunction,
                icon: 'line',
            },
        ],
    };
}
function getIntervalLine(theme, series, intervalRatio, transaction) {
    if (!transaction || !series.length || !series[0].data || !series[0].data.length) {
        return [];
    }
    var seriesStart = parseInt(series[0].data[0].name, 0);
    var seriesEnd = parseInt(series[0].data.slice(-1)[0].name, 0);
    if (seriesEnd < seriesStart) {
        return [];
    }
    var periodLine = {
        data: [],
        color: theme.textColor,
        markLine: {
            data: [],
            label: {},
            lineStyle: {
                normal: {
                    color: theme.textColor,
                    type: 'dashed',
                    width: 1,
                },
            },
            symbol: ['none', 'none'],
            tooltip: {
                show: false,
            },
        },
        seriesName: 'Baseline',
    };
    var periodLineLabel = {
        fontSize: 11,
        show: true,
    };
    var previousPeriod = tslib_1.__assign(tslib_1.__assign({}, periodLine), { markLine: tslib_1.__assign({}, periodLine.markLine), seriesName: 'Baseline' });
    var currentPeriod = tslib_1.__assign(tslib_1.__assign({}, periodLine), { markLine: tslib_1.__assign({}, periodLine.markLine), seriesName: 'Baseline' });
    var periodDividingLine = tslib_1.__assign(tslib_1.__assign({}, periodLine), { markLine: tslib_1.__assign({}, periodLine.markLine), seriesName: 'Period split' });
    var seriesDiff = seriesEnd - seriesStart;
    var seriesLine = seriesDiff * intervalRatio + seriesStart;
    previousPeriod.markLine.data = [
        [
            { value: 'Past', coord: [seriesStart, transaction.aggregate_range_1] },
            { coord: [seriesLine, transaction.aggregate_range_1] },
        ],
    ];
    previousPeriod.markLine.tooltip = {
        formatter: function () {
            return [
                '<div class="tooltip-series tooltip-series-solo">',
                '<div>',
                "<span class=\"tooltip-label\"><strong>" + locale_1.t('Past Baseline') + "</strong></span>",
                // p50() coerces the axis to be time based
                charts_1.tooltipFormatter(transaction.aggregate_range_1, 'p50()'),
                '</div>',
                '</div>',
                '<div class="tooltip-arrow"></div>',
            ].join('');
        },
    };
    currentPeriod.markLine.data = [
        [
            { value: 'Present', coord: [seriesLine, transaction.aggregate_range_2] },
            { coord: [seriesEnd, transaction.aggregate_range_2] },
        ],
    ];
    currentPeriod.markLine.tooltip = {
        formatter: function () {
            return [
                '<div class="tooltip-series tooltip-series-solo">',
                '<div>',
                "<span class=\"tooltip-label\"><strong>" + locale_1.t('Present Baseline') + "</strong></span>",
                // p50() coerces the axis to be time based
                charts_1.tooltipFormatter(transaction.aggregate_range_2, 'p50()'),
                '</div>',
                '</div>',
                '<div class="tooltip-arrow"></div>',
            ].join('');
        },
    };
    periodDividingLine.markLine = {
        data: [
            {
                value: 'Previous Period / This Period',
                xAxis: seriesLine,
            },
        ],
        label: { show: false },
        lineStyle: {
            normal: {
                color: theme.textColor,
                type: 'solid',
                width: 2,
            },
        },
        symbol: ['none', 'none'],
        tooltip: {
            show: false,
        },
    };
    previousPeriod.markLine.label = tslib_1.__assign(tslib_1.__assign({}, periodLineLabel), { formatter: 'Past', position: 'insideStartBottom' });
    currentPeriod.markLine.label = tslib_1.__assign(tslib_1.__assign({}, periodLineLabel), { formatter: 'Present', position: 'insideEndBottom' });
    var additionalLineSeries = [previousPeriod, currentPeriod, periodDividingLine];
    return additionalLineSeries;
}
var Chart = /** @class */ (function (_super) {
    tslib_1.__extends(Chart, _super);
    function Chart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleLegendSelectChanged = function (legendChange) {
            var _a = _this.props, location = _a.location, trendChangeType = _a.trendChangeType;
            var selected = legendChange.selected;
            var unselected = Object.keys(selected).filter(function (key) { return !selected[key]; });
            var query = tslib_1.__assign({}, location.query);
            var queryKey = utils_1.getUnselectedSeries(trendChangeType);
            query[queryKey] = unselected;
            var to = tslib_1.__assign(tslib_1.__assign({}, location), { query: query });
            react_router_1.browserHistory.push(to);
        };
        return _this;
    }
    Chart.prototype.render = function () {
        var _this = this;
        var _a, _b;
        var props = this.props;
        var theme = props.theme, trendChangeType = props.trendChangeType, router = props.router, statsPeriod = props.statsPeriod, project = props.project, environment = props.environment, transaction = props.transaction, statsData = props.statsData, isLoading = props.isLoading, location = props.location, projects = props.projects;
        var lineColor = utils_1.trendToColor[trendChangeType || ''];
        var events = statsData && (transaction === null || transaction === void 0 ? void 0 : transaction.project) && (transaction === null || transaction === void 0 ? void 0 : transaction.transaction)
            ? statsData[[transaction.project, transaction.transaction].join(',')]
            : undefined;
        var data = (_a = events === null || events === void 0 ? void 0 : events.data) !== null && _a !== void 0 ? _a : [];
        var trendFunction = utils_1.getCurrentTrendFunction(location);
        var trendParameter = utils_1.getCurrentTrendParameter(location);
        var chartLabel = utils_1.generateTrendFunctionAsString(trendFunction.field, trendParameter.column);
        var results = transformEventStats(data, chartLabel);
        var _c = utils_1.transformEventStatsSmoothed(results, chartLabel), smoothedResults = _c.smoothedResults, minValue = _c.minValue, maxValue = _c.maxValue;
        var start = props.start ? dates_1.getUtcToLocalDateObject(props.start) : null;
        var end = props.end ? dates_1.getUtcToLocalDateObject(props.end) : null;
        var utc = getParams_1.getParams(location.query).utc;
        var seriesSelection = queryString_1.decodeList(location.query[utils_1.getUnselectedSeries(trendChangeType)]).reduce(function (selection, metric) {
            selection[metric] = false;
            return selection;
        }, {});
        var legend = tslib_1.__assign(tslib_1.__assign({}, getLegend(chartLabel)), { selected: seriesSelection });
        var loading = isLoading;
        var reloading = isLoading;
        var transactionProject = parseInt(((_b = projects.find(function (_a) {
            var slug = _a.slug;
            return (transaction === null || transaction === void 0 ? void 0 : transaction.project) === slug;
        })) === null || _b === void 0 ? void 0 : _b.id) || '', 10);
        var yMax = Math.max(maxValue, (transaction === null || transaction === void 0 ? void 0 : transaction.aggregate_range_2) || 0, (transaction === null || transaction === void 0 ? void 0 : transaction.aggregate_range_1) || 0);
        var yMin = Math.min(minValue, (transaction === null || transaction === void 0 ? void 0 : transaction.aggregate_range_1) || Number.MAX_SAFE_INTEGER, (transaction === null || transaction === void 0 ? void 0 : transaction.aggregate_range_2) || Number.MAX_SAFE_INTEGER);
        var yDiff = yMax - yMin;
        var yMargin = yDiff * 0.1;
        var queryExtra = {
            showTransactions: trendChangeType,
            yAxis: releaseChartControls_1.YAxis.COUNT_DURATION,
        };
        var chartOptions = {
            tooltip: {
                valueFormatter: function (value, seriesName) {
                    return charts_1.tooltipFormatter(value, seriesName);
                },
            },
            yAxis: {
                min: Math.max(0, yMin - yMargin),
                max: yMax + yMargin,
                axisLabel: {
                    color: theme.chartLabel,
                    // p50() coerces the axis to be time based
                    formatter: function (value) { return charts_1.axisLabelFormatter(value, 'p50()'); },
                },
            },
        };
        return (<chartZoom_1.default router={router} period={statsPeriod} start={start} end={end} utc={utc === 'true'}>
        {function (zoomRenderProps) {
                var smoothedSeries = smoothedResults
                    ? smoothedResults.map(function (values) {
                        return tslib_1.__assign(tslib_1.__assign({}, values), { color: lineColor.default, lineStyle: {
                                opacity: 1,
                            } });
                    })
                    : [];
                var intervalSeries = getIntervalLine(theme, smoothedResults || [], 0.5, transaction);
                return (<releaseSeries_1.default start={start} end={end} queryExtra={queryExtra} period={statsPeriod} utc={utc === 'true'} projects={isNaN(transactionProject) ? project : [transactionProject]} environments={environment} memoized>
              {function (_a) {
                        var releaseSeries = _a.releaseSeries;
                        return (<transitionChart_1.default loading={loading} reloading={reloading}>
                  <transparentLoadingMask_1.default visible={reloading}/>
                  {getDynamicText_1.default({
                                value: (<lineChart_1.default {...zoomRenderProps} {...chartOptions} onLegendSelectChanged={_this.handleLegendSelectChanged} series={tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(smoothedSeries)), tslib_1.__read(releaseSeries)), tslib_1.__read(intervalSeries))} seriesOptions={{
                                        showSymbol: false,
                                    }} legend={legend} toolBox={{
                                        show: false,
                                    }} grid={{
                                        left: '10px',
                                        right: '10px',
                                        top: '40px',
                                        bottom: '0px',
                                    }}/>),
                                fixed: 'Duration Chart',
                            })}
                </transitionChart_1.default>);
                    }}
            </releaseSeries_1.default>);
            }}
      </chartZoom_1.default>);
    };
    return Chart;
}(react_1.Component));
exports.default = react_2.withTheme(withApi_1.default(react_router_1.withRouter(Chart)));
//# sourceMappingURL=chart.jsx.map