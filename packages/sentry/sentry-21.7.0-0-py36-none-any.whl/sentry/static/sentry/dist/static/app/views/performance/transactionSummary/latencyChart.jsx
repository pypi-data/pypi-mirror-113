Object.defineProperty(exports, "__esModule", { value: true });
exports.decodeHistogramZoom = exports.LatencyChartControls = exports.ZOOM_END = exports.ZOOM_START = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var barChart_1 = tslib_1.__importDefault(require("app/components/charts/barChart"));
var barChartZoom_1 = tslib_1.__importDefault(require("app/components/charts/barChartZoom"));
var errorPanel_1 = tslib_1.__importDefault(require("app/components/charts/errorPanel"));
var loadingPanel_1 = tslib_1.__importDefault(require("app/components/charts/loadingPanel"));
var optionSelector_1 = tslib_1.__importDefault(require("app/components/charts/optionSelector"));
var styles_1 = require("app/components/charts/styles");
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var analytics_1 = require("app/utils/analytics");
var eventView_1 = tslib_1.__importDefault(require("app/utils/discover/eventView"));
var histogram_1 = tslib_1.__importDefault(require("app/utils/performance/histogram"));
var histogramQuery_1 = tslib_1.__importDefault(require("app/utils/performance/histogram/histogramQuery"));
var utils_1 = require("app/utils/performance/histogram/utils");
var queryString_1 = require("app/utils/queryString");
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var filter_1 = require("./filter");
exports.ZOOM_START = 'startDuration';
exports.ZOOM_END = 'endDuration';
var NUM_BUCKETS = 50;
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
 * for each duration bucket. We always render 50 buckets of
 * equal widths based on the endpoints min + max durations.
 *
 * This graph visualizes how many transactions were recorded
 * at each duration bucket, showing the modality of the transaction.
 */
var LatencyChart = /** @class */ (function (_super) {
    tslib_1.__extends(LatencyChart, _super);
    function LatencyChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            zoomError: false,
        };
        _this.handleMouseOver = function () {
            // Hide the zoom error tooltip on the next hover.
            if (_this.state.zoomError) {
                _this.setState({ zoomError: false });
            }
        };
        _this.handleDataZoom = function () {
            var organization = _this.props.organization;
            analytics_1.trackAnalyticsEvent({
                eventKey: 'performance_views.latency_chart.zoom',
                eventName: 'Performance Views: Transaction Summary Latency Chart Zoom',
                organization_id: parseInt(organization.id, 10),
            });
        };
        _this.handleDataZoomCancelled = function () {
            _this.setState({ zoomError: true });
        };
        return _this;
    }
    LatencyChart.prototype.bucketWidth = function (data) {
        // We can assume that all buckets are of equal width, use the first two
        // buckets to get the width. The value of each histogram function indicates
        // the beginning of the bucket.
        return data.length > 2 ? data[1].bin - data[0].bin : 0;
    };
    LatencyChart.prototype.renderLoading = function () {
        return <loadingPanel_1.default data-test-id="histogram-loading"/>;
    };
    LatencyChart.prototype.renderError = function () {
        // Don't call super as we don't really need issues for this.
        return (<errorPanel_1.default>
        <icons_1.IconWarning color="gray300" size="lg"/>
      </errorPanel_1.default>);
    };
    LatencyChart.prototype.renderChart = function (data) {
        var _this = this;
        var _a = this.props, location = _a.location, currentFilter = _a.currentFilter;
        var zoomError = this.state.zoomError;
        var xAxis = {
            type: 'category',
            truncate: true,
            axisTick: {
                interval: 0,
                alignWithLabel: true,
            },
        };
        var colors = currentFilter === filter_1.SpanOperationBreakdownFilter.None
            ? tslib_1.__spreadArray([], tslib_1.__read(theme_1.default.charts.getColorPalette(1))) : [filter_1.filterToColour(currentFilter)];
        // Use a custom tooltip formatter as we need to replace
        // the tooltip content entirely when zooming is no longer available.
        var tooltip = {
            formatter: function (series) {
                var seriesData = Array.isArray(series) ? series : [series];
                var contents = [];
                if (!zoomError) {
                    // Replicate the necessary logic from app/components/charts/components/tooltip.jsx
                    contents = seriesData.map(function (item) {
                        var label = item.seriesName;
                        var value = item.value[1].toLocaleString();
                        return [
                            '<div class="tooltip-series">',
                            "<div><span class=\"tooltip-label\">" + item.marker + " <strong>" + label + "</strong></span> " + value + "</div>",
                            '</div>',
                        ].join('');
                    });
                    var seriesLabel = seriesData[0].value[0];
                    contents.push("<div class=\"tooltip-date\">" + seriesLabel + "</div>");
                }
                else {
                    contents = [
                        '<div class="tooltip-series tooltip-series-solo">',
                        locale_1.t('Target zoom region too small'),
                        '</div>',
                    ];
                }
                contents.push('<div class="tooltip-arrow"></div>');
                return contents.join('');
            },
        };
        var series = {
            seriesName: locale_1.t('Count'),
            data: utils_1.formatHistogramData(data, { type: 'duration' }),
        };
        return (<barChartZoom_1.default minZoomWidth={NUM_BUCKETS} location={location} paramStart={exports.ZOOM_START} paramEnd={exports.ZOOM_END} xAxisIndex={[0]} buckets={utils_1.computeBuckets(data)} onDataZoomCancelled={this.handleDataZoomCancelled}>
        {function (zoomRenderProps) { return (<barChart_1.default grid={{ left: '10px', right: '10px', top: '40px', bottom: '0px' }} xAxis={xAxis} yAxis={{ type: 'value' }} series={[series]} tooltip={tooltip} colors={colors} onMouseOver={_this.handleMouseOver} {...zoomRenderProps}/>); }}
      </barChartZoom_1.default>);
    };
    LatencyChart.prototype.render = function () {
        var _this = this;
        var _a;
        var _b = this.props, organization = _b.organization, query = _b.query, start = _b.start, end = _b.end, statsPeriod = _b.statsPeriod, environment = _b.environment, project = _b.project, location = _b.location, currentFilter = _b.currentFilter;
        var eventView = eventView_1.default.fromNewQueryWithLocation({
            id: undefined,
            version: 2,
            name: '',
            fields: ['transaction.duration'],
            projects: project,
            range: statsPeriod,
            query: query,
            environment: environment,
            start: start,
            end: end,
        }, location);
        var _c = decodeHistogramZoom(location), min = _c.min, max = _c.max;
        var field = (_a = filter_1.filterToField(currentFilter)) !== null && _a !== void 0 ? _a : 'transaction.duration';
        var headerTitle = currentFilter === filter_1.SpanOperationBreakdownFilter.None
            ? locale_1.t('Duration Distribution')
            : locale_1.tct('Span Operation Distribution - [operationName]', {
                operationName: currentFilter,
            });
        return (<react_1.Fragment>
        <styles_1.HeaderTitleLegend>
          {headerTitle}
          <questionTooltip_1.default position="top" size="sm" title={locale_1.t("Duration Distribution reflects the volume of transactions per median duration.")}/>
        </styles_1.HeaderTitleLegend>
        <histogram_1.default location={location} zoomKeys={[exports.ZOOM_START, exports.ZOOM_END]}>
          {function (_a) {
                var activeFilter = _a.activeFilter;
                return (<histogramQuery_1.default location={location} orgSlug={organization.slug} eventView={eventView} numBuckets={NUM_BUCKETS} fields={[field]} min={min} max={max} dataFilter={activeFilter.value}>
              {function (_a) {
                        var _b;
                        var histograms = _a.histograms, isLoading = _a.isLoading, error = _a.error;
                        if (isLoading) {
                            return _this.renderLoading();
                        }
                        else if (error) {
                            return _this.renderError();
                        }
                        var data = (_b = histograms === null || histograms === void 0 ? void 0 : histograms[field]) !== null && _b !== void 0 ? _b : [];
                        return _this.renderChart(data);
                    }}
            </histogramQuery_1.default>);
            }}
        </histogram_1.default>
      </react_1.Fragment>);
    };
    return LatencyChart;
}(react_1.Component));
function LatencyChartControls(props) {
    var location = props.location;
    return (<histogram_1.default location={location} zoomKeys={[exports.ZOOM_START, exports.ZOOM_END]}>
      {function (_a) {
            var filterOptions = _a.filterOptions, handleFilterChange = _a.handleFilterChange, activeFilter = _a.activeFilter;
            return (<react_1.Fragment>
            <optionSelector_1.default title={locale_1.t('Outliers')} selected={activeFilter.value} options={filterOptions} onChange={handleFilterChange}/>
          </react_1.Fragment>);
        }}
    </histogram_1.default>);
}
exports.LatencyChartControls = LatencyChartControls;
function decodeHistogramZoom(location) {
    var min = undefined;
    var max = undefined;
    if (exports.ZOOM_START in location.query) {
        min = queryString_1.decodeInteger(location.query[exports.ZOOM_START], 0);
    }
    if (exports.ZOOM_END in location.query) {
        var decodedMax = queryString_1.decodeInteger(location.query[exports.ZOOM_END]);
        if (typeof decodedMax === 'number') {
            max = decodedMax;
        }
    }
    return { min: min, max: max };
}
exports.decodeHistogramZoom = decodeHistogramZoom;
exports.default = LatencyChart;
//# sourceMappingURL=latencyChart.jsx.map