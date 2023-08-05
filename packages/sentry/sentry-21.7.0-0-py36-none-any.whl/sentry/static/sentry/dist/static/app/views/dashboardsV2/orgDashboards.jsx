Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var notFound_1 = tslib_1.__importDefault(require("app/components/errors/notFound"));
var sentryDocumentTitle_1 = tslib_1.__importDefault(require("app/components/sentryDocumentTitle"));
var locale_1 = require("app/locale");
var analytics_1 = require("app/utils/analytics");
var OrgDashboards = /** @class */ (function (_super) {
    tslib_1.__extends(OrgDashboards, _super);
    function OrgDashboards() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            // AsyncComponent state
            loading: true,
            reloading: false,
            error: false,
            errors: {},
            dashboards: [],
            selectedDashboard: null,
        };
        return _this;
    }
    OrgDashboards.prototype.componentDidUpdate = function (prevProps) {
        if (!isEqual_1.default(prevProps.params.dashboardId, this.props.params.dashboardId)) {
            this.remountComponent();
        }
    };
    OrgDashboards.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, params = _a.params;
        var url = "/organizations/" + organization.slug + "/dashboards/";
        var endpoints = [['dashboards', url]];
        if (params.dashboardId) {
            endpoints.push(['selectedDashboard', "" + url + params.dashboardId + "/"]);
            analytics_1.trackAnalyticsEvent({
                eventKey: 'dashboards2.view',
                eventName: 'Dashboards2: View dashboard',
                organization_id: parseInt(this.props.organization.id, 10),
                dashboard_id: params.dashboardId,
            });
        }
        return endpoints;
    };
    OrgDashboards.prototype.getDashboards = function () {
        var dashboards = this.state.dashboards;
        return Array.isArray(dashboards) ? dashboards : [];
    };
    OrgDashboards.prototype.onRequestSuccess = function (_a) {
        var stateKey = _a.stateKey, data = _a.data;
        var _b = this.props, params = _b.params, organization = _b.organization, location = _b.location;
        if (params.dashboardId || stateKey === 'selectedDashboard') {
            return;
        }
        // If we don't have a selected dashboard, and one isn't going to arrive
        // we can redirect to the first dashboard in the list.
        var dashboardId = data.length ? data[0].id : 'default-overview';
        var url = "/organizations/" + organization.slug + "/dashboard/" + dashboardId + "/";
        react_router_1.browserHistory.replace({
            pathname: url,
            query: tslib_1.__assign({}, location.query),
        });
    };
    OrgDashboards.prototype.renderBody = function () {
        var children = this.props.children;
        var _a = this.state, selectedDashboard = _a.selectedDashboard, error = _a.error;
        return children({
            error: error,
            dashboard: selectedDashboard,
            dashboards: this.getDashboards(),
            reloadData: this.reloadData.bind(this),
        });
    };
    OrgDashboards.prototype.renderError = function (error) {
        var notFound = Object.values(this.state.errors).find(function (resp) { return resp && resp.status === 404; });
        if (notFound) {
            return <notFound_1.default />;
        }
        return _super.prototype.renderError.call(this, error, true, true);
    };
    OrgDashboards.prototype.renderComponent = function () {
        var _a = this.props, organization = _a.organization, location = _a.location;
        if (!organization.features.includes('dashboards-basic')) {
            // Redirect to Dashboards v1
            react_router_1.browserHistory.replace({
                pathname: "/organizations/" + organization.slug + "/dashboards/",
                query: tslib_1.__assign({}, location.query),
            });
            return null;
        }
        return (<sentryDocumentTitle_1.default title={locale_1.t('Dashboards')} orgSlug={organization.slug}>
        {_super.prototype.renderComponent.call(this)}
      </sentryDocumentTitle_1.default>);
    };
    return OrgDashboards;
}(asyncComponent_1.default));
exports.default = OrgDashboards;
//# sourceMappingURL=orgDashboards.jsx.map