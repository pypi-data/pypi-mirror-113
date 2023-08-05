Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var ReactRouter = tslib_1.__importStar(require("react-router"));
var react_2 = require("@emotion/react");
var chartZoom_1 = tslib_1.__importDefault(require("app/components/charts/chartZoom"));
var errorPanel_1 = tslib_1.__importDefault(require("app/components/charts/errorPanel"));
var eventsRequest_1 = tslib_1.__importDefault(require("app/components/charts/eventsRequest"));
var lineChart_1 = tslib_1.__importDefault(require("app/components/charts/lineChart"));
var releaseSeries_1 = tslib_1.__importDefault(require("app/components/charts/releaseSeries"));
var styles_1 = require("app/components/charts/styles");
var transitionChart_1 = tslib_1.__importDefault(require("app/components/charts/transitionChart"));
var transparentLoadingMask_1 = tslib_1.__importDefault(require("app/components/charts/transparentLoadingMask"));
var utils_1 = require("app/components/charts/utils");
var getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var dates_1 = require("app/utils/dates");
var charts_1 = require("app/utils/discover/charts");
var fields_1 = require("app/utils/discover/fields");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var overview_1 = require("app/views/releases/detail/overview");
var QUERY_KEYS = [
    'environment',
    'project',
    'query',
    'start',
    'end',
    'statsPeriod',
];
var YAXIS_VALUES = [
    'p75(measurements.fp)',
    'p75(measurements.fcp)',
    'p75(measurements.lcp)',
    'p75(measurements.fid)',
];
var VitalsChart = /** @class */ (function (_super) {
    tslib_1.__extends(VitalsChart, _super);
    function VitalsChart() {
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
    VitalsChart.prototype.render = function () {
        var _this = this;
        var _a = this.props, theme = _a.theme, api = _a.api, project = _a.project, environment = _a.environment, location = _a.location, organization = _a.organization, query = _a.query, statsPeriod = _a.statsPeriod, router = _a.router, queryExtra = _a.queryExtra;
        var start = this.props.start ? dates_1.getUtcToLocalDateObject(this.props.start) : null;
        var end = this.props.end ? dates_1.getUtcToLocalDateObject(this.props.end) : null;
        var utc = getParams_1.getParams(location.query).utc;
        var legend = {
            right: 10,
            top: 0,
            selected: utils_1.getSeriesSelection(location),
            formatter: function (seriesName) {
                var arg = fields_1.getAggregateArg(seriesName);
                if (arg !== null) {
                    var slug = fields_1.getMeasurementSlug(arg);
                    if (slug !== null) {
                        seriesName = slug.toUpperCase();
                    }
                }
                return seriesName;
            },
        };
        var datetimeSelection = {
            start: start,
            end: end,
            period: statsPeriod,
        };
        var chartOptions = {
            grid: {
                left: '10px',
                right: '10px',
                top: '40px',
                bottom: '0px',
            },
            seriesOptions: {
                showSymbol: false,
            },
            tooltip: {
                trigger: 'axis',
                valueFormatter: charts_1.tooltipFormatter,
            },
            yAxis: {
                axisLabel: {
                    color: theme.chartLabel,
                    // p75(measurements.fcp) coerces the axis to be time based
                    formatter: function (value) {
                        return charts_1.axisLabelFormatter(value, 'p75(measurements.fcp)');
                    },
                },
            },
        };
        return (<react_1.Fragment>
        <styles_1.HeaderTitleLegend>
          {locale_1.t('Web Vitals Breakdown')}
          <questionTooltip_1.default size="sm" position="top" title={locale_1.t("Web Vitals Breakdown reflects the 75th percentile of web vitals over time.")}/>
        </styles_1.HeaderTitleLegend>
        <chartZoom_1.default router={router} period={statsPeriod} start={start} end={end} utc={utc === 'true'}>
          {function (zoomRenderProps) { return (<eventsRequest_1.default api={api} organization={organization} period={statsPeriod} project={project} environment={environment} start={start} end={end} interval={utils_1.getInterval(datetimeSelection, true)} showLoading={false} query={query} includePrevious={false} yAxis={YAXIS_VALUES} partial>
              {function (_a) {
                    var results = _a.results, errored = _a.errored, loading = _a.loading, reloading = _a.reloading;
                    if (errored) {
                        return (<errorPanel_1.default>
                      <icons_1.IconWarning color="gray500" size="lg"/>
                    </errorPanel_1.default>);
                    }
                    var colors = (results && theme.charts.getColorPalette(results.length - 2)) || [];
                    // Create a list of series based on the order of the fields,
                    var series = results
                        ? results.map(function (values, i) { return (tslib_1.__assign(tslib_1.__assign({}, values), { color: colors[i] })); })
                        : [];
                    return (<releaseSeries_1.default start={start} end={end} queryExtra={tslib_1.__assign(tslib_1.__assign({}, queryExtra), { showTransactions: overview_1.TransactionsListOption.SLOW_LCP })} period={statsPeriod} utc={utc === 'true'} projects={project} environments={environment}>
                    {function (_a) {
                            var releaseSeries = _a.releaseSeries;
                            return (<transitionChart_1.default loading={loading} reloading={reloading}>
                        <transparentLoadingMask_1.default visible={reloading}/>
                        {getDynamicText_1.default({
                                    value: (<lineChart_1.default {...zoomRenderProps} {...chartOptions} legend={legend} onLegendSelectChanged={_this.handleLegendSelectChanged} series={tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(series)), tslib_1.__read(releaseSeries))}/>),
                                    fixed: <placeholder_1.default height="200px" testId="skeleton-ui"/>,
                                })}
                      </transitionChart_1.default>);
                        }}
                  </releaseSeries_1.default>);
                }}
            </eventsRequest_1.default>); }}
        </chartZoom_1.default>
      </react_1.Fragment>);
    };
    return VitalsChart;
}(react_1.Component));
exports.default = withApi_1.default(react_2.withTheme(ReactRouter.withRouter(VitalsChart)));
//# sourceMappingURL=vitalsChart.jsx.map