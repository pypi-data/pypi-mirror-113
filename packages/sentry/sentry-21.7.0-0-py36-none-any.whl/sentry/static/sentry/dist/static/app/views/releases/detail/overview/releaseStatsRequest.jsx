Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var meanBy_1 = tslib_1.__importDefault(require("lodash/meanBy"));
var omitBy_1 = tslib_1.__importDefault(require("lodash/omitBy"));
var pick_1 = tslib_1.__importDefault(require("lodash/pick"));
var events_1 = require("app/actionCreators/events");
var indicator_1 = require("app/actionCreators/indicator");
var getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
var globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
var locale_1 = require("app/locale");
var utils_1 = require("app/utils");
var formatters_1 = require("app/utils/formatters");
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var utils_2 = require("../../utils");
var releaseChartControls_1 = require("./chart/releaseChartControls");
var utils_3 = require("./chart/utils");
var omitIgnoredProps = function (props) {
    return omitBy_1.default(props, function (_, key) {
        return ['api', 'orgId', 'projectSlug', 'location', 'children'].includes(key);
    });
};
var ReleaseStatsRequest = /** @class */ (function (_super) {
    tslib_1.__extends(ReleaseStatsRequest, _super);
    function ReleaseStatsRequest() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            reloading: false,
            errored: false,
            data: null,
        };
        _this.unmounting = false;
        _this.fetchData = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var data, _a, yAxis, hasHealthData, hasDiscover, hasPerformance, error_1;
            var _b, _c;
            return tslib_1.__generator(this, function (_d) {
                switch (_d.label) {
                    case 0:
                        data = null;
                        _a = this.props, yAxis = _a.yAxis, hasHealthData = _a.hasHealthData, hasDiscover = _a.hasDiscover, hasPerformance = _a.hasPerformance;
                        if (!hasHealthData && !hasDiscover && !hasPerformance) {
                            return [2 /*return*/];
                        }
                        this.setState(function (state) { return ({
                            reloading: state.data !== null,
                            errored: false,
                        }); });
                        _d.label = 1;
                    case 1:
                        _d.trys.push([1, 12, , 13]);
                        if (!(yAxis === releaseChartControls_1.YAxis.SESSIONS)) return [3 /*break*/, 3];
                        return [4 /*yield*/, this.fetchSessions()];
                    case 2:
                        data = _d.sent();
                        _d.label = 3;
                    case 3:
                        if (!(yAxis === releaseChartControls_1.YAxis.USERS)) return [3 /*break*/, 5];
                        return [4 /*yield*/, this.fetchUsers()];
                    case 4:
                        data = _d.sent();
                        _d.label = 5;
                    case 5:
                        if (!(yAxis === releaseChartControls_1.YAxis.CRASH_FREE)) return [3 /*break*/, 7];
                        return [4 /*yield*/, this.fetchCrashFree()];
                    case 6:
                        data = _d.sent();
                        _d.label = 7;
                    case 7:
                        if (!(yAxis === releaseChartControls_1.YAxis.SESSION_DURATION)) return [3 /*break*/, 9];
                        return [4 /*yield*/, this.fetchSessionDuration()];
                    case 8:
                        data = _d.sent();
                        _d.label = 9;
                    case 9:
                        if (!(yAxis === releaseChartControls_1.YAxis.EVENTS ||
                            yAxis === releaseChartControls_1.YAxis.FAILED_TRANSACTIONS ||
                            yAxis === releaseChartControls_1.YAxis.COUNT_DURATION ||
                            yAxis === releaseChartControls_1.YAxis.COUNT_VITAL)) return [3 /*break*/, 11];
                        return [4 /*yield*/, this.fetchEventData()];
                    case 10:
                        // this is used to get total counts for chart footer summary
                        data = _d.sent();
                        _d.label = 11;
                    case 11: return [3 /*break*/, 13];
                    case 12:
                        error_1 = _d.sent();
                        indicator_1.addErrorMessage((_c = (_b = error_1.responseJSON) === null || _b === void 0 ? void 0 : _b.detail) !== null && _c !== void 0 ? _c : locale_1.t('Error loading chart data'));
                        this.setState({
                            errored: true,
                            data: null,
                        });
                        return [3 /*break*/, 13];
                    case 13:
                        if (!utils_1.defined(data) && !this.state.errored) {
                            // this should not happen
                            this.setState({
                                errored: true,
                                data: null,
                            });
                        }
                        if (this.unmounting) {
                            return [2 /*return*/];
                        }
                        this.setState({
                            reloading: false,
                            data: data,
                        });
                        return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    ReleaseStatsRequest.prototype.componentDidMount = function () {
        this.fetchData();
    };
    ReleaseStatsRequest.prototype.componentDidUpdate = function (prevProps) {
        if (isEqual_1.default(omitIgnoredProps(prevProps), omitIgnoredProps(this.props))) {
            return;
        }
        this.fetchData();
    };
    ReleaseStatsRequest.prototype.componentWillUnmount = function () {
        this.unmounting = true;
    };
    Object.defineProperty(ReleaseStatsRequest.prototype, "path", {
        get: function () {
            var organization = this.props.organization;
            return "/organizations/" + organization.slug + "/sessions/";
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ReleaseStatsRequest.prototype, "baseQueryParams", {
        get: function () {
            var _a = this.props, version = _a.version, organization = _a.organization, location = _a.location, selection = _a.selection, defaultStatsPeriod = _a.defaultStatsPeriod;
            return tslib_1.__assign({ query: new tokenizeSearch_1.QueryResults(["release:\"" + version + "\""]).formatString(), interval: utils_3.getInterval(selection.datetime, {
                    highFidelity: organization.features.includes('minute-resolution-sessions'),
                }) }, getParams_1.getParams(pick_1.default(location.query, Object.values(globalSelectionHeader_1.URL_PARAM)), {
                defaultStatsPeriod: defaultStatsPeriod,
            }));
        },
        enumerable: false,
        configurable: true
    });
    ReleaseStatsRequest.prototype.fetchSessions = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, api, version, _b, releaseResponse, otherReleasesResponse, totalSessions, chartData, otherChartData;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, api = _a.api, version = _a.version;
                        return [4 /*yield*/, Promise.all([
                                api.requestPromise(this.path, {
                                    query: tslib_1.__assign(tslib_1.__assign({}, this.baseQueryParams), { field: 'sum(session)', groupBy: 'session.status' }),
                                }),
                                api.requestPromise(this.path, {
                                    query: tslib_1.__assign(tslib_1.__assign({}, this.baseQueryParams), { field: 'sum(session)', groupBy: 'session.status', query: new tokenizeSearch_1.QueryResults(["!release:\"" + version + "\""]).formatString() }),
                                }),
                            ])];
                    case 1:
                        _b = tslib_1.__read.apply(void 0, [_c.sent(), 2]), releaseResponse = _b[0], otherReleasesResponse = _b[1];
                        totalSessions = utils_3.getTotalsFromSessionsResponse({
                            response: releaseResponse,
                            field: 'sum(session)',
                        });
                        chartData = utils_3.fillChartDataFromSessionsResponse({
                            response: releaseResponse,
                            field: 'sum(session)',
                            groupBy: 'session.status',
                            chartData: utils_3.initSessionsBreakdownChartData(),
                        });
                        otherChartData = utils_3.fillChartDataFromSessionsResponse({
                            response: otherReleasesResponse,
                            field: 'sum(session)',
                            groupBy: 'session.status',
                            chartData: utils_3.initOtherSessionsBreakdownChartData(),
                        });
                        return [2 /*return*/, {
                                chartData: tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(Object.values(chartData))), tslib_1.__read(Object.values(otherChartData))),
                                chartSummary: totalSessions.toLocaleString(),
                            }];
                }
            });
        });
    };
    ReleaseStatsRequest.prototype.fetchUsers = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, api, version, _b, releaseResponse, otherReleasesResponse, totalUsers, chartData, otherChartData;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, api = _a.api, version = _a.version;
                        return [4 /*yield*/, Promise.all([
                                api.requestPromise(this.path, {
                                    query: tslib_1.__assign(tslib_1.__assign({}, this.baseQueryParams), { field: 'count_unique(user)', groupBy: 'session.status' }),
                                }),
                                api.requestPromise(this.path, {
                                    query: tslib_1.__assign(tslib_1.__assign({}, this.baseQueryParams), { field: 'count_unique(user)', groupBy: 'session.status', query: new tokenizeSearch_1.QueryResults(["!release:\"" + version + "\""]).formatString() }),
                                }),
                            ])];
                    case 1:
                        _b = tslib_1.__read.apply(void 0, [_c.sent(), 2]), releaseResponse = _b[0], otherReleasesResponse = _b[1];
                        totalUsers = utils_3.getTotalsFromSessionsResponse({
                            response: releaseResponse,
                            field: 'count_unique(user)',
                        });
                        chartData = utils_3.fillChartDataFromSessionsResponse({
                            response: releaseResponse,
                            field: 'count_unique(user)',
                            groupBy: 'session.status',
                            chartData: utils_3.initSessionsBreakdownChartData(),
                        });
                        otherChartData = utils_3.fillChartDataFromSessionsResponse({
                            response: otherReleasesResponse,
                            field: 'count_unique(user)',
                            groupBy: 'session.status',
                            chartData: utils_3.initOtherSessionsBreakdownChartData(),
                        });
                        return [2 /*return*/, {
                                chartData: tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(Object.values(chartData))), tslib_1.__read(Object.values(otherChartData))),
                                chartSummary: totalUsers.toLocaleString(),
                            }];
                }
            });
        });
    };
    ReleaseStatsRequest.prototype.fetchCrashFree = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, api, version, _b, releaseResponse, otherReleasesResponse, chartData, otherChartData, summary;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, api = _a.api, version = _a.version;
                        return [4 /*yield*/, Promise.all([
                                api.requestPromise(this.path, {
                                    query: tslib_1.__assign(tslib_1.__assign({}, this.baseQueryParams), { field: ['sum(session)', 'count_unique(user)'], groupBy: 'session.status' }),
                                }),
                                api.requestPromise(this.path, {
                                    query: tslib_1.__assign(tslib_1.__assign({}, this.baseQueryParams), { field: ['sum(session)', 'count_unique(user)'], groupBy: 'session.status', query: new tokenizeSearch_1.QueryResults(["!release:\"" + version + "\""]).formatString() }),
                                }),
                            ])];
                    case 1:
                        _b = tslib_1.__read.apply(void 0, [_c.sent(), 2]), releaseResponse = _b[0], otherReleasesResponse = _b[1];
                        chartData = utils_3.fillCrashFreeChartDataFromSessionsReponse({
                            response: releaseResponse,
                            field: 'sum(session)',
                            entity: 'sessions',
                            chartData: utils_3.initCrashFreeChartData(),
                        });
                        chartData = utils_3.fillCrashFreeChartDataFromSessionsReponse({
                            response: releaseResponse,
                            field: 'count_unique(user)',
                            entity: 'users',
                            chartData: chartData,
                        });
                        otherChartData = utils_3.fillCrashFreeChartDataFromSessionsReponse({
                            response: otherReleasesResponse,
                            field: 'sum(session)',
                            entity: 'sessions',
                            chartData: utils_3.initOtherCrashFreeChartData(),
                        });
                        otherChartData = utils_3.fillCrashFreeChartDataFromSessionsReponse({
                            response: otherReleasesResponse,
                            field: 'count_unique(user)',
                            entity: 'users',
                            chartData: otherChartData,
                        });
                        summary = locale_1.tct('[usersPercent] users, [sessionsPercent] sessions', {
                            usersPercent: utils_2.displayCrashFreePercent(meanBy_1.default(chartData.users.data.filter(function (item) { return utils_1.defined(item.value); }), 'value')),
                            sessionsPercent: utils_2.displayCrashFreePercent(meanBy_1.default(chartData.sessions.data.filter(function (item) { return utils_1.defined(item.value); }), 'value')),
                        });
                        return [2 /*return*/, {
                                chartData: tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(Object.values(chartData))), tslib_1.__read(Object.values(otherChartData))),
                                chartSummary: summary,
                            }];
                }
            });
        });
    };
    ReleaseStatsRequest.prototype.fetchSessionDuration = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, api, version, _b, releaseResponse, otherReleasesResponse, totalMedianDuration, chartData, otherChartData;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, api = _a.api, version = _a.version;
                        return [4 /*yield*/, Promise.all([
                                api.requestPromise(this.path, {
                                    query: tslib_1.__assign(tslib_1.__assign({}, this.baseQueryParams), { field: 'p50(session.duration)' }),
                                }),
                                api.requestPromise(this.path, {
                                    query: tslib_1.__assign(tslib_1.__assign({}, this.baseQueryParams), { field: 'p50(session.duration)', query: new tokenizeSearch_1.QueryResults(["!release:\"" + version + "\""]).formatString() }),
                                }),
                            ])];
                    case 1:
                        _b = tslib_1.__read.apply(void 0, [_c.sent(), 2]), releaseResponse = _b[0], otherReleasesResponse = _b[1];
                        totalMedianDuration = utils_3.getTotalsFromSessionsResponse({
                            response: releaseResponse,
                            field: 'p50(session.duration)',
                        });
                        chartData = utils_3.fillChartDataFromSessionsResponse({
                            response: releaseResponse,
                            field: 'p50(session.duration)',
                            groupBy: null,
                            chartData: utils_3.initSessionDurationChartData(),
                            valueFormatter: function (duration) { return utils_2.roundDuration(duration ? duration / 1000 : 0); },
                        });
                        otherChartData = utils_3.fillChartDataFromSessionsResponse({
                            response: otherReleasesResponse,
                            field: 'p50(session.duration)',
                            groupBy: null,
                            chartData: utils_3.initOtherSessionDurationChartData(),
                            valueFormatter: function (duration) { return utils_2.roundDuration(duration ? duration / 1000 : 0); },
                        });
                        return [2 /*return*/, {
                                chartData: tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(Object.values(chartData))), tslib_1.__read(Object.values(otherChartData))),
                                chartSummary: formatters_1.getExactDuration(utils_2.roundDuration(totalMedianDuration ? totalMedianDuration / 1000 : 0)),
                            }];
                }
            });
        });
    };
    ReleaseStatsRequest.prototype.fetchEventData = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, api, organization, location, yAxis, eventType, vitalType, selection, version, eventView, payload, eventsCountResponse, chartSummary;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization, location = _a.location, yAxis = _a.yAxis, eventType = _a.eventType, vitalType = _a.vitalType, selection = _a.selection, version = _a.version;
                        eventView = utils_3.getReleaseEventView(selection, version, yAxis, eventType, vitalType, organization, true);
                        payload = eventView.getEventsAPIPayload(location);
                        return [4 /*yield*/, events_1.fetchTotalCount(api, organization.slug, payload)];
                    case 1:
                        eventsCountResponse = _b.sent();
                        chartSummary = eventsCountResponse.toLocaleString();
                        return [2 /*return*/, { chartData: [], chartSummary: chartSummary }];
                }
            });
        });
    };
    ReleaseStatsRequest.prototype.render = function () {
        var _a, _b;
        var children = this.props.children;
        var _c = this.state, data = _c.data, reloading = _c.reloading, errored = _c.errored;
        var loading = data === null;
        return children({
            loading: loading,
            reloading: reloading,
            errored: errored,
            chartData: (_a = data === null || data === void 0 ? void 0 : data.chartData) !== null && _a !== void 0 ? _a : [],
            chartSummary: (_b = data === null || data === void 0 ? void 0 : data.chartSummary) !== null && _b !== void 0 ? _b : '',
        });
    };
    return ReleaseStatsRequest;
}(React.Component));
exports.default = ReleaseStatsRequest;
//# sourceMappingURL=releaseStatsRequest.jsx.map