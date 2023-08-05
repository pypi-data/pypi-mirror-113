Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var omit_1 = tslib_1.__importDefault(require("lodash/omit"));
var indicator_1 = require("app/actionCreators/indicator");
var utils_1 = require("app/components/charts/utils");
var getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
var locale_1 = require("app/locale");
var utils_2 = require("app/utils");
var getPeriod_1 = require("app/utils/getPeriod");
var utils_3 = require("app/views/releases/detail/overview/chart/utils");
var utils_4 = require("app/views/releases/utils");
var projectCharts_1 = require("../projectCharts");
var utils_5 = require("../utils");
var omitIgnoredProps = function (props) {
    return omit_1.default(props, ['api', 'organization', 'children', 'selection.datetime.utc']);
};
var SessionsRequest = /** @class */ (function (_super) {
    tslib_1.__extends(SessionsRequest, _super);
    function SessionsRequest() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            reloading: false,
            errored: false,
            timeseriesData: null,
            previousTimeseriesData: null,
            totalSessions: null,
        };
        _this.unmounting = false;
        _this.fetchData = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, api, selection, onTotalValuesChange, displayMode, disablePrevious, shouldFetchWithPrevious, response, _b, timeseriesData, previousTimeseriesData, totalSessions, _c;
            return tslib_1.__generator(this, function (_d) {
                switch (_d.label) {
                    case 0:
                        _a = this.props, api = _a.api, selection = _a.selection, onTotalValuesChange = _a.onTotalValuesChange, displayMode = _a.displayMode, disablePrevious = _a.disablePrevious;
                        shouldFetchWithPrevious = !disablePrevious && utils_5.shouldFetchPreviousPeriod(selection.datetime);
                        this.setState(function (state) { return ({
                            reloading: state.timeseriesData !== null,
                            errored: false,
                        }); });
                        _d.label = 1;
                    case 1:
                        _d.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise(this.path, {
                                query: this.queryParams({ shouldFetchWithPrevious: shouldFetchWithPrevious }),
                            })];
                    case 2:
                        response = _d.sent();
                        _b = displayMode === projectCharts_1.DisplayModes.SESSIONS
                            ? this.transformSessionCountData(response)
                            : this.transformData(response, { fetchedWithPrevious: shouldFetchWithPrevious }), timeseriesData = _b.timeseriesData, previousTimeseriesData = _b.previousTimeseriesData, totalSessions = _b.totalSessions;
                        if (this.unmounting) {
                            return [2 /*return*/];
                        }
                        this.setState({
                            reloading: false,
                            timeseriesData: timeseriesData,
                            previousTimeseriesData: previousTimeseriesData,
                            totalSessions: totalSessions,
                        });
                        onTotalValuesChange(totalSessions);
                        return [3 /*break*/, 4];
                    case 3:
                        _c = _d.sent();
                        indicator_1.addErrorMessage(locale_1.t('Error loading chart data'));
                        this.setState({
                            errored: true,
                            reloading: false,
                            timeseriesData: null,
                            previousTimeseriesData: null,
                            totalSessions: null,
                        });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    SessionsRequest.prototype.componentDidMount = function () {
        this.fetchData();
    };
    SessionsRequest.prototype.componentDidUpdate = function (prevProps) {
        if (!isEqual_1.default(omitIgnoredProps(this.props), omitIgnoredProps(prevProps))) {
            this.fetchData();
        }
    };
    SessionsRequest.prototype.componentWillUnmount = function () {
        this.unmounting = true;
    };
    Object.defineProperty(SessionsRequest.prototype, "path", {
        get: function () {
            var organization = this.props.organization;
            return "/organizations/" + organization.slug + "/sessions/";
        },
        enumerable: false,
        configurable: true
    });
    SessionsRequest.prototype.queryParams = function (_a) {
        var _b = _a.shouldFetchWithPrevious, shouldFetchWithPrevious = _b === void 0 ? false : _b;
        var _c = this.props, selection = _c.selection, query = _c.query;
        var datetime = selection.datetime, projects = selection.projects, environment = selection.environments;
        var baseParams = {
            field: 'sum(session)',
            groupBy: 'session.status',
            interval: utils_1.getSeriesApiInterval(datetime),
            project: projects[0],
            environment: environment,
            query: query,
        };
        if (!shouldFetchWithPrevious) {
            return tslib_1.__assign(tslib_1.__assign({}, baseParams), getParams_1.getParams(datetime));
        }
        var period = selection.datetime.period;
        var doubledPeriod = getPeriod_1.getPeriod({ period: period, start: undefined, end: undefined }, { shouldDoublePeriod: true }).statsPeriod;
        return tslib_1.__assign(tslib_1.__assign({}, baseParams), { statsPeriod: doubledPeriod });
    };
    SessionsRequest.prototype.transformData = function (responseData, _a) {
        var _b = _a.fetchedWithPrevious, fetchedWithPrevious = _b === void 0 ? false : _b;
        var theme = this.props.theme;
        // Take the floor just in case, but data should always be divisible by 2
        var dataMiddleIndex = Math.floor(responseData.intervals.length / 2);
        // calculate the total number of sessions for this period (exclude previous if there)
        var totalSessions = responseData.groups.reduce(function (acc, group) {
            return acc +
                group.series['sum(session)']
                    .slice(fetchedWithPrevious ? dataMiddleIndex : 0)
                    .reduce(function (value, groupAcc) { return groupAcc + value; }, 0);
        }, 0);
        var previousPeriodTotalSessions = fetchedWithPrevious
            ? responseData.groups.reduce(function (acc, group) {
                return acc +
                    group.series['sum(session)']
                        .slice(0, dataMiddleIndex)
                        .reduce(function (value, groupAcc) { return groupAcc + value; }, 0);
            }, 0)
            : 0;
        // TODO(project-details): refactor this to avoid duplication as we add more session charts
        var timeseriesData = [
            {
                seriesName: locale_1.t('This Period'),
                color: theme.green300,
                data: responseData.intervals
                    .slice(fetchedWithPrevious ? dataMiddleIndex : 0)
                    .map(function (interval, i) {
                    var _a, _b;
                    var totalIntervalSessions = responseData.groups.reduce(function (acc, group) {
                        return acc +
                            group.series['sum(session)'].slice(fetchedWithPrevious ? dataMiddleIndex : 0)[i];
                    }, 0);
                    var intervalCrashedSessions = (_b = (_a = responseData.groups
                        .find(function (group) { return group.by['session.status'] === 'crashed'; })) === null || _a === void 0 ? void 0 : _a.series['sum(session)'].slice(fetchedWithPrevious ? dataMiddleIndex : 0)[i]) !== null && _b !== void 0 ? _b : 0;
                    var crashedSessionsPercent = utils_2.percent(intervalCrashedSessions, totalIntervalSessions);
                    return {
                        name: interval,
                        value: totalSessions === 0 && previousPeriodTotalSessions === 0
                            ? 0
                            : totalIntervalSessions === 0
                                ? null
                                : utils_4.getCrashFreePercent(100 - crashedSessionsPercent),
                    };
                }),
            },
        ]; // TODO(project-detail): Change SeriesDataUnit value to support null
        var previousTimeseriesData = fetchedWithPrevious
            ? {
                seriesName: locale_1.t('Previous Period'),
                data: responseData.intervals.slice(0, dataMiddleIndex).map(function (_interval, i) {
                    var _a, _b;
                    var totalIntervalSessions = responseData.groups.reduce(function (acc, group) {
                        return acc + group.series['sum(session)'].slice(0, dataMiddleIndex)[i];
                    }, 0);
                    var intervalCrashedSessions = (_b = (_a = responseData.groups
                        .find(function (group) { return group.by['session.status'] === 'crashed'; })) === null || _a === void 0 ? void 0 : _a.series['sum(session)'].slice(0, dataMiddleIndex)[i]) !== null && _b !== void 0 ? _b : 0;
                    var crashedSessionsPercent = utils_2.percent(intervalCrashedSessions, totalIntervalSessions);
                    return {
                        name: responseData.intervals[i + dataMiddleIndex],
                        value: totalSessions === 0 && previousPeriodTotalSessions === 0
                            ? 0
                            : totalIntervalSessions === 0
                                ? null
                                : utils_4.getCrashFreePercent(100 - crashedSessionsPercent),
                    };
                }),
            } // TODO(project-detail): Change SeriesDataUnit value to support null
            : null;
        return {
            totalSessions: totalSessions,
            timeseriesData: timeseriesData,
            previousTimeseriesData: previousTimeseriesData,
        };
    };
    SessionsRequest.prototype.transformSessionCountData = function (responseData) {
        var totalSessions = utils_3.getTotalsFromSessionsResponse({
            response: responseData,
            field: 'sum(session)',
        });
        var chartData = utils_3.fillChartDataFromSessionsResponse({
            response: responseData,
            field: 'sum(session)',
            groupBy: 'session.status',
            chartData: utils_3.initSessionsBreakdownChartData(),
        });
        return {
            timeseriesData: Object.values(chartData),
            previousTimeseriesData: null,
            totalSessions: totalSessions,
        };
    };
    SessionsRequest.prototype.render = function () {
        var children = this.props.children;
        var _a = this.state, timeseriesData = _a.timeseriesData, reloading = _a.reloading, errored = _a.errored, totalSessions = _a.totalSessions, previousTimeseriesData = _a.previousTimeseriesData;
        var loading = timeseriesData === null;
        return children({
            loading: loading,
            reloading: reloading,
            errored: errored,
            totalSessions: totalSessions,
            previousTimeseriesData: previousTimeseriesData,
            timeseriesData: timeseriesData !== null && timeseriesData !== void 0 ? timeseriesData : [],
        });
    };
    return SessionsRequest;
}(React.Component));
exports.default = react_1.withTheme(SessionsRequest);
//# sourceMappingURL=sessionsRequest.jsx.map