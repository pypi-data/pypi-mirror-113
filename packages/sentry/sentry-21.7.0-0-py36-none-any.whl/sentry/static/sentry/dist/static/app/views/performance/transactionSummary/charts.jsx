Object.defineProperty(exports, "__esModule", { value: true });
exports.DisplayModes = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var optionSelector_1 = tslib_1.__importDefault(require("app/components/charts/optionSelector"));
var styles_1 = require("app/components/charts/styles");
var panels_1 = require("app/components/panels");
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var locale_1 = require("app/locale");
var histogram_1 = require("app/utils/performance/histogram");
var queryString_1 = require("app/utils/queryString");
var overview_1 = require("app/views/releases/detail/overview");
var releaseChartControls_1 = require("app/views/releases/detail/overview/chart/releaseChartControls");
var types_1 = require("../trends/types");
var utils_1 = require("../trends/utils");
var durationChart_1 = tslib_1.__importDefault(require("./durationChart"));
var durationPercentileChart_1 = tslib_1.__importDefault(require("./durationPercentileChart"));
var filter_1 = require("./filter");
var latencyChart_1 = tslib_1.__importStar(require("./latencyChart"));
var trendChart_1 = tslib_1.__importDefault(require("./trendChart"));
var vitalsChart_1 = tslib_1.__importDefault(require("./vitalsChart"));
var DisplayModes;
(function (DisplayModes) {
    DisplayModes["DURATION_PERCENTILE"] = "durationpercentile";
    DisplayModes["DURATION"] = "duration";
    DisplayModes["LATENCY"] = "latency";
    DisplayModes["TREND"] = "trend";
    DisplayModes["VITALS"] = "vitals";
})(DisplayModes = exports.DisplayModes || (exports.DisplayModes = {}));
function generateDisplayOptions(currentFilter) {
    if (currentFilter === filter_1.SpanOperationBreakdownFilter.None) {
        return [
            { value: DisplayModes.DURATION, label: locale_1.t('Duration Breakdown') },
            { value: DisplayModes.DURATION_PERCENTILE, label: locale_1.t('Duration Percentiles') },
            { value: DisplayModes.LATENCY, label: locale_1.t('Duration Distribution') },
            { value: DisplayModes.TREND, label: locale_1.t('Trends') },
            { value: DisplayModes.VITALS, label: locale_1.t('Web Vitals') },
        ];
    }
    // A span operation name breakdown has been chosen.
    return [
        { value: DisplayModes.DURATION, label: locale_1.t('Span Operation Breakdown') },
        { value: DisplayModes.DURATION_PERCENTILE, label: locale_1.t('Span Operation Percentiles') },
        { value: DisplayModes.LATENCY, label: locale_1.t('Span Operation Distribution') },
        { value: DisplayModes.TREND, label: locale_1.t('Trends') },
        { value: DisplayModes.VITALS, label: locale_1.t('Web Vitals') },
    ];
}
var TREND_FUNCTIONS_OPTIONS = utils_1.TRENDS_FUNCTIONS.map(function (_a) {
    var field = _a.field, label = _a.label;
    return ({
        value: field,
        label: label,
    });
});
var TransactionSummaryCharts = /** @class */ (function (_super) {
    tslib_1.__extends(TransactionSummaryCharts, _super);
    function TransactionSummaryCharts() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDisplayChange = function (value) {
            var location = _this.props.location;
            react_router_1.browserHistory.push({
                pathname: location.pathname,
                query: tslib_1.__assign(tslib_1.__assign({}, histogram_1.removeHistogramQueryStrings(location, [latencyChart_1.ZOOM_START, latencyChart_1.ZOOM_END])), { display: value }),
            });
        };
        _this.handleTrendDisplayChange = function (value) {
            var location = _this.props.location;
            react_router_1.browserHistory.push({
                pathname: location.pathname,
                query: tslib_1.__assign(tslib_1.__assign({}, location.query), { trendFunction: value }),
            });
        };
        _this.handleTrendColumnChange = function (value) {
            var location = _this.props.location;
            react_router_1.browserHistory.push({
                pathname: location.pathname,
                query: tslib_1.__assign(tslib_1.__assign({}, location.query), { trendColumn: value }),
            });
        };
        return _this;
    }
    TransactionSummaryCharts.prototype.render = function () {
        var _a = this.props, totalValues = _a.totalValues, eventView = _a.eventView, organization = _a.organization, location = _a.location, currentFilter = _a.currentFilter;
        var TREND_PARAMETERS_OPTIONS = utils_1.getTrendsParameters({
            canSeeSpanOpTrends: organization.features.includes('performance-ops-breakdown'),
        }).map(function (_a) {
            var column = _a.column, label = _a.label;
            return ({
                value: column,
                label: label,
            });
        });
        var display = queryString_1.decodeScalar(location.query.display, DisplayModes.DURATION);
        var trendFunction = queryString_1.decodeScalar(location.query.trendFunction, TREND_FUNCTIONS_OPTIONS[0].value);
        var trendColumn = queryString_1.decodeScalar(location.query.trendColumn, TREND_PARAMETERS_OPTIONS[0].value);
        if (!Object.values(DisplayModes).includes(display)) {
            display = DisplayModes.DURATION;
        }
        if (!Object.values(types_1.TrendFunctionField).includes(trendFunction)) {
            trendFunction = types_1.TrendFunctionField.P50;
        }
        if (!Object.values(types_1.TrendColumnField).includes(trendColumn)) {
            trendColumn = types_1.TrendColumnField.DURATION;
        }
        var releaseQueryExtra = {
            yAxis: display === DisplayModes.VITALS ? releaseChartControls_1.YAxis.COUNT_VITAL : releaseChartControls_1.YAxis.COUNT_DURATION,
            showTransactions: display === DisplayModes.VITALS
                ? overview_1.TransactionsListOption.SLOW_LCP
                : display === DisplayModes.DURATION
                    ? overview_1.TransactionsListOption.SLOW
                    : undefined,
        };
        return (<panels_1.Panel>
        <styles_1.ChartContainer>
          {display === DisplayModes.LATENCY && (<latencyChart_1.default organization={organization} location={location} query={eventView.query} project={eventView.project} environment={eventView.environment} start={eventView.start} end={eventView.end} statsPeriod={eventView.statsPeriod} currentFilter={currentFilter}/>)}
          {display === DisplayModes.DURATION && (<durationChart_1.default organization={organization} query={eventView.query} queryExtra={releaseQueryExtra} project={eventView.project} environment={eventView.environment} start={eventView.start} end={eventView.end} statsPeriod={eventView.statsPeriod} currentFilter={currentFilter}/>)}
          {display === DisplayModes.DURATION_PERCENTILE && (<durationPercentileChart_1.default organization={organization} location={location} query={eventView.query} project={eventView.project} environment={eventView.environment} start={eventView.start} end={eventView.end} statsPeriod={eventView.statsPeriod} currentFilter={currentFilter}/>)}
          {display === DisplayModes.TREND && (<trendChart_1.default trendDisplay={utils_1.generateTrendFunctionAsString(trendFunction, trendColumn)} organization={organization} query={eventView.query} queryExtra={releaseQueryExtra} project={eventView.project} environment={eventView.environment} start={eventView.start} end={eventView.end} statsPeriod={eventView.statsPeriod}/>)}
          {display === DisplayModes.VITALS && (<vitalsChart_1.default organization={organization} query={eventView.query} queryExtra={releaseQueryExtra} project={eventView.project} environment={eventView.environment} start={eventView.start} end={eventView.end} statsPeriod={eventView.statsPeriod}/>)}
        </styles_1.ChartContainer>

        <styles_1.ChartControls>
          <styles_1.InlineContainer>
            <styles_1.SectionHeading key="total-heading">{locale_1.t('Total Transactions')}</styles_1.SectionHeading>
            <styles_1.SectionValue key="total-value">
              {totalValues === null ? (<placeholder_1.default height="24px"/>) : (totalValues.toLocaleString())}
            </styles_1.SectionValue>
          </styles_1.InlineContainer>
          <styles_1.InlineContainer>
            {display === DisplayModes.TREND && (<optionSelector_1.default title={locale_1.t('Percentile')} selected={trendFunction} options={TREND_FUNCTIONS_OPTIONS} onChange={this.handleTrendDisplayChange}/>)}
            {display === DisplayModes.TREND && (<optionSelector_1.default title={locale_1.t('Parameter')} selected={trendColumn} options={TREND_PARAMETERS_OPTIONS} onChange={this.handleTrendColumnChange}/>)}
            {display === DisplayModes.LATENCY && (<latencyChart_1.LatencyChartControls location={location}/>)}
            <optionSelector_1.default title={locale_1.t('Display')} selected={display} options={generateDisplayOptions(currentFilter)} onChange={this.handleDisplayChange}/>
          </styles_1.InlineContainer>
        </styles_1.ChartControls>
      </panels_1.Panel>);
    };
    return TransactionSummaryCharts;
}(react_1.Component));
exports.default = TransactionSummaryCharts;
//# sourceMappingURL=charts.jsx.map