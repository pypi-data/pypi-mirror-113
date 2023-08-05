Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var pick_1 = tslib_1.__importDefault(require("lodash/pick"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var areaChart_1 = tslib_1.__importDefault(require("app/components/charts/areaChart"));
var errorPanel_1 = tslib_1.__importDefault(require("app/components/charts/errorPanel"));
var loadingPanel_1 = tslib_1.__importDefault(require("app/components/charts/loadingPanel"));
var styles_1 = require("app/components/charts/styles");
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var utils_1 = require("app/utils");
var charts_1 = require("app/utils/discover/charts");
var eventView_1 = tslib_1.__importDefault(require("app/utils/discover/eventView"));
var formatters_1 = require("app/utils/formatters");
var filter_1 = require("./filter");
var QUERY_KEYS = [
    'environment',
    'project',
    'query',
    'start',
    'end',
    'statsPeriod',
];
/**
 * Fetch and render a bar chart that shows event volume
 * for each duration bucket. We always render 15 buckets of
 * equal widths based on the endpoints min + max durations.
 *
 * This graph visualizes how many transactions were recorded
 * at each duration bucket, showing the modality of the transaction.
 */
var DurationPercentileChart = /** @class */ (function (_super) {
    tslib_1.__extends(DurationPercentileChart, _super);
    function DurationPercentileChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.generateFields = function () {
            var currentFilter = _this.props.currentFilter;
            if (currentFilter === filter_1.SpanOperationBreakdownFilter.None) {
                return [
                    'percentile(transaction.duration, 0.10)',
                    'percentile(transaction.duration, 0.25)',
                    'percentile(transaction.duration, 0.50)',
                    'percentile(transaction.duration, 0.75)',
                    'percentile(transaction.duration, 0.90)',
                    'percentile(transaction.duration, 0.95)',
                    'percentile(transaction.duration, 0.99)',
                    'percentile(transaction.duration, 0.995)',
                    'percentile(transaction.duration, 0.999)',
                    'p100()',
                ];
            }
            var field = filter_1.filterToField(currentFilter);
            return [
                "percentile(" + field + ", 0.10)",
                "percentile(" + field + ", 0.25)",
                "percentile(" + field + ", 0.50)",
                "percentile(" + field + ", 0.75)",
                "percentile(" + field + ", 0.90)",
                "percentile(" + field + ", 0.95)",
                "percentile(" + field + ", 0.99)",
                "percentile(" + field + ", 0.995)",
                "percentile(" + field + ", 0.999)",
                "p100(" + field + ")",
            ];
        };
        _this.getEndpoints = function () {
            var _a = _this.props, organization = _a.organization, query = _a.query, start = _a.start, end = _a.end, statsPeriod = _a.statsPeriod, environment = _a.environment, project = _a.project, location = _a.location;
            var eventView = eventView_1.default.fromSavedQuery({
                id: '',
                name: '',
                version: 2,
                fields: _this.generateFields(),
                orderby: '',
                projects: project,
                range: statsPeriod,
                query: query,
                environment: environment,
                start: start,
                end: end,
            });
            var apiPayload = eventView.getEventsAPIPayload(location);
            apiPayload.referrer = 'api.performance.durationpercentilechart';
            return [
                ['chartData', "/organizations/" + organization.slug + "/eventsv2/", { query: apiPayload }],
            ];
        };
        return _this;
    }
    DurationPercentileChart.prototype.componentDidUpdate = function (prevProps) {
        if (this.shouldRefetchData(prevProps)) {
            this.fetchData();
        }
    };
    DurationPercentileChart.prototype.shouldRefetchData = function (prevProps) {
        if (this.state.loading) {
            return false;
        }
        return !isEqual_1.default(pick_1.default(prevProps, QUERY_KEYS), pick_1.default(this.props, QUERY_KEYS));
    };
    DurationPercentileChart.prototype.renderLoading = function () {
        return <loadingPanel_1.default data-test-id="histogram-loading"/>;
    };
    DurationPercentileChart.prototype.renderError = function () {
        // Don't call super as we don't really need issues for this.
        return (<errorPanel_1.default>
        <icons_1.IconWarning color="gray300" size="lg"/>
      </errorPanel_1.default>);
    };
    DurationPercentileChart.prototype.renderBody = function () {
        var currentFilter = this.props.currentFilter;
        var chartData = this.state.chartData;
        if (!utils_1.defined(chartData)) {
            return null;
        }
        var colors = function (theme) {
            return currentFilter === filter_1.SpanOperationBreakdownFilter.None
                ? theme.charts.getColorPalette(1)
                : [filter_1.filterToColour(currentFilter)];
        };
        return <StyledAreaChart series={transformData(chartData.data)} colors={colors}/>;
    };
    DurationPercentileChart.prototype.render = function () {
        var currentFilter = this.props.currentFilter;
        var headerTitle = currentFilter === filter_1.SpanOperationBreakdownFilter.None
            ? locale_1.t('Duration Percentiles')
            : locale_1.tct('Span Operation Percentiles - [operationName]', {
                operationName: currentFilter,
            });
        return (<React.Fragment>
        <styles_1.HeaderTitleLegend>
          {headerTitle}
          <questionTooltip_1.default position="top" size="sm" title={locale_1.t("Compare the duration at each percentile. Compare with Latency Histogram to see transaction volume at duration intervals.")}/>
        </styles_1.HeaderTitleLegend>
        {this.renderComponent()}
      </React.Fragment>);
    };
    return DurationPercentileChart;
}(asyncComponent_1.default));
var StyledAreaChart = react_1.withTheme(function (_a) {
    var theme = _a.theme, props = tslib_1.__rest(_a, ["theme"]);
    return (<areaChart_1.default grid={{ left: '10px', right: '10px', top: '40px', bottom: '0px' }} xAxis={{
            type: 'category',
            truncate: true,
            axisLabel: {
                showMinLabel: true,
                showMaxLabel: true,
            },
            axisTick: {
                interval: 0,
                alignWithLabel: true,
            },
        }} yAxis={{
            type: 'value',
            axisLabel: {
                color: theme.chartLabel,
                // Use p50() to force time formatting.
                formatter: function (value) { return charts_1.axisLabelFormatter(value, 'p50()'); },
            },
        }} tooltip={{ valueFormatter: function (value) { return formatters_1.getDuration(value / 1000, 2); } }} {...props}/>);
});
var VALUE_EXTRACT_PATTERN = /(\d+)$/;
/**
 * Convert a discover response into a barchart compatible series
 */
function transformData(data) {
    var extractedData = Object.keys(data[0])
        .map(function (key) {
        var nameMatch = VALUE_EXTRACT_PATTERN.exec(key);
        if (!nameMatch) {
            return [-1, -1];
        }
        var nameValue = Number(nameMatch[1]);
        if (nameValue > 100) {
            nameValue /= 10;
        }
        return [nameValue, data[0][key]];
    })
        .filter(function (i) { return i[0] > 0; });
    extractedData.sort(function (a, b) {
        if (a[0] > b[0]) {
            return 1;
        }
        if (a[0] < b[0]) {
            return -1;
        }
        return 0;
    });
    return [
        {
            seriesName: locale_1.t('Duration'),
            data: extractedData.map(function (i) { return ({ value: i[1], name: i[0].toLocaleString() + "%" }); }),
        },
    ];
}
exports.default = DurationPercentileChart;
//# sourceMappingURL=durationPercentileChart.jsx.map