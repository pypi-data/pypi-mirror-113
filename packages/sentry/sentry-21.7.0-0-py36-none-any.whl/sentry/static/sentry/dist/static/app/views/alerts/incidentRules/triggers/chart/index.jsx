var _a, _b;
Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var chunk_1 = tslib_1.__importDefault(require("lodash/chunk"));
var maxBy_1 = tslib_1.__importDefault(require("lodash/maxBy"));
var events_1 = require("app/actionCreators/events");
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var eventsRequest_1 = tslib_1.__importDefault(require("app/components/charts/eventsRequest"));
var optionSelector_1 = tslib_1.__importDefault(require("app/components/charts/optionSelector"));
var styles_1 = require("app/components/charts/styles");
var loadingMask_1 = tslib_1.__importDefault(require("app/components/loadingMask"));
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var types_1 = require("../../types");
var thresholdsChart_1 = tslib_1.__importDefault(require("./thresholdsChart"));
var TIME_PERIOD_MAP = (_a = {},
    _a[types_1.TimePeriod.SIX_HOURS] = locale_1.t('Last 6 hours'),
    _a[types_1.TimePeriod.ONE_DAY] = locale_1.t('Last 24 hours'),
    _a[types_1.TimePeriod.THREE_DAYS] = locale_1.t('Last 3 days'),
    _a[types_1.TimePeriod.SEVEN_DAYS] = locale_1.t('Last 7 days'),
    _a[types_1.TimePeriod.FOURTEEN_DAYS] = locale_1.t('Last 14 days'),
    _a[types_1.TimePeriod.THIRTY_DAYS] = locale_1.t('Last 30 days'),
    _a);
/**
 * If TimeWindow is small we want to limit the stats period
 * If the time window is one day we want to use a larger stats period
 */
var AVAILABLE_TIME_PERIODS = (_b = {},
    _b[types_1.TimeWindow.ONE_MINUTE] = [
        types_1.TimePeriod.SIX_HOURS,
        types_1.TimePeriod.ONE_DAY,
        types_1.TimePeriod.THREE_DAYS,
        types_1.TimePeriod.SEVEN_DAYS,
    ],
    _b[types_1.TimeWindow.FIVE_MINUTES] = [
        types_1.TimePeriod.ONE_DAY,
        types_1.TimePeriod.THREE_DAYS,
        types_1.TimePeriod.SEVEN_DAYS,
        types_1.TimePeriod.FOURTEEN_DAYS,
        types_1.TimePeriod.THIRTY_DAYS,
    ],
    _b[types_1.TimeWindow.TEN_MINUTES] = [
        types_1.TimePeriod.ONE_DAY,
        types_1.TimePeriod.THREE_DAYS,
        types_1.TimePeriod.SEVEN_DAYS,
        types_1.TimePeriod.FOURTEEN_DAYS,
        types_1.TimePeriod.THIRTY_DAYS,
    ],
    _b[types_1.TimeWindow.FIFTEEN_MINUTES] = [
        types_1.TimePeriod.THREE_DAYS,
        types_1.TimePeriod.SEVEN_DAYS,
        types_1.TimePeriod.FOURTEEN_DAYS,
        types_1.TimePeriod.THIRTY_DAYS,
    ],
    _b[types_1.TimeWindow.THIRTY_MINUTES] = [
        types_1.TimePeriod.SEVEN_DAYS,
        types_1.TimePeriod.FOURTEEN_DAYS,
        types_1.TimePeriod.THIRTY_DAYS,
    ],
    _b[types_1.TimeWindow.ONE_HOUR] = [types_1.TimePeriod.FOURTEEN_DAYS, types_1.TimePeriod.THIRTY_DAYS],
    _b[types_1.TimeWindow.TWO_HOURS] = [types_1.TimePeriod.THIRTY_DAYS],
    _b[types_1.TimeWindow.FOUR_HOURS] = [types_1.TimePeriod.THIRTY_DAYS],
    _b[types_1.TimeWindow.ONE_DAY] = [types_1.TimePeriod.THIRTY_DAYS],
    _b);
var AGGREGATE_FUNCTIONS = {
    avg: function (seriesChunk) {
        return AGGREGATE_FUNCTIONS.sum(seriesChunk) / seriesChunk.length;
    },
    sum: function (seriesChunk) {
        return seriesChunk.reduce(function (acc, series) { return acc + series.value; }, 0);
    },
    max: function (seriesChunk) {
        return Math.max.apply(Math, tslib_1.__spreadArray([], tslib_1.__read(seriesChunk.map(function (series) { return series.value; }))));
    },
    min: function (seriesChunk) {
        return Math.min.apply(Math, tslib_1.__spreadArray([], tslib_1.__read(seriesChunk.map(function (series) { return series.value; }))));
    },
};
/**
 * Determines the number of datapoints to roll up
 */
var getBucketSize = function (timeWindow, dataPoints) {
    var e_1, _a;
    var MAX_DPS = 720;
    try {
        for (var _b = tslib_1.__values([5, 10, 15, 30, 60, 120, 240]), _c = _b.next(); !_c.done; _c = _b.next()) {
            var bucketSize = _c.value;
            var chunkSize = bucketSize / timeWindow;
            if (dataPoints / chunkSize <= MAX_DPS) {
                return bucketSize / timeWindow;
            }
        }
    }
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
        }
        finally { if (e_1) throw e_1.error; }
    }
    return 2;
};
/**
 * This is a chart to be used in Metric Alert rules that fetches events based on
 * query, timewindow, and aggregations.
 */
var TriggersChart = /** @class */ (function (_super) {
    tslib_1.__extends(TriggersChart, _super);
    function TriggersChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            statsPeriod: types_1.TimePeriod.ONE_DAY,
            totalEvents: null,
        };
        _this.handleStatsPeriodChange = function (timePeriod) {
            _this.setState({ statsPeriod: timePeriod });
        };
        _this.getStatsPeriod = function () {
            var statsPeriod = _this.state.statsPeriod;
            var timeWindow = _this.props.timeWindow;
            var statsPeriodOptions = AVAILABLE_TIME_PERIODS[timeWindow];
            var period = statsPeriodOptions.includes(statsPeriod)
                ? statsPeriod
                : statsPeriodOptions[0];
            return period;
        };
        return _this;
    }
    TriggersChart.prototype.componentDidMount = function () {
        this.fetchTotalCount();
    };
    TriggersChart.prototype.componentDidUpdate = function (prevProps, prevState) {
        var _a = this.props, query = _a.query, environment = _a.environment, timeWindow = _a.timeWindow;
        var statsPeriod = this.state.statsPeriod;
        if (prevProps.environment !== environment ||
            prevProps.query !== query ||
            prevProps.timeWindow !== timeWindow ||
            prevState.statsPeriod !== statsPeriod) {
            this.fetchTotalCount();
        }
    };
    TriggersChart.prototype.fetchTotalCount = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, api, organization, environment, projects, query, statsPeriod, totalEvents, e_2;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization, environment = _a.environment, projects = _a.projects, query = _a.query;
                        statsPeriod = this.getStatsPeriod();
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, events_1.fetchTotalCount(api, organization.slug, {
                                field: [],
                                project: projects.map(function (_a) {
                                    var id = _a.id;
                                    return id;
                                }),
                                query: query,
                                statsPeriod: statsPeriod,
                                environment: environment ? [environment] : [],
                            })];
                    case 2:
                        totalEvents = _b.sent();
                        this.setState({ totalEvents: totalEvents });
                        return [3 /*break*/, 4];
                    case 3:
                        e_2 = _b.sent();
                        this.setState({ totalEvents: null });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    TriggersChart.prototype.render = function () {
        var _this = this;
        var _a = this.props, api = _a.api, organization = _a.organization, projects = _a.projects, timeWindow = _a.timeWindow, query = _a.query, aggregate = _a.aggregate, triggers = _a.triggers, resolveThreshold = _a.resolveThreshold, thresholdType = _a.thresholdType, environment = _a.environment, header = _a.header;
        var _b = this.state, statsPeriod = _b.statsPeriod, totalEvents = _b.totalEvents;
        var statsPeriodOptions = AVAILABLE_TIME_PERIODS[timeWindow];
        var period = this.getStatsPeriod();
        return (<feature_1.default features={['metric-alert-builder-aggregate']} organization={organization}>
        {function (_a) {
                var hasFeature = _a.hasFeature;
                return (<eventsRequest_1.default api={api} organization={organization} query={query} environment={environment ? [environment] : undefined} project={projects.map(function (_a) {
                    var id = _a.id;
                    return Number(id);
                })} interval={timeWindow + "m"} period={period} yAxis={aggregate} includePrevious={false} currentSeriesName={aggregate} partial={false}>
              {function (_a) {
                        var _b;
                        var loading = _a.loading, reloading = _a.reloading, timeseriesData = _a.timeseriesData;
                        var maxValue;
                        var timeseriesLength;
                        if (((_b = timeseriesData === null || timeseriesData === void 0 ? void 0 : timeseriesData[0]) === null || _b === void 0 ? void 0 : _b.data) !== undefined) {
                            maxValue = maxBy_1.default(timeseriesData[0].data, function (_a) {
                                var value = _a.value;
                                return value;
                            });
                            timeseriesLength = timeseriesData[0].data.length;
                            if (hasFeature && timeseriesLength > 600) {
                                var avgData_1 = [];
                                var minData_1 = [];
                                var maxData_1 = [];
                                var chunkSize = getBucketSize(timeWindow, timeseriesData[0].data.length);
                                chunk_1.default(timeseriesData[0].data, chunkSize).forEach(function (seriesChunk) {
                                    avgData_1.push({
                                        name: seriesChunk[0].name,
                                        value: AGGREGATE_FUNCTIONS.avg(seriesChunk),
                                    });
                                    minData_1.push({
                                        name: seriesChunk[0].name,
                                        value: AGGREGATE_FUNCTIONS.min(seriesChunk),
                                    });
                                    maxData_1.push({
                                        name: seriesChunk[0].name,
                                        value: AGGREGATE_FUNCTIONS.max(seriesChunk),
                                    });
                                });
                                timeseriesData = [
                                    timeseriesData[0],
                                    { seriesName: locale_1.t('Minimum'), data: minData_1 },
                                    { seriesName: locale_1.t('Average'), data: avgData_1 },
                                    { seriesName: locale_1.t('Maximum'), data: maxData_1 },
                                ];
                            }
                        }
                        var chart = (<React.Fragment>
                    {header}
                    <TransparentLoadingMask visible={reloading}/>
                    {loading || reloading ? (<ChartPlaceholder />) : (<thresholdsChart_1.default period={statsPeriod} maxValue={maxValue ? maxValue.value : maxValue} data={timeseriesData} triggers={triggers} resolveThreshold={resolveThreshold} thresholdType={thresholdType}/>)}
                    <styles_1.ChartControls>
                      <styles_1.InlineContainer>
                        <React.Fragment>
                          <styles_1.SectionHeading>{locale_1.t('Total Events')}</styles_1.SectionHeading>
                          {totalEvents !== null ? (<styles_1.SectionValue>{totalEvents.toLocaleString()}</styles_1.SectionValue>) : (<styles_1.SectionValue>&mdash;</styles_1.SectionValue>)}
                        </React.Fragment>
                      </styles_1.InlineContainer>
                      <styles_1.InlineContainer>
                        <optionSelector_1.default options={statsPeriodOptions.map(function (timePeriod) { return ({
                                label: TIME_PERIOD_MAP[timePeriod],
                                value: timePeriod,
                                disabled: loading || reloading,
                            }); })} selected={period} onChange={_this.handleStatsPeriodChange} title={locale_1.t('Display')}/>
                      </styles_1.InlineContainer>
                    </styles_1.ChartControls>
                  </React.Fragment>);
                        return chart;
                    }}
            </eventsRequest_1.default>);
            }}
      </feature_1.default>);
    };
    return TriggersChart;
}(React.PureComponent));
exports.default = withApi_1.default(TriggersChart);
var TransparentLoadingMask = styled_1.default(loadingMask_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  ", ";\n  opacity: 0.4;\n  z-index: 1;\n"], ["\n  ", ";\n  opacity: 0.4;\n  z-index: 1;\n"])), function (p) { return !p.visible && 'display: none;'; });
var ChartPlaceholder = styled_1.default(placeholder_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  /* Height and margin should add up to graph size (200px) */\n  margin: 0 0 ", ";\n  height: 184px;\n"], ["\n  /* Height and margin should add up to graph size (200px) */\n  margin: 0 0 ", ";\n  height: 184px;\n"])), space_1.default(2));
var templateObject_1, templateObject_2;
//# sourceMappingURL=index.jsx.map