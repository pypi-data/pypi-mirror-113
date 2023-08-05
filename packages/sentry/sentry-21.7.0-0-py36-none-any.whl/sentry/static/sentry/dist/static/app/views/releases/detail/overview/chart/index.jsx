Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_2 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var guideAnchor_1 = tslib_1.__importDefault(require("app/components/assistant/guideAnchor"));
var eventsChart_1 = tslib_1.__importDefault(require("app/components/charts/eventsChart"));
var styles_1 = require("app/components/charts/styles");
var panels_1 = require("app/components/panels");
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var locale_1 = require("app/locale");
var analytics_1 = require("app/utils/analytics");
var queryString_1 = require("app/utils/queryString");
var data_1 = require("app/views/performance/data");
var releaseStatsRequest_1 = tslib_1.__importDefault(require("../releaseStatsRequest"));
var healthChartContainer_1 = tslib_1.__importDefault(require("./healthChartContainer"));
var releaseChartControls_1 = tslib_1.__importStar(require("./releaseChartControls"));
var utils_1 = require("./utils");
var ReleaseChartContainer = /** @class */ (function (_super) {
    tslib_1.__extends(ReleaseChartContainer, _super);
    function ReleaseChartContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * The top events endpoint used to generate these series is not guaranteed to return a series
         * for both the current release and the other releases. This happens when there is insufficient
         * data. In these cases, the endpoint will return a single zerofilled series for the current
         * release.
         *
         * This is problematic as we want to show both series even if one is empty. To deal with this,
         * we clone the non empty series (to preserve the timestamps) with value 0 (to represent the
         * lack of data).
         */
        _this.seriesTransformer = function (series) {
            var current = null;
            var others = null;
            var allSeries = [];
            series.forEach(function (s) {
                if (s.seriesName === 'current' || s.seriesName === locale_1.t('This Release')) {
                    current = s;
                }
                else if (s.seriesName === 'others' || s.seriesName === locale_1.t('Other Releases')) {
                    others = s;
                }
                else {
                    allSeries.push(s);
                }
            });
            if (current !== null && others === null) {
                others = _this.cloneSeriesAsZero(current);
            }
            else if (current === null && others !== null) {
                current = _this.cloneSeriesAsZero(others);
            }
            if (others !== null) {
                others.seriesName = locale_1.t('Other Releases');
                allSeries.unshift(others);
            }
            if (current !== null) {
                current.seriesName = locale_1.t('This Release');
                allSeries.unshift(current);
            }
            return allSeries;
        };
        return _this;
    }
    ReleaseChartContainer.prototype.componentDidMount = function () {
        var _a = this.props, organization = _a.organization, yAxis = _a.yAxis, platform = _a.platform;
        analytics_1.trackAnalyticsEvent({
            eventKey: "release_detail.display_chart",
            eventName: "Release Detail: Display Chart",
            organization_id: parseInt(organization.id, 10),
            display: yAxis,
            platform: platform,
        });
    };
    /**
     * This returns an array with 3 colors, one for each of
     * 1. This Release
     * 2. Other Releases
     * 3. Releases (the markers)
     */
    ReleaseChartContainer.prototype.getTransactionsChartColors = function () {
        var _a = this.props, yAxis = _a.yAxis, theme = _a.theme;
        switch (yAxis) {
            case releaseChartControls_1.YAxis.FAILED_TRANSACTIONS:
                return [theme.red300, theme.red100, theme.purple300];
            default:
                return [theme.purple300, theme.purple100, theme.purple300];
        }
    };
    ReleaseChartContainer.prototype.getChartTitle = function () {
        var _a = this.props, yAxis = _a.yAxis, organization = _a.organization;
        switch (yAxis) {
            case releaseChartControls_1.YAxis.SESSIONS:
                return {
                    title: locale_1.t('Session Count'),
                    help: locale_1.t('The number of sessions in a given period.'),
                };
            case releaseChartControls_1.YAxis.USERS:
                return {
                    title: locale_1.t('User Count'),
                    help: locale_1.t('The number of users in a given period.'),
                };
            case releaseChartControls_1.YAxis.SESSION_DURATION:
                return { title: locale_1.t('Session Duration') };
            case releaseChartControls_1.YAxis.CRASH_FREE:
                return { title: locale_1.t('Crash Free Rate') };
            case releaseChartControls_1.YAxis.FAILED_TRANSACTIONS:
                return {
                    title: locale_1.t('Failure Count'),
                    help: data_1.getTermHelp(organization, data_1.PERFORMANCE_TERM.FAILURE_RATE),
                };
            case releaseChartControls_1.YAxis.COUNT_DURATION:
                return { title: locale_1.t('Slow Duration Count') };
            case releaseChartControls_1.YAxis.COUNT_VITAL:
                return { title: locale_1.t('Slow Vital Count') };
            case releaseChartControls_1.YAxis.EVENTS:
            default:
                return { title: locale_1.t('Event Count') };
        }
    };
    ReleaseChartContainer.prototype.cloneSeriesAsZero = function (series) {
        return tslib_1.__assign(tslib_1.__assign({}, series), { data: series.data.map(function (point) { return (tslib_1.__assign(tslib_1.__assign({}, point), { value: 0 })); }) });
    };
    ReleaseChartContainer.prototype.renderStackedChart = function () {
        var _a = this.props, location = _a.location, router = _a.router, organization = _a.organization, api = _a.api, releaseMeta = _a.releaseMeta, yAxis = _a.yAxis, eventType = _a.eventType, vitalType = _a.vitalType, selection = _a.selection, version = _a.version;
        var projects = selection.projects, environments = selection.environments, datetime = selection.datetime;
        var start = datetime.start, end = datetime.end, period = datetime.period, utc = datetime.utc;
        var eventView = utils_1.getReleaseEventView(selection, version, yAxis, eventType, vitalType, organization);
        var apiPayload = eventView.getEventsAPIPayload(location);
        var colors = this.getTransactionsChartColors();
        var _b = this.getChartTitle(), title = _b.title, help = _b.help;
        var releaseQueryExtra = {
            showTransactions: location.query.showTransactions,
            eventType: eventType,
            vitalType: vitalType,
            yAxis: yAxis,
        };
        return (<eventsChart_1.default router={router} organization={organization} showLegend yAxis={eventView.getYAxis()} query={apiPayload.query} api={api} projects={projects} environments={environments} start={start} end={end} period={period} utc={utc} disablePrevious emphasizeReleases={[releaseMeta.version]} field={eventView.getFields()} topEvents={2} orderby={queryString_1.decodeScalar(apiPayload.sort)} currentSeriesName={locale_1.t('This Release')} 
        // This seems a little strange but is intentional as EventsChart
        // uses the previousSeriesName as the secondary series name
        previousSeriesName={locale_1.t('Other Releases')} seriesTransformer={this.seriesTransformer} disableableSeries={[locale_1.t('This Release'), locale_1.t('Other Releases')]} colors={colors} preserveReleaseQueryParams releaseQueryExtra={releaseQueryExtra} chartHeader={<styles_1.HeaderTitleLegend>
            {title}
            {help && <questionTooltip_1.default size="sm" position="top" title={help}/>}
          </styles_1.HeaderTitleLegend>} legendOptions={{ right: 10, top: 0 }} chartOptions={{ grid: { left: '10px', right: '10px', top: '40px', bottom: '0px' } }}/>);
    };
    ReleaseChartContainer.prototype.renderHealthChart = function (loading, reloading, errored, chartData) {
        var _a = this.props, selection = _a.selection, yAxis = _a.yAxis, router = _a.router, platform = _a.platform;
        var _b = this.getChartTitle(), title = _b.title, help = _b.help;
        return (<healthChartContainer_1.default platform={platform} loading={loading} errored={errored} reloading={reloading} chartData={chartData} selection={selection} yAxis={yAxis} router={router} title={title} help={help}/>);
    };
    ReleaseChartContainer.prototype.render = function () {
        var _this = this;
        var _a = this.props, yAxis = _a.yAxis, eventType = _a.eventType, vitalType = _a.vitalType, hasDiscover = _a.hasDiscover, hasHealthData = _a.hasHealthData, hasPerformance = _a.hasPerformance, onYAxisChange = _a.onYAxisChange, onEventTypeChange = _a.onEventTypeChange, onVitalTypeChange = _a.onVitalTypeChange, organization = _a.organization, defaultStatsPeriod = _a.defaultStatsPeriod, api = _a.api, version = _a.version, selection = _a.selection, location = _a.location, projectSlug = _a.projectSlug;
        return (<releaseStatsRequest_1.default api={api} organization={organization} projectSlug={projectSlug} version={version} selection={selection} location={location} yAxis={yAxis} eventType={eventType} vitalType={vitalType} hasHealthData={hasHealthData} hasDiscover={hasDiscover} hasPerformance={hasPerformance} defaultStatsPeriod={defaultStatsPeriod}>
        {function (_a) {
                var loading = _a.loading, reloading = _a.reloading, errored = _a.errored, chartData = _a.chartData, chartSummary = _a.chartSummary;
                return (<panels_1.Panel>
            <styles_1.ChartContainer>
              {((hasDiscover || hasPerformance) && yAxis === releaseChartControls_1.YAxis.EVENTS) ||
                        (hasPerformance && releaseChartControls_1.PERFORMANCE_AXIS.includes(yAxis))
                        ? _this.renderStackedChart()
                        : _this.renderHealthChart(loading, reloading, errored, chartData)}
            </styles_1.ChartContainer>
            <AnchorWrapper>
              <guideAnchor_1.default target="release_chart" position="bottom" offset="-80px">
                <react_1.Fragment />
              </guideAnchor_1.default>
            </AnchorWrapper>
            <releaseChartControls_1.default summary={chartSummary} yAxis={yAxis} onYAxisChange={onYAxisChange} eventType={eventType} onEventTypeChange={onEventTypeChange} vitalType={vitalType} onVitalTypeChange={onVitalTypeChange} organization={organization} hasDiscover={hasDiscover} hasHealthData={hasHealthData} hasPerformance={hasPerformance}/>
          </panels_1.Panel>);
            }}
      </releaseStatsRequest_1.default>);
    };
    return ReleaseChartContainer;
}(react_1.Component));
exports.default = react_2.withTheme(ReleaseChartContainer);
var AnchorWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  height: 0;\n  width: 0;\n  margin-left: 50%;\n"], ["\n  height: 0;\n  width: 0;\n  margin-left: 50%;\n"])));
var templateObject_1;
//# sourceMappingURL=index.jsx.map