Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var moment_1 = tslib_1.__importDefault(require("moment"));
var members_1 = require("app/actionCreators/members");
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var locale_1 = require("app/locale");
var dates_1 = require("app/utils/dates");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var types_1 = require("app/views/alerts/incidentRules/types");
var row_1 = require("app/views/alerts/list/row");
var utils_1 = require("../../utils");
var body_1 = tslib_1.__importDefault(require("./body"));
var constants_1 = require("./constants");
var header_1 = tslib_1.__importDefault(require("./header"));
var AlertRuleDetails = /** @class */ (function (_super) {
    tslib_1.__extends(AlertRuleDetails, _super);
    function AlertRuleDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = { isLoading: false, hasError: false };
        _this.fetchData = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, api, _b, orgId, ruleId, location, timePeriod, start, end, rulePromise, incidentsPromise, _err_1;
            var _this = this;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, api = _a.api, _b = _a.params, orgId = _b.orgId, ruleId = _b.ruleId, location = _a.location;
                        this.setState({ isLoading: true, hasError: false });
                        if (!location.query.alert) return [3 /*break*/, 2];
                        return [4 /*yield*/, utils_1.fetchIncident(api, orgId, location.query.alert)
                                .then(function (incident) { return _this.setState({ selectedIncident: incident }); })
                                .catch(function () { return _this.setState({ selectedIncident: null }); })];
                    case 1:
                        _c.sent();
                        return [3 /*break*/, 3];
                    case 2:
                        this.setState({ selectedIncident: null });
                        _c.label = 3;
                    case 3:
                        timePeriod = this.getTimePeriod();
                        start = timePeriod.start, end = timePeriod.end;
                        _c.label = 4;
                    case 4:
                        _c.trys.push([4, 6, , 7]);
                        rulePromise = utils_1.fetchAlertRule(orgId, ruleId).then(function (rule) {
                            return _this.setState({ rule: rule });
                        });
                        incidentsPromise = utils_1.fetchIncidentsForRule(orgId, ruleId, start, end).then(function (incidents) { return _this.setState({ incidents: incidents }); });
                        return [4 /*yield*/, Promise.all([rulePromise, incidentsPromise])];
                    case 5:
                        _c.sent();
                        this.setState({ isLoading: false, hasError: false });
                        return [3 /*break*/, 7];
                    case 6:
                        _err_1 = _c.sent();
                        this.setState({ isLoading: false, hasError: true });
                        return [3 /*break*/, 7];
                    case 7: return [2 /*return*/];
                }
            });
        }); };
        _this.handleTimePeriodChange = function (value) {
            react_router_1.browserHistory.push({
                pathname: _this.props.location.pathname,
                query: {
                    period: value,
                },
            });
        };
        _this.handleZoom = function (start, end) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var location;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        location = this.props.location;
                        return [4 /*yield*/, react_router_1.browserHistory.push({
                                pathname: location.pathname,
                                query: {
                                    start: start,
                                    end: end,
                                },
                            })];
                    case 1:
                        _a.sent();
                        return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    AlertRuleDetails.prototype.componentDidMount = function () {
        var _a = this.props, api = _a.api, params = _a.params;
        members_1.fetchOrgMembers(api, params.orgId);
        this.fetchData();
    };
    AlertRuleDetails.prototype.componentDidUpdate = function (prevProps) {
        if (prevProps.location.search !== this.props.location.search ||
            prevProps.params.orgId !== this.props.params.orgId ||
            prevProps.params.ruleId !== this.props.params.ruleId) {
            this.fetchData();
        }
    };
    AlertRuleDetails.prototype.getTimePeriod = function () {
        var _a, _b;
        var location = this.props.location;
        var rule = this.state.rule;
        var defaultPeriod = (rule === null || rule === void 0 ? void 0 : rule.timeWindow) && (rule === null || rule === void 0 ? void 0 : rule.timeWindow) > types_1.TimeWindow.ONE_HOUR
            ? types_1.TimePeriod.SEVEN_DAYS
            : types_1.TimePeriod.ONE_DAY;
        var period = (_a = location.query.period) !== null && _a !== void 0 ? _a : defaultPeriod;
        if (location.query.start && location.query.end) {
            return {
                start: location.query.start,
                end: location.query.end,
                period: period,
                label: locale_1.t('Custom time'),
                display: (<react_1.Fragment>
            <dateTime_1.default date={moment_1.default.utc(location.query.start)} timeAndDate/>
            {' — '}
            <dateTime_1.default date={moment_1.default.utc(location.query.end)} timeAndDate/>
          </react_1.Fragment>),
                custom: true,
            };
        }
        if (location.query.alert && this.state.selectedIncident) {
            var _c = row_1.makeRuleDetailsQuery(this.state.selectedIncident), start_1 = _c.start, end_1 = _c.end;
            return {
                start: start_1,
                end: end_1,
                period: period,
                label: locale_1.t('Custom time'),
                display: (<react_1.Fragment>
            <dateTime_1.default date={moment_1.default.utc(start_1)} timeAndDate/>
            {' — '}
            <dateTime_1.default date={moment_1.default.utc(end_1)} timeAndDate/>
          </react_1.Fragment>),
                custom: true,
            };
        }
        var timeOption = (_b = constants_1.TIME_OPTIONS.find(function (item) { return item.value === period; })) !== null && _b !== void 0 ? _b : constants_1.TIME_OPTIONS[1];
        var start = dates_1.getUtcDateString(moment_1.default(moment_1.default.utc().diff(constants_1.TIME_WINDOWS[timeOption.value])));
        var end = dates_1.getUtcDateString(moment_1.default.utc());
        return {
            start: start,
            end: end,
            period: period,
            label: timeOption.label,
            display: timeOption.label,
        };
    };
    AlertRuleDetails.prototype.render = function () {
        var _a = this.state, rule = _a.rule, incidents = _a.incidents, hasError = _a.hasError, selectedIncident = _a.selectedIncident;
        var _b = this.props, params = _b.params, organization = _b.organization;
        var timePeriod = this.getTimePeriod();
        return (<react_1.Fragment>
        <feature_1.default organization={organization} features={['alert-details-redesign']}>
          <header_1.default hasIncidentRuleDetailsError={hasError} params={params} rule={rule}/>
          <body_1.default {...this.props} rule={rule} incidents={incidents} timePeriod={timePeriod} selectedIncident={selectedIncident} handleTimePeriodChange={this.handleTimePeriodChange} handleZoom={this.handleZoom}/>
        </feature_1.default>
      </react_1.Fragment>);
    };
    return AlertRuleDetails;
}(react_1.Component));
exports.default = withApi_1.default(AlertRuleDetails);
//# sourceMappingURL=index.jsx.map