Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var ReactRouter = tslib_1.__importStar(require("react-router"));
var react_2 = require("@emotion/react");
var chartZoom_1 = tslib_1.__importDefault(require("app/components/charts/chartZoom"));
var markLine_1 = tslib_1.__importDefault(require("app/components/charts/components/markLine"));
var errorPanel_1 = tslib_1.__importDefault(require("app/components/charts/errorPanel"));
var eventsRequest_1 = tslib_1.__importDefault(require("app/components/charts/eventsRequest"));
var lineChart_1 = tslib_1.__importDefault(require("app/components/charts/lineChart"));
var releaseSeries_1 = tslib_1.__importDefault(require("app/components/charts/releaseSeries"));
var styles_1 = require("app/components/charts/styles");
var transitionChart_1 = tslib_1.__importDefault(require("app/components/charts/transitionChart"));
var transparentLoadingMask_1 = tslib_1.__importDefault(require("app/components/charts/transparentLoadingMask"));
var utils_1 = require("app/components/charts/utils");
var panels_1 = require("app/components/panels");
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var dates_1 = require("app/utils/dates");
var charts_1 = require("app/utils/discover/charts");
var fields_1 = require("app/utils/discover/fields");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var queryString_1 = require("app/utils/queryString");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var utils_2 = require("../trends/utils");
var utils_3 = require("./utils");
var QUERY_KEYS = [
    'environment',
    'project',
    'query',
    'start',
    'end',
    'statsPeriod',
];
var VitalChart = /** @class */ (function (_super) {
    tslib_1.__extends(VitalChart, _super);
    function VitalChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleLegendSelectChanged = function (legendChange) {
            var location = _this.props.location;
            var selected = legendChange.selected;
            var unselected = Object.keys(selected).filter(function (key) { return !selected[key]; });
            var to = tslib_1.__assign(tslib_1.__assign({}, location), { query: tslib_1.__assign(tslib_1.__assign({}, location.query), { unselectedSeries: unselected }) });
            react_router_1.browserHistory.push(to);
        };
        return _this;
    }
    VitalChart.prototype.render = function () {
        var _this = this;
        var _a = this.props, theme = _a.theme, api = _a.api, project = _a.project, environment = _a.environment, location = _a.location, organization = _a.organization, query = _a.query, statsPeriod = _a.statsPeriod, router = _a.router;
        var start = this.props.start ? dates_1.getUtcToLocalDateObject(this.props.start) : null;
        var end = this.props.end ? dates_1.getUtcToLocalDateObject(this.props.end) : null;
        var utc = queryString_1.decodeScalar(router.location.query.utc) !== 'false';
        var vitalName = utils_3.vitalNameFromLocation(location);
        var yAxis = "p75(" + vitalName + ")";
        var legend = {
            right: 10,
            top: 0,
            selected: utils_1.getSeriesSelection(location),
        };
        var datetimeSelection = {
            start: start,
            end: end,
            period: statsPeriod,
        };
        var vitalPoor = utils_3.webVitalPoor[vitalName];
        var vitalMeh = utils_3.webVitalMeh[vitalName];
        var markLines = [
            {
                seriesName: 'Thresholds',
                type: 'line',
                data: [],
                markLine: markLine_1.default({
                    silent: true,
                    lineStyle: {
                        color: theme.red300,
                        type: 'dashed',
                        width: 1.5,
                    },
                    label: {
                        show: true,
                        position: 'insideEndTop',
                        formatter: locale_1.t('Poor'),
                    },
                    data: [
                        {
                            yAxis: vitalPoor,
                        },
                    ],
                }),
            },
            {
                seriesName: 'Thresholds',
                type: 'line',
                data: [],
                markLine: markLine_1.default({
                    silent: true,
                    lineStyle: {
                        color: theme.yellow300,
                        type: 'dashed',
                        width: 1.5,
                    },
                    label: {
                        show: true,
                        position: 'insideEndTop',
                        formatter: locale_1.t('Meh'),
                    },
                    data: [
                        {
                            yAxis: vitalMeh,
                        },
                    ],
                }),
            },
        ];
        var chartOptions = {
            grid: {
                left: '5px',
                right: '10px',
                top: '35px',
                bottom: '0px',
            },
            seriesOptions: {
                showSymbol: false,
            },
            tooltip: {
                trigger: 'axis',
                valueFormatter: function (value, seriesName) {
                    return charts_1.tooltipFormatter(value, vitalName === fields_1.WebVital.CLS ? seriesName : yAxis);
                },
            },
            yAxis: {
                min: 0,
                max: vitalPoor,
                axisLabel: {
                    color: theme.chartLabel,
                    showMaxLabel: false,
                    // coerces the axis to be time based
                    formatter: function (value) { return charts_1.axisLabelFormatter(value, yAxis); },
                },
            },
        };
        return (<panels_1.Panel>
        <styles_1.ChartContainer>
          <styles_1.HeaderTitleLegend>
            {locale_1.t('Duration p75')}
            <questionTooltip_1.default size="sm" position="top" title={locale_1.t("The durations shown should fall under the vital threshold.")}/>
          </styles_1.HeaderTitleLegend>
          <chartZoom_1.default router={router} period={statsPeriod} start={start} end={end} utc={utc}>
            {function (zoomRenderProps) { return (<eventsRequest_1.default api={api} organization={organization} period={statsPeriod} project={project} environment={environment} start={start} end={end} interval={utils_1.getInterval(datetimeSelection, true)} showLoading={false} query={query} includePrevious={false} yAxis={[yAxis]} partial>
                {function (_a) {
                    var results = _a.timeseriesData, errored = _a.errored, loading = _a.loading, reloading = _a.reloading;
                    if (errored) {
                        return (<errorPanel_1.default>
                        <icons_1.IconWarning color="gray500" size="lg"/>
                      </errorPanel_1.default>);
                    }
                    var colors = (results && theme.charts.getColorPalette(results.length - 2)) || [];
                    var smoothedResults = utils_2.transformEventStatsSmoothed(results).smoothedResults;
                    var smoothedSeries = smoothedResults
                        ? smoothedResults.map(function (_a, i) {
                            var seriesName = _a.seriesName, rest = tslib_1.__rest(_a, ["seriesName"]);
                            return tslib_1.__assign(tslib_1.__assign({ seriesName: utils_2.replaceSeriesName(seriesName) || 'p75' }, rest), { color: colors[i], lineStyle: {
                                    opacity: 1,
                                    width: 2,
                                } });
                        })
                        : [];
                    var seriesMax = utils_3.getMaxOfSeries(smoothedSeries);
                    var yAxisMax = Math.max(seriesMax, vitalPoor);
                    chartOptions.yAxis.max = yAxisMax * 1.1;
                    return (<releaseSeries_1.default start={start} end={end} period={statsPeriod} utc={utc} projects={project} environments={environment}>
                      {function (_a) {
                            var releaseSeries = _a.releaseSeries;
                            return (<transitionChart_1.default loading={loading} reloading={reloading}>
                          <transparentLoadingMask_1.default visible={reloading}/>
                          {getDynamicText_1.default({
                                    value: (<lineChart_1.default {...zoomRenderProps} {...chartOptions} legend={legend} onLegendSelectChanged={_this.handleLegendSelectChanged} series={tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(markLines)), tslib_1.__read(releaseSeries)), tslib_1.__read(smoothedSeries))}/>),
                                    fixed: 'Web Vitals Chart',
                                })}
                        </transitionChart_1.default>);
                        }}
                    </releaseSeries_1.default>);
                }}
              </eventsRequest_1.default>); }}
          </chartZoom_1.default>
        </styles_1.ChartContainer>
      </panels_1.Panel>);
    };
    return VitalChart;
}(react_1.Component));
exports.default = withApi_1.default(react_2.withTheme(ReactRouter.withRouter(VitalChart)));
//# sourceMappingURL=vitalChart.jsx.map