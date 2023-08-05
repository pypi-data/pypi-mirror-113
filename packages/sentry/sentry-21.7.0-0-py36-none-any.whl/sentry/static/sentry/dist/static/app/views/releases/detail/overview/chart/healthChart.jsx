Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var react_1 = require("@emotion/react");
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var areaChart_1 = tslib_1.__importDefault(require("app/components/charts/areaChart"));
var lineChart_1 = tslib_1.__importDefault(require("app/components/charts/lineChart"));
var stackedAreaChart_1 = tslib_1.__importDefault(require("app/components/charts/stackedAreaChart"));
var styles_1 = require("app/components/charts/styles");
var utils_1 = require("app/components/charts/utils");
var utils_2 = require("app/components/organizations/timeRangeSelector/utils");
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var utils_3 = require("app/utils");
var dates_1 = require("app/utils/dates");
var charts_1 = require("app/utils/discover/charts");
var formatters_1 = require("app/utils/formatters");
var queryString_1 = require("app/utils/queryString");
var utils_4 = require("app/views/releases/utils");
var sessionTerm_1 = require("../../../utils/sessionTerm");
var releaseChartControls_1 = require("./releaseChartControls");
var utils_5 = require("./utils");
var HealthChart = /** @class */ (function (_super) {
    tslib_1.__extends(HealthChart, _super);
    function HealthChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleLegendSelectChanged = function (legendChange) {
            var location = _this.props.location;
            var selected = legendChange.selected;
            var to = tslib_1.__assign(tslib_1.__assign({}, location), { query: tslib_1.__assign(tslib_1.__assign({}, location.query), { unselectedSeries: Object.keys(selected).filter(function (key) { return !selected[key]; }) }) });
            react_router_1.browserHistory.replace(to);
        };
        _this.formatTooltipValue = function (value) {
            var yAxis = _this.props.yAxis;
            switch (yAxis) {
                case releaseChartControls_1.YAxis.SESSION_DURATION:
                    return typeof value === 'number' ? formatters_1.getExactDuration(value, true) : '\u2015';
                case releaseChartControls_1.YAxis.CRASH_FREE:
                    return utils_3.defined(value) ? value + "%" : '\u2015';
                case releaseChartControls_1.YAxis.SESSIONS:
                case releaseChartControls_1.YAxis.USERS:
                default:
                    return typeof value === 'number' ? value.toLocaleString() : value;
            }
        };
        return _this;
    }
    HealthChart.prototype.componentDidMount = function () {
        if (this.shouldUnselectHealthySeries()) {
            this.props.onVisibleSeriesRecalculated();
            this.handleLegendSelectChanged({ selected: { Healthy: false } });
        }
    };
    HealthChart.prototype.shouldComponentUpdate = function (nextProps) {
        if (this.props.title !== nextProps.title) {
            return true;
        }
        if (nextProps.reloading || !nextProps.timeseriesData) {
            return false;
        }
        if (this.props.location.query.unselectedSeries !==
            nextProps.location.query.unselectedSeries) {
            return true;
        }
        if (isEqual_1.default(this.props.timeseriesData, nextProps.timeseriesData)) {
            return false;
        }
        return true;
    };
    HealthChart.prototype.shouldUnselectHealthySeries = function () {
        var _a = this.props, timeseriesData = _a.timeseriesData, location = _a.location, shouldRecalculateVisibleSeries = _a.shouldRecalculateVisibleSeries;
        var otherAreasThanHealthyArePositive = timeseriesData
            .filter(function (s) {
            return ![
                sessionTerm_1.sessionTerm.healthy,
                sessionTerm_1.sessionTerm.otherHealthy,
                sessionTerm_1.sessionTerm.otherErrored,
                sessionTerm_1.sessionTerm.otherCrashed,
                sessionTerm_1.sessionTerm.otherAbnormal,
            ].includes(s.seriesName);
        })
            .some(function (s) { return s.data.some(function (d) { return d.value > 0; }); });
        var alreadySomethingUnselected = !!queryString_1.decodeScalar(location.query.unselectedSeries);
        return (shouldRecalculateVisibleSeries &&
            otherAreasThanHealthyArePositive &&
            !alreadySomethingUnselected);
    };
    HealthChart.prototype.configureYAxis = function () {
        var _a = this.props, theme = _a.theme, yAxis = _a.yAxis;
        switch (yAxis) {
            case releaseChartControls_1.YAxis.CRASH_FREE:
                return {
                    max: 100,
                    scale: true,
                    axisLabel: {
                        formatter: function (value) { return utils_4.displayCrashFreePercent(value); },
                        color: theme.chartLabel,
                    },
                };
            case releaseChartControls_1.YAxis.SESSION_DURATION:
                return {
                    scale: true,
                    axisLabel: {
                        formatter: function (value) { return charts_1.axisDuration(value * 1000); },
                        color: theme.chartLabel,
                    },
                };
            case releaseChartControls_1.YAxis.SESSIONS:
            case releaseChartControls_1.YAxis.USERS:
            default:
                return undefined;
        }
    };
    HealthChart.prototype.configureXAxis = function () {
        var _a = this.props, timeseriesData = _a.timeseriesData, zoomRenderProps = _a.zoomRenderProps;
        if (timeseriesData.every(function (s) { return s.data.length === 1; })) {
            if (zoomRenderProps.period) {
                var _b = utils_2.parseStatsPeriod(zoomRenderProps.period, null), start = _b.start, end = _b.end;
                return { min: start, max: end };
            }
            return {
                min: dates_1.getUtcDateString(zoomRenderProps.start),
                max: dates_1.getUtcDateString(zoomRenderProps.end),
            };
        }
        return undefined;
    };
    HealthChart.prototype.getChart = function () {
        var yAxis = this.props.yAxis;
        switch (yAxis) {
            case releaseChartControls_1.YAxis.SESSION_DURATION:
                return areaChart_1.default;
            case releaseChartControls_1.YAxis.SESSIONS:
            case releaseChartControls_1.YAxis.USERS:
                return stackedAreaChart_1.default;
            case releaseChartControls_1.YAxis.CRASH_FREE:
            default:
                return lineChart_1.default;
        }
    };
    HealthChart.prototype.getLegendTooltipDescription = function (serieName) {
        var platform = this.props.platform;
        switch (serieName) {
            case sessionTerm_1.sessionTerm.crashed:
                return sessionTerm_1.getSessionTermDescription(sessionTerm_1.SessionTerm.CRASHED, platform);
            case sessionTerm_1.sessionTerm.abnormal:
                return sessionTerm_1.getSessionTermDescription(sessionTerm_1.SessionTerm.ABNORMAL, platform);
            case sessionTerm_1.sessionTerm.errored:
                return sessionTerm_1.getSessionTermDescription(sessionTerm_1.SessionTerm.ERRORED, platform);
            case sessionTerm_1.sessionTerm.healthy:
                return sessionTerm_1.getSessionTermDescription(sessionTerm_1.SessionTerm.HEALTHY, platform);
            case sessionTerm_1.sessionTerm['crash-free-users']:
                return sessionTerm_1.getSessionTermDescription(sessionTerm_1.SessionTerm.CRASH_FREE_USERS, platform);
            case sessionTerm_1.sessionTerm['crash-free-sessions']:
                return sessionTerm_1.getSessionTermDescription(sessionTerm_1.SessionTerm.CRASH_FREE_SESSIONS, platform);
            default:
                return '';
        }
    };
    HealthChart.prototype.getLegendSeries = function () {
        var timeseriesData = this.props.timeseriesData;
        return (timeseriesData
            .filter(function (d) { return !utils_5.isOtherSeries(d); })
            // we don't want Other Healthy, Other Crashed, etc. to show up in the legend
            .sort(utils_5.sortSessionSeries)
            .map(function (d) { return d.seriesName; }));
    };
    HealthChart.prototype.getLegendSelectedSeries = function () {
        var _a;
        var _b = this.props, location = _b.location, yAxis = _b.yAxis;
        var selection = (_a = utils_1.getSeriesSelection(location)) !== null && _a !== void 0 ? _a : {};
        // otherReleases toggles all "other" series (other healthy, other crashed, etc.) at once
        var otherReleasesVisible = !(selection[sessionTerm_1.sessionTerm.otherReleases] === false);
        if (yAxis === releaseChartControls_1.YAxis.SESSIONS || yAxis === releaseChartControls_1.YAxis.USERS) {
            selection[sessionTerm_1.sessionTerm.otherErrored] =
                !(selection === null || selection === void 0 ? void 0 : selection.hasOwnProperty(sessionTerm_1.sessionTerm.errored)) && otherReleasesVisible;
            selection[sessionTerm_1.sessionTerm.otherCrashed] =
                !(selection === null || selection === void 0 ? void 0 : selection.hasOwnProperty(sessionTerm_1.sessionTerm.crashed)) && otherReleasesVisible;
            selection[sessionTerm_1.sessionTerm.otherAbnormal] =
                !(selection === null || selection === void 0 ? void 0 : selection.hasOwnProperty(sessionTerm_1.sessionTerm.abnormal)) && otherReleasesVisible;
            selection[sessionTerm_1.sessionTerm.otherHealthy] =
                !(selection === null || selection === void 0 ? void 0 : selection.hasOwnProperty(sessionTerm_1.sessionTerm.healthy)) && otherReleasesVisible;
        }
        if (yAxis === releaseChartControls_1.YAxis.CRASH_FREE) {
            selection[sessionTerm_1.sessionTerm.otherCrashFreeSessions] =
                !(selection === null || selection === void 0 ? void 0 : selection.hasOwnProperty(sessionTerm_1.sessionTerm['crash-free-sessions'])) &&
                    otherReleasesVisible;
            selection[sessionTerm_1.sessionTerm.otherCrashFreeUsers] =
                !(selection === null || selection === void 0 ? void 0 : selection.hasOwnProperty(sessionTerm_1.sessionTerm['crash-free-users'])) &&
                    otherReleasesVisible;
        }
        return selection;
    };
    HealthChart.prototype.render = function () {
        var _this = this;
        var _a = this.props, timeseriesData = _a.timeseriesData, zoomRenderProps = _a.zoomRenderProps, title = _a.title, help = _a.help;
        var Chart = this.getChart();
        var legend = {
            right: 10,
            top: 0,
            data: this.getLegendSeries(),
            selected: this.getLegendSelectedSeries(),
            tooltip: {
                show: true,
                // TODO(ts) tooltip.formatter has incorrect types in echarts 4
                formatter: function (params) {
                    var _a;
                    var seriesNameDesc = _this.getLegendTooltipDescription((_a = params.name) !== null && _a !== void 0 ? _a : '');
                    if (!seriesNameDesc) {
                        return '';
                    }
                    return ['<div class="tooltip-description">', seriesNameDesc, '</div>'].join('');
                },
            },
        };
        return (<React.Fragment>
        <styles_1.HeaderTitleLegend>
          {title}
          {help && <questionTooltip_1.default size="sm" position="top" title={help}/>}
        </styles_1.HeaderTitleLegend>

        <Chart legend={legend} {...zoomRenderProps} series={timeseriesData} isGroupedByDate seriesOptions={{
                showSymbol: false,
            }} grid={{
                left: '10px',
                right: '10px',
                top: '40px',
                bottom: '0px',
            }} yAxis={this.configureYAxis()} xAxis={this.configureXAxis()} tooltip={{ valueFormatter: this.formatTooltipValue }} onLegendSelectChanged={this.handleLegendSelectChanged} transformSinglePointToBar/>
      </React.Fragment>);
    };
    return HealthChart;
}(React.Component));
exports.default = react_1.withTheme(HealthChart);
//# sourceMappingURL=healthChart.jsx.map