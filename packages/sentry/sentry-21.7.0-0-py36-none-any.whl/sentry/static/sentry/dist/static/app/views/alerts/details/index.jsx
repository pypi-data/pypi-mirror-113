Object.defineProperty(exports, "__esModule", { value: true });
exports.alertDetailsLink = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var incident_1 = require("app/actionCreators/incident");
var indicator_1 = require("app/actionCreators/indicator");
var members_1 = require("app/actionCreators/members");
var sentryDocumentTitle_1 = tslib_1.__importDefault(require("app/components/sentryDocumentTitle"));
var locale_1 = require("app/locale");
var analytics_1 = require("app/utils/analytics");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var types_1 = require("../types");
var utils_1 = require("../utils");
var body_1 = tslib_1.__importDefault(require("./body"));
var header_1 = tslib_1.__importDefault(require("./header"));
var alertDetailsLink = function (organization, incident) {
    return "/organizations/" + organization.slug + "/alerts/rules/details/" + ((incident === null || incident === void 0 ? void 0 : incident.alertRule.status) === types_1.AlertRuleStatus.SNAPSHOT &&
        (incident === null || incident === void 0 ? void 0 : incident.alertRule.originalAlertRuleId)
        ? incident === null || incident === void 0 ? void 0 : incident.alertRule.originalAlertRuleId
        : incident === null || incident === void 0 ? void 0 : incident.alertRule.id) + "/";
};
exports.alertDetailsLink = alertDetailsLink;
var IncidentDetails = /** @class */ (function (_super) {
    tslib_1.__extends(IncidentDetails, _super);
    function IncidentDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = { isLoading: false, hasError: false };
        _this.fetchData = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, api, location, organization, _b, orgId, alertId, incidentPromise, statsPromise, _err_1;
            var _this = this;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        this.setState({ isLoading: true, hasError: false });
                        _a = this.props, api = _a.api, location = _a.location, organization = _a.organization, _b = _a.params, orgId = _b.orgId, alertId = _b.alertId;
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        incidentPromise = utils_1.fetchIncident(api, orgId, alertId).then(function (incident) {
                            var hasRedesign = incident.alertRule &&
                                _this.props.organization.features.includes('alert-details-redesign');
                            // only stop redirect if param is explicitly set to false
                            var stopRedirect = location && location.query && location.query.redirect === 'false';
                            if (hasRedesign && !stopRedirect) {
                                react_router_1.browserHistory.replace({
                                    pathname: exports.alertDetailsLink(organization, incident),
                                    query: { alert: incident.identifier },
                                });
                            }
                            _this.setState({ incident: incident });
                            incident_1.markIncidentAsSeen(api, orgId, incident);
                        });
                        statsPromise = utils_1.fetchIncidentStats(api, orgId, alertId).then(function (stats) {
                            return _this.setState({ stats: stats });
                        });
                        // State not set after promise.all because stats *usually* takes
                        // more time than the incident api
                        return [4 /*yield*/, Promise.all([incidentPromise, statsPromise])];
                    case 2:
                        // State not set after promise.all because stats *usually* takes
                        // more time than the incident api
                        _c.sent();
                        this.setState({ isLoading: false, hasError: false });
                        return [3 /*break*/, 4];
                    case 3:
                        _err_1 = _c.sent();
                        this.setState({ isLoading: false, hasError: true });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleSubscriptionChange = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, api, _b, orgId, alertId, isSubscribed, newIsSubscribed;
            return tslib_1.__generator(this, function (_c) {
                _a = this.props, api = _a.api, _b = _a.params, orgId = _b.orgId, alertId = _b.alertId;
                if (!this.state.incident) {
                    return [2 /*return*/];
                }
                isSubscribed = this.state.incident.isSubscribed;
                newIsSubscribed = !isSubscribed;
                this.setState(function (state) { return ({
                    incident: tslib_1.__assign(tslib_1.__assign({}, state.incident), { isSubscribed: newIsSubscribed }),
                }); });
                try {
                    utils_1.updateSubscription(api, orgId, alertId, newIsSubscribed);
                }
                catch (_err) {
                    this.setState(function (state) { return ({
                        incident: tslib_1.__assign(tslib_1.__assign({}, state.incident), { isSubscribed: isSubscribed }),
                    }); });
                    indicator_1.addErrorMessage(locale_1.t('An error occurred, your subscription status was not changed.'));
                }
                return [2 /*return*/];
            });
        }); };
        _this.handleStatusChange = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, api, _b, orgId, alertId, status, newStatus, incident, _err_2;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, api = _a.api, _b = _a.params, orgId = _b.orgId, alertId = _b.alertId;
                        if (!this.state.incident) {
                            return [2 /*return*/];
                        }
                        status = this.state.incident.status;
                        newStatus = utils_1.isOpen(this.state.incident) ? types_1.IncidentStatus.CLOSED : status;
                        this.setState(function (state) { return ({
                            incident: tslib_1.__assign(tslib_1.__assign({}, state.incident), { status: newStatus }),
                        }); });
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, utils_1.updateStatus(api, orgId, alertId, newStatus)];
                    case 2:
                        incident = _c.sent();
                        // Update entire incident object because updating status can cause other parts
                        // of the model to change (e.g close date)
                        this.setState({ incident: incident });
                        return [3 /*break*/, 4];
                    case 3:
                        _err_2 = _c.sent();
                        this.setState(function (state) { return ({
                            incident: tslib_1.__assign(tslib_1.__assign({}, state.incident), { status: status }),
                        }); });
                        indicator_1.addErrorMessage(locale_1.t('An error occurred, your incident status was not changed.'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    IncidentDetails.prototype.componentDidMount = function () {
        var _a = this.props, api = _a.api, organization = _a.organization, params = _a.params;
        analytics_1.trackAnalyticsEvent({
            eventKey: 'alert_details.viewed',
            eventName: 'Alert Details: Viewed',
            organization_id: parseInt(organization.id, 10),
            alert_id: parseInt(params.alertId, 10),
        });
        members_1.fetchOrgMembers(api, params.orgId);
        this.fetchData();
    };
    IncidentDetails.prototype.render = function () {
        var _a;
        var _b = this.state, incident = _b.incident, stats = _b.stats, hasError = _b.hasError;
        var _c = this.props, params = _c.params, organization = _c.organization;
        var alertId = params.alertId;
        var project = (_a = incident === null || incident === void 0 ? void 0 : incident.projects) === null || _a === void 0 ? void 0 : _a[0];
        return (<react_1.Fragment>
        <sentryDocumentTitle_1.default title={locale_1.t('Alert %s', alertId)} orgSlug={organization.slug} projectSlug={project}/>
        <header_1.default hasIncidentDetailsError={hasError} params={params} incident={incident} stats={stats} onSubscriptionChange={this.handleSubscriptionChange} onStatusChange={this.handleStatusChange}/>
        <body_1.default {...this.props} incident={incident} stats={stats}/>
      </react_1.Fragment>);
    };
    return IncidentDetails;
}(react_1.Component));
exports.default = withApi_1.default(IncidentDetails);
//# sourceMappingURL=index.jsx.map