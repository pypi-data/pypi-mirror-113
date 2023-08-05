Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var areaChart_1 = tslib_1.__importDefault(require("app/components/charts/areaChart"));
var barChart_1 = tslib_1.__importDefault(require("app/components/charts/barChart"));
var eventsRequest_1 = tslib_1.__importDefault(require("app/components/charts/eventsRequest"));
var lineChart_1 = tslib_1.__importDefault(require("app/components/charts/lineChart"));
var utils_1 = require("app/components/charts/utils");
var loadingContainer_1 = tslib_1.__importDefault(require("app/components/loading/loadingContainer"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var icons_1 = require("app/icons");
var dates_1 = require("app/utils/dates");
var charts_1 = require("app/utils/discover/charts");
var fields_1 = require("app/utils/discover/fields");
var types_1 = require("app/utils/discover/types");
var queryString_1 = require("app/utils/queryString");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var MiniGraph = /** @class */ (function (_super) {
    tslib_1.__extends(MiniGraph, _super);
    function MiniGraph() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    MiniGraph.prototype.shouldComponentUpdate = function (nextProps) {
        // We pay for the cost of the deep comparison here since it is cheaper
        // than the cost for rendering the graph, which can take ~200ms to ~300ms to
        // render.
        return !isEqual_1.default(this.getRefreshProps(this.props), this.getRefreshProps(nextProps));
    };
    MiniGraph.prototype.getRefreshProps = function (props) {
        // get props that are relevant to the API payload for the graph
        var organization = props.organization, location = props.location, eventView = props.eventView;
        var apiPayload = eventView.getEventsAPIPayload(location);
        var query = apiPayload.query;
        var start = apiPayload.start ? dates_1.getUtcToLocalDateObject(apiPayload.start) : null;
        var end = apiPayload.end ? dates_1.getUtcToLocalDateObject(apiPayload.end) : null;
        var period = apiPayload.statsPeriod;
        var display = eventView.getDisplayMode();
        var isTopEvents = display === types_1.DisplayModes.TOP5 || display === types_1.DisplayModes.DAILYTOP5;
        var isDaily = display === types_1.DisplayModes.DAILYTOP5 || display === types_1.DisplayModes.DAILY;
        var field = isTopEvents ? apiPayload.field : undefined;
        var topEvents = isTopEvents ? types_1.TOP_N : undefined;
        var orderby = isTopEvents ? queryString_1.decodeScalar(apiPayload.sort) : undefined;
        var interval = isDaily ? '1d' : utils_1.getInterval({ start: start, end: end, period: period }, true);
        return {
            organization: organization,
            apiPayload: apiPayload,
            query: query,
            start: start,
            end: end,
            period: period,
            interval: interval,
            project: eventView.project,
            environment: eventView.environment,
            yAxis: eventView.getYAxis(),
            field: field,
            topEvents: topEvents,
            orderby: orderby,
            showDaily: isDaily,
            expired: eventView.expired,
            name: eventView.name,
        };
    };
    MiniGraph.prototype.getChartType = function (_a) {
        var showDaily = _a.showDaily, yAxis = _a.yAxis, timeseriesData = _a.timeseriesData;
        if (showDaily) {
            return 'bar';
        }
        if (timeseriesData.length > 1) {
            switch (fields_1.aggregateMultiPlotType(yAxis)) {
                case 'line':
                    return 'line';
                case 'area':
                    return 'area';
                default:
                    throw new Error("Unknown multi plot type for " + yAxis);
            }
        }
        return 'area';
    };
    MiniGraph.prototype.getChartComponent = function (chartType) {
        switch (chartType) {
            case 'bar':
                return barChart_1.default;
            case 'line':
                return lineChart_1.default;
            case 'area':
                return areaChart_1.default;
            default:
                throw new Error("Unknown multi plot type for " + chartType);
        }
    };
    MiniGraph.prototype.render = function () {
        var _this = this;
        var _a = this.props, theme = _a.theme, api = _a.api;
        var _b = this.getRefreshProps(this.props), query = _b.query, start = _b.start, end = _b.end, period = _b.period, interval = _b.interval, organization = _b.organization, project = _b.project, environment = _b.environment, yAxis = _b.yAxis, field = _b.field, topEvents = _b.topEvents, orderby = _b.orderby, showDaily = _b.showDaily, expired = _b.expired, name = _b.name;
        return (<eventsRequest_1.default organization={organization} api={api} query={query} start={start} end={end} period={period} interval={interval} project={project} environment={environment} includePrevious={false} yAxis={yAxis} field={field} topEvents={topEvents} orderby={orderby} expired={expired} name={name} partial>
        {function (_a) {
                var _b;
                var loading = _a.loading, timeseriesData = _a.timeseriesData, results = _a.results, errored = _a.errored;
                if (errored) {
                    return (<StyledGraphContainer>
                <icons_1.IconWarning color="gray300" size="md"/>
              </StyledGraphContainer>);
                }
                if (loading) {
                    return (<StyledGraphContainer>
                <loadingIndicator_1.default mini/>
              </StyledGraphContainer>);
                }
                var allSeries = (_b = timeseriesData !== null && timeseriesData !== void 0 ? timeseriesData : results) !== null && _b !== void 0 ? _b : [];
                var chartType = _this.getChartType({
                    showDaily: showDaily,
                    yAxis: yAxis,
                    timeseriesData: allSeries,
                });
                var data = allSeries.map(function (series) { return (tslib_1.__assign(tslib_1.__assign({}, series), { lineStyle: {
                        opacity: chartType === 'line' ? 1 : 0,
                    }, smooth: true })); });
                var chartOptions = {
                    colors: allSeries.length
                        ? tslib_1.__spreadArray([], tslib_1.__read(theme.charts.getColorPalette(allSeries.length - 2))) : undefined,
                    height: 100,
                    series: tslib_1.__spreadArray([], tslib_1.__read(data)),
                    xAxis: {
                        show: false,
                        axisPointer: {
                            show: false,
                        },
                    },
                    yAxis: {
                        show: true,
                        axisLine: {
                            show: false,
                        },
                        axisLabel: {
                            color: theme.chartLabel,
                            fontFamily: theme.text.family,
                            fontSize: 12,
                            formatter: function (value) { return charts_1.axisLabelFormatter(value, yAxis, true); },
                            inside: true,
                            showMinLabel: false,
                            showMaxLabel: false,
                        },
                        splitNumber: 3,
                        splitLine: {
                            show: false,
                        },
                        zlevel: theme.zIndex.header,
                    },
                    tooltip: {
                        show: false,
                    },
                    toolBox: {
                        show: false,
                    },
                    grid: {
                        left: 0,
                        top: 0,
                        right: 0,
                        bottom: 0,
                        containLabel: false,
                    },
                    stacked: typeof topEvents === 'number' && topEvents > 0,
                };
                var Component = _this.getChartComponent(chartType);
                return <Component {...chartOptions}/>;
            }}
      </eventsRequest_1.default>);
    };
    return MiniGraph;
}(React.Component));
var StyledGraphContainer = styled_1.default(function (props) { return (<loadingContainer_1.default {...props} maskBackgroundColor="transparent"/>); })(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  height: 100px;\n\n  display: flex;\n  justify-content: center;\n  align-items: center;\n"], ["\n  height: 100px;\n\n  display: flex;\n  justify-content: center;\n  align-items: center;\n"])));
exports.default = withApi_1.default(react_1.withTheme(MiniGraph));
var templateObject_1;
//# sourceMappingURL=miniGraph.jsx.map