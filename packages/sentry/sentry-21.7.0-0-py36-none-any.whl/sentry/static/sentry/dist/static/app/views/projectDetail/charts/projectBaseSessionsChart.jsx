Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_2 = require("@emotion/react");
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var chartZoom_1 = tslib_1.__importDefault(require("app/components/charts/chartZoom"));
var errorPanel_1 = tslib_1.__importDefault(require("app/components/charts/errorPanel"));
var lineChart_1 = tslib_1.__importDefault(require("app/components/charts/lineChart"));
var releaseSeries_1 = tslib_1.__importDefault(require("app/components/charts/releaseSeries"));
var stackedAreaChart_1 = tslib_1.__importDefault(require("app/components/charts/stackedAreaChart"));
var styles_1 = require("app/components/charts/styles");
var transitionChart_1 = tslib_1.__importDefault(require("app/components/charts/transitionChart"));
var transparentLoadingMask_1 = tslib_1.__importDefault(require("app/components/charts/transparentLoadingMask"));
var utils_1 = require("app/components/charts/utils");
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var withGlobalSelection_1 = tslib_1.__importDefault(require("app/utils/withGlobalSelection"));
var utils_2 = require("app/views/releases/utils");
var sessionTerm_1 = require("app/views/releases/utils/sessionTerm");
var projectCharts_1 = require("../projectCharts");
var sessionsRequest_1 = tslib_1.__importDefault(require("./sessionsRequest"));
function ProjectBaseSessionsChart(_a) {
    var title = _a.title, theme = _a.theme, organization = _a.organization, router = _a.router, selection = _a.selection, api = _a.api, onTotalValuesChange = _a.onTotalValuesChange, displayMode = _a.displayMode, help = _a.help, disablePrevious = _a.disablePrevious, query = _a.query;
    var projects = selection.projects, environments = selection.environments, datetime = selection.datetime;
    var start = datetime.start, end = datetime.end, period = datetime.period, utc = datetime.utc;
    return (<react_1.Fragment>
      {getDynamicText_1.default({
            value: (<chartZoom_1.default router={router} period={period} start={start} end={end} utc={utc}>
            {function (zoomRenderProps) { return (<sessionsRequest_1.default api={api} selection={selection} organization={organization} onTotalValuesChange={onTotalValuesChange} displayMode={displayMode} disablePrevious={disablePrevious} query={query}>
                {function (_a) {
                        var errored = _a.errored, loading = _a.loading, reloading = _a.reloading, timeseriesData = _a.timeseriesData, previousTimeseriesData = _a.previousTimeseriesData;
                        return (<releaseSeries_1.default utc={utc} period={period} start={start} end={end} projects={projects} environments={environments} query={query}>
                    {function (_a) {
                                var releaseSeries = _a.releaseSeries;
                                if (errored) {
                                    return (<errorPanel_1.default>
                            <icons_1.IconWarning color="gray300" size="lg"/>
                          </errorPanel_1.default>);
                                }
                                return (<transitionChart_1.default loading={loading} reloading={reloading}>
                          <transparentLoadingMask_1.default visible={reloading}/>

                          <styles_1.HeaderTitleLegend>
                            {title}
                            {help && (<questionTooltip_1.default size="sm" position="top" title={help}/>)}
                          </styles_1.HeaderTitleLegend>

                          <Chart theme={theme} zoomRenderProps={zoomRenderProps} reloading={reloading} timeSeries={timeseriesData} previousTimeSeries={previousTimeseriesData
                                        ? [previousTimeseriesData]
                                        : undefined} releaseSeries={releaseSeries} displayMode={displayMode}/>
                        </transitionChart_1.default>);
                            }}
                  </releaseSeries_1.default>);
                    }}
              </sessionsRequest_1.default>); }}
          </chartZoom_1.default>),
            fixed: title + " Chart",
        })}
    </react_1.Fragment>);
}
var Chart = /** @class */ (function (_super) {
    tslib_1.__extends(Chart, _super);
    function Chart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            seriesSelection: {},
            forceUpdate: false,
        };
        // inspired by app/components/charts/eventsChart.tsx@handleLegendSelectChanged
        _this.handleLegendSelectChanged = function (_a) {
            var selected = _a.selected;
            var seriesSelection = Object.keys(selected).reduce(function (state, key) {
                state[key] = selected[key];
                return state;
            }, {});
            // we have to force an update here otherwise ECharts will
            // update its internal state and disable the series
            _this.setState({ seriesSelection: seriesSelection, forceUpdate: true }, function () {
                return _this.setState({ forceUpdate: false });
            });
        };
        return _this;
    }
    Chart.prototype.shouldComponentUpdate = function (nextProps, nextState) {
        if (nextState.forceUpdate) {
            return true;
        }
        if (!isEqual_1.default(this.state.seriesSelection, nextState.seriesSelection)) {
            return true;
        }
        if (nextProps.releaseSeries !== this.props.releaseSeries &&
            !nextProps.reloading &&
            !this.props.reloading) {
            return true;
        }
        if (this.props.reloading && !nextProps.reloading) {
            return true;
        }
        if (nextProps.timeSeries !== this.props.timeSeries) {
            return true;
        }
        return false;
    };
    Object.defineProperty(Chart.prototype, "legend", {
        get: function () {
            var _a;
            var _b, _c;
            var _d = this.props, theme = _d.theme, timeSeries = _d.timeSeries, previousTimeSeries = _d.previousTimeSeries, releaseSeries = _d.releaseSeries;
            var seriesSelection = this.state.seriesSelection;
            var hideReleasesByDefault = ((_c = (_b = releaseSeries[0]) === null || _b === void 0 ? void 0 : _b.markLine) === null || _c === void 0 ? void 0 : _c.data.length) >= utils_1.RELEASE_LINES_THRESHOLD;
            var hideHealthyByDefault = timeSeries
                .filter(function (s) { return sessionTerm_1.sessionTerm.healthy !== s.seriesName; })
                .some(function (s) { return s.data.some(function (d) { return d.value > 0; }); });
            var selected = Object.keys(seriesSelection).length === 0 &&
                (hideReleasesByDefault || hideHealthyByDefault)
                ? (_a = {},
                    _a[locale_1.t('Releases')] = !hideReleasesByDefault,
                    _a[sessionTerm_1.sessionTerm.healthy] = !hideHealthyByDefault,
                    _a) : seriesSelection;
            return {
                right: 10,
                top: 0,
                icon: 'circle',
                itemHeight: 8,
                itemWidth: 8,
                itemGap: 12,
                align: 'left',
                textStyle: {
                    color: theme.textColor,
                    verticalAlign: 'top',
                    fontSize: 11,
                    fontFamily: theme.text.family,
                },
                data: tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(timeSeries.map(function (s) { return s.seriesName; }))), tslib_1.__read((previousTimeSeries !== null && previousTimeSeries !== void 0 ? previousTimeSeries : []).map(function (s) { return s.seriesName; }))), tslib_1.__read(releaseSeries.map(function (s) { return s.seriesName; }))),
                selected: selected,
            };
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(Chart.prototype, "chartOptions", {
        get: function () {
            var _a = this.props, theme = _a.theme, displayMode = _a.displayMode;
            return {
                grid: { left: '10px', right: '10px', top: '40px', bottom: '0px' },
                seriesOptions: {
                    showSymbol: false,
                },
                tooltip: {
                    trigger: 'axis',
                    truncate: 80,
                    valueFormatter: function (value) {
                        if (value === null) {
                            return '\u2014';
                        }
                        if (displayMode === projectCharts_1.DisplayModes.STABILITY) {
                            return utils_2.displayCrashFreePercent(value, 0, 3);
                        }
                        return typeof value === 'number' ? value.toLocaleString() : value;
                    },
                },
                yAxis: displayMode === projectCharts_1.DisplayModes.STABILITY
                    ? {
                        axisLabel: {
                            color: theme.gray200,
                            formatter: function (value) { return utils_2.displayCrashFreePercent(value); },
                        },
                        scale: true,
                        max: 100,
                    }
                    : { min: 0 },
            };
        },
        enumerable: false,
        configurable: true
    });
    Chart.prototype.render = function () {
        var _a = this.props, zoomRenderProps = _a.zoomRenderProps, timeSeries = _a.timeSeries, previousTimeSeries = _a.previousTimeSeries, releaseSeries = _a.releaseSeries, displayMode = _a.displayMode;
        var ChartComponent = displayMode === projectCharts_1.DisplayModes.STABILITY ? lineChart_1.default : stackedAreaChart_1.default;
        return (<ChartComponent {...zoomRenderProps} {...this.chartOptions} legend={this.legend} series={Array.isArray(releaseSeries) ? tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(timeSeries)), tslib_1.__read(releaseSeries)) : timeSeries} previousPeriod={previousTimeSeries} onLegendSelectChanged={this.handleLegendSelectChanged} transformSinglePointToBar/>);
    };
    return Chart;
}(react_1.Component));
exports.default = withGlobalSelection_1.default(react_2.withTheme(ProjectBaseSessionsChart));
//# sourceMappingURL=projectBaseSessionsChart.jsx.map