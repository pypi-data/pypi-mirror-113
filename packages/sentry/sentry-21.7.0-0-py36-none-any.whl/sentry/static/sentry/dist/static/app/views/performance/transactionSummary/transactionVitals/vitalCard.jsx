Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_2 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var throttle_1 = tslib_1.__importDefault(require("lodash/throttle"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var barChart_1 = tslib_1.__importDefault(require("app/components/charts/barChart"));
var barChartZoom_1 = tslib_1.__importDefault(require("app/components/charts/barChartZoom"));
var markLine_1 = tslib_1.__importDefault(require("app/components/charts/components/markLine"));
var transparentLoadingMask_1 = tslib_1.__importDefault(require("app/components/charts/transparentLoadingMask"));
var discoverButton_1 = tslib_1.__importDefault(require("app/components/discoverButton"));
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var fields_1 = require("app/utils/discover/fields");
var formatters_1 = require("app/utils/formatters");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var utils_1 = require("app/utils/performance/histogram/utils");
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var utils_2 = require("app/views/performance/transactionSummary/transactionEvents/utils");
var vitalsCards_1 = require("../../landing/vitalsCards");
var utils_3 = require("../../vitalDetail/utils");
var constants_1 = require("./constants");
var styles_1 = require("./styles");
var utils_4 = require("./utils");
var VitalCard = /** @class */ (function (_super) {
    tslib_1.__extends(VitalCard, _super);
    function VitalCard() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            refDataRect: null,
            refPixelRect: null,
        };
        _this.trackOpenInDiscoverClicked = function () {
            var organization = _this.props.organization;
            var vital = _this.props.vitalDetails;
            analytics_1.trackAnalyticsEvent({
                eventKey: 'performance_views.vitals.open_in_discover',
                eventName: 'Performance Views: Open vitals in discover',
                organization_id: organization.id,
                vital: vital.slug,
            });
        };
        _this.trackOpenAllEventsClicked = function () {
            var organization = _this.props.organization;
            var vital = _this.props.vitalDetails;
            analytics_1.trackAnalyticsEvent({
                eventKey: 'performance_views.vitals.open_all_events',
                eventName: 'Performance Views: Open vitals in all events',
                organization_id: organization.id,
                vital: vital.slug,
            });
        };
        /**
         * This callback happens everytime ECharts renders. This is NOT when ECharts
         * finishes rendering, so it can be called quite frequently. The calculations
         * here can get expensive if done frequently, furthermore, this can trigger a
         * state change leading to a re-render. So slow down the updates here as they
         * do not need to be updated every single time.
         */
        _this.handleRendered = throttle_1.default(function (_, chartRef) {
            var chartData = _this.props.chartData;
            var refDataRect = _this.state.refDataRect;
            if (refDataRect === null || chartData.length < 1) {
                return;
            }
            var refPixelRect = refDataRect === null ? null : utils_4.asPixelRect(chartRef, refDataRect);
            if (refPixelRect !== null && !isEqual_1.default(refPixelRect, _this.state.refPixelRect)) {
                _this.setState({ refPixelRect: refPixelRect });
            }
        }, 200, { leading: true });
        _this.handleDataZoomCancelled = function () { };
        return _this;
    }
    VitalCard.getDerivedStateFromProps = function (nextProps, prevState) {
        var isLoading = nextProps.isLoading, error = nextProps.error, chartData = nextProps.chartData;
        if (isLoading || error === null) {
            return tslib_1.__assign({}, prevState);
        }
        var refDataRect = utils_4.getRefRect(chartData);
        if (prevState.refDataRect === null ||
            (refDataRect !== null && !isEqual_1.default(refDataRect, prevState.refDataRect))) {
            return tslib_1.__assign(tslib_1.__assign({}, prevState), { refDataRect: refDataRect });
        }
        return tslib_1.__assign({}, prevState);
    };
    Object.defineProperty(VitalCard.prototype, "summary", {
        get: function () {
            var _a;
            var summaryData = this.props.summaryData;
            return (_a = summaryData === null || summaryData === void 0 ? void 0 : summaryData.p75) !== null && _a !== void 0 ? _a : null;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(VitalCard.prototype, "failureRate", {
        get: function () {
            var _a, _b;
            var summaryData = this.props.summaryData;
            var numerator = (_a = summaryData === null || summaryData === void 0 ? void 0 : summaryData.poor) !== null && _a !== void 0 ? _a : 0;
            var denominator = (_b = summaryData === null || summaryData === void 0 ? void 0 : summaryData.total) !== null && _b !== void 0 ? _b : 0;
            return denominator <= 0 ? 0 : numerator / denominator;
        },
        enumerable: false,
        configurable: true
    });
    VitalCard.prototype.getFormattedStatNumber = function () {
        var vital = this.props.vitalDetails;
        var summary = this.summary;
        var type = vital.type;
        return summary === null
            ? '\u2014'
            : type === 'duration'
                ? formatters_1.getDuration(summary / 1000, 2, true)
                : formatters_1.formatFloat(summary, 2);
    };
    VitalCard.prototype.renderSummary = function () {
        var _a;
        var _b = this.props, vital = _b.vitalDetails, eventView = _b.eventView, organization = _b.organization, min = _b.min, max = _b.max, dataFilter = _b.dataFilter;
        var slug = vital.slug, name = vital.name, description = vital.description;
        var hasPerformanceEventsPage = organization.features.includes('performance-events-page');
        var column = "measurements." + slug;
        var newEventView = eventView
            .withColumns([
            { kind: 'field', field: 'transaction' },
            {
                kind: 'function',
                function: ['percentile', column, constants_1.PERCENTILE.toString(), undefined],
            },
            { kind: 'function', function: ['count', '', '', undefined] },
        ])
            .withSorts([
            {
                kind: 'desc',
                field: fields_1.getAggregateAlias("percentile(" + column + "," + constants_1.PERCENTILE.toString() + ")"),
            },
        ]);
        var query = tokenizeSearch_1.tokenizeSearch((_a = newEventView.query) !== null && _a !== void 0 ? _a : '');
        query.addTagValues('has', [column]);
        // add in any range constraints if any
        if (min !== undefined || max !== undefined) {
            if (min !== undefined) {
                query.addTagValues(column, [">=" + min]);
            }
            if (max !== undefined) {
                query.addTagValues(column, ["<=" + max]);
            }
        }
        newEventView.query = query.formatString();
        return (<styles_1.CardSummary>
        <SummaryHeading>
          <styles_1.CardSectionHeading>{name + " (" + slug.toUpperCase() + ")"}</styles_1.CardSectionHeading>
        </SummaryHeading>
        <styles_1.StatNumber>
          {getDynamicText_1.default({
                value: this.getFormattedStatNumber(),
                fixed: '\u2014',
            })}
        </styles_1.StatNumber>
        <styles_1.Description>{description}</styles_1.Description>
        <div>
          {hasPerformanceEventsPage ? (<button_1.default size="small" to={newEventView
                    .withColumns([{ kind: 'field', field: column }])
                    .withSorts([{ kind: 'desc', field: column }])
                    .getPerformanceTransactionEventsViewUrlTarget(organization.slug, {
                    showTransactions: dataFilter === 'all'
                        ? utils_2.EventsDisplayFilterName.p100
                        : utils_2.EventsDisplayFilterName.p75,
                    webVital: column,
                })} onClick={this.trackOpenAllEventsClicked}>
              {locale_1.t('View All Events')}
            </button_1.default>) : (<discoverButton_1.default size="small" to={newEventView.getResultsViewUrlTarget(organization.slug)} onClick={this.trackOpenInDiscoverClicked}>
              {locale_1.t('Open in Discover')}
            </discoverButton_1.default>)}
        </div>
      </styles_1.CardSummary>);
    };
    VitalCard.prototype.renderHistogram = function () {
        var _a;
        var _this = this;
        var _b = this.props, theme = _b.theme, location = _b.location, isLoading = _b.isLoading, chartData = _b.chartData, summaryData = _b.summaryData, error = _b.error, colors = _b.colors, vital = _b.vital, vitalDetails = _b.vitalDetails, _c = _b.precision, precision = _c === void 0 ? 0 : _c;
        var slug = vitalDetails.slug;
        var series = this.getSeries();
        var xAxis = {
            type: 'category',
            truncate: true,
            axisTick: {
                alignWithLabel: true,
            },
        };
        var values = series.data.map(function (point) { return point.value; });
        var max = values.length ? Math.max.apply(Math, tslib_1.__spreadArray([], tslib_1.__read(values))) : undefined;
        var yAxis = {
            type: 'value',
            max: max,
            axisLabel: {
                color: theme.chartLabel,
                formatter: formatters_1.formatAbbreviatedNumber,
            },
        };
        var allSeries = [series];
        if (!isLoading && !error) {
            var baselineSeries = this.getBaselineSeries();
            if (baselineSeries !== null) {
                allSeries.push(baselineSeries);
            }
        }
        var vitalData = !isLoading && !error && summaryData !== null ? (_a = {}, _a[vital] = summaryData, _a) : {};
        return (<barChartZoom_1.default minZoomWidth={Math.pow(10, -precision) * constants_1.NUM_BUCKETS} location={location} paramStart={slug + "Start"} paramEnd={slug + "End"} xAxisIndex={[0]} buckets={utils_1.computeBuckets(chartData)} onDataZoomCancelled={this.handleDataZoomCancelled}>
        {function (zoomRenderProps) { return (<Container>
            <transparentLoadingMask_1.default visible={isLoading}/>
            <PercentContainer>
              <vitalsCards_1.VitalBar isLoading={isLoading} data={vitalData} vital={vital} showBar={false} showStates={false} showVitalPercentNames={false} showDurationDetail={false}/>
            </PercentContainer>
            {getDynamicText_1.default({
                    value: (<barChart_1.default series={allSeries} xAxis={xAxis} yAxis={yAxis} colors={colors} onRendered={_this.handleRendered} grid={{
                            left: space_1.default(3),
                            right: space_1.default(3),
                            top: space_1.default(3),
                            bottom: space_1.default(1.5),
                        }} stacked {...zoomRenderProps}/>),
                    fixed: <placeholder_1.default testId="skeleton-ui" height="200px"/>,
                })}
          </Container>); }}
      </barChartZoom_1.default>);
    };
    VitalCard.prototype.bucketWidth = function () {
        var chartData = this.props.chartData;
        // We can assume that all buckets are of equal width, use the first two
        // buckets to get the width. The value of each histogram function indicates
        // the beginning of the bucket.
        return chartData.length >= 2 ? chartData[1].bin - chartData[0].bin : 0;
    };
    VitalCard.prototype.getSeries = function () {
        var _this = this;
        var _a = this.props, theme = _a.theme, chartData = _a.chartData, precision = _a.precision, vitalDetails = _a.vitalDetails, vital = _a.vital;
        var additionalFieldsFn = function (bucket) {
            return {
                itemStyle: { color: theme[_this.getVitalsColor(vital, bucket)] },
            };
        };
        var data = utils_1.formatHistogramData(chartData, {
            precision: precision === 0 ? undefined : precision,
            type: vitalDetails.type,
            additionalFieldsFn: additionalFieldsFn,
        });
        return {
            seriesName: locale_1.t('Count'),
            data: data,
        };
    };
    VitalCard.prototype.getVitalsColor = function (vital, value) {
        var poorThreshold = utils_3.webVitalPoor[vital];
        var mehThreshold = utils_3.webVitalMeh[vital];
        if (value >= poorThreshold) {
            return utils_3.vitalStateColors[utils_3.VitalState.POOR];
        }
        else if (value >= mehThreshold) {
            return utils_3.vitalStateColors[utils_3.VitalState.MEH];
        }
        else {
            return utils_3.vitalStateColors[utils_3.VitalState.GOOD];
        }
    };
    VitalCard.prototype.getBaselineSeries = function () {
        var _a = this.props, theme = _a.theme, chartData = _a.chartData;
        var summary = this.summary;
        if (summary === null || this.state.refPixelRect === null) {
            return null;
        }
        var summaryBucket = utils_4.findNearestBucketIndex(chartData, summary);
        if (summaryBucket === null || summaryBucket === -1) {
            return null;
        }
        var thresholdPixelBottom = utils_4.mapPoint({
            // subtract 0.5 from the x here to ensure that the threshold lies between buckets
            x: summaryBucket - 0.5,
            y: 0,
        }, this.state.refDataRect, this.state.refPixelRect);
        if (thresholdPixelBottom === null) {
            return null;
        }
        var thresholdPixelTop = utils_4.mapPoint({
            // subtract 0.5 from the x here to ensure that the threshold lies between buckets
            x: summaryBucket - 0.5,
            y: Math.max.apply(Math, tslib_1.__spreadArray([], tslib_1.__read(chartData.map(function (data) { return data.count; })))) || 1,
        }, this.state.refDataRect, this.state.refPixelRect);
        if (thresholdPixelTop === null) {
            return null;
        }
        var markLine = markLine_1.default({
            animationDuration: 200,
            data: [[thresholdPixelBottom, thresholdPixelTop]],
            label: {
                show: false,
            },
            lineStyle: {
                color: theme.textColor,
                type: 'solid',
            },
        });
        // TODO(tonyx): This conflicts with the types declaration of `MarkLine`
        // if we add it in the constructor. So we opt to add it here so typescript
        // doesn't complain.
        markLine.tooltip = {
            formatter: function () {
                return [
                    '<div class="tooltip-series tooltip-series-solo">',
                    '<span class="tooltip-label">',
                    "<strong>" + locale_1.t('p75') + "</strong>",
                    '</span>',
                    '</div>',
                    '<div class="tooltip-arrow"></div>',
                ].join('');
            },
        };
        return {
            seriesName: locale_1.t('p75'),
            data: [],
            markLine: markLine,
        };
    };
    VitalCard.prototype.render = function () {
        return (<styles_1.Card>
        {this.renderSummary()}
        {this.renderHistogram()}
      </styles_1.Card>);
    };
    return VitalCard;
}(react_1.Component));
var SummaryHeading = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n"], ["\n  display: flex;\n  justify-content: space-between;\n"])));
var Container = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var PercentContainer = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  top: ", ";\n  right: ", ";\n  z-index: 2;\n"], ["\n  position: absolute;\n  top: ", ";\n  right: ", ";\n  z-index: 2;\n"])), space_1.default(2), space_1.default(3));
exports.default = react_2.withTheme(VitalCard);
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=vitalCard.jsx.map