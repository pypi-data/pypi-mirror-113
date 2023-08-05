Object.defineProperty(exports, "__esModule", { value: true });
exports.DashboardBasicFeature = void 0;
var tslib_1 = require("tslib");
var react_1 = tslib_1.__importDefault(require("react"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var notFound_1 = tslib_1.__importDefault(require("app/components/errors/notFound"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var locale_1 = require("app/locale");
var organization_1 = require("app/styles/organization");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var detail_1 = tslib_1.__importDefault(require("./detail"));
var orgDashboards_1 = tslib_1.__importDefault(require("./orgDashboards"));
var types_1 = require("./types");
function ViewEditDashboard(props) {
    var organization = props.organization, params = props.params, api = props.api, location = props.location;
    return (<exports.DashboardBasicFeature organization={organization}>
      <orgDashboards_1.default api={api} location={location} params={params} organization={organization}>
        {function (_a) {
            var dashboard = _a.dashboard, dashboards = _a.dashboards, error = _a.error, reloadData = _a.reloadData;
            return error ? (<notFound_1.default />) : dashboard ? (<detail_1.default {...props} initialState={types_1.DashboardState.VIEW} dashboard={dashboard} dashboards={dashboards} reloadData={reloadData}/>) : (<loadingIndicator_1.default />);
        }}
      </orgDashboards_1.default>
    </exports.DashboardBasicFeature>);
}
exports.default = withApi_1.default(withOrganization_1.default(ViewEditDashboard));
var DashboardBasicFeature = function (_a) {
    var organization = _a.organization, children = _a.children;
    var renderDisabled = function () { return (<organization_1.PageContent>
      <alert_1.default type="warning">{locale_1.t("You don't have access to this feature")}</alert_1.default>
    </organization_1.PageContent>); };
    return (<feature_1.default hookName="feature-disabled:dashboards-page" features={['organizations:dashboards-basic']} organization={organization} renderDisabled={renderDisabled}>
      {children}
    </feature_1.default>);
};
exports.DashboardBasicFeature = DashboardBasicFeature;
//# sourceMappingURL=view.jsx.map