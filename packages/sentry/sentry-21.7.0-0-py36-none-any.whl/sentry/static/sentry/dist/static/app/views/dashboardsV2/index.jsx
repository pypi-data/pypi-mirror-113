Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var notFound_1 = tslib_1.__importDefault(require("app/components/errors/notFound"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var detail_1 = tslib_1.__importDefault(require("./detail"));
var orgDashboards_1 = tslib_1.__importDefault(require("./orgDashboards"));
var types_1 = require("./types");
var view_1 = require("./view");
var DashboardsV2Container = /** @class */ (function (_super) {
    tslib_1.__extends(DashboardsV2Container, _super);
    function DashboardsV2Container() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    DashboardsV2Container.prototype.render = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, params = _a.params, api = _a.api, location = _a.location, children = _a.children;
        if (organization.features.includes('dashboards-edit')) {
            return children;
        }
        return (<view_1.DashboardBasicFeature organization={organization}>
        <orgDashboards_1.default api={api} location={location} params={params} organization={organization}>
          {function (_a) {
                var dashboard = _a.dashboard, dashboards = _a.dashboards, error = _a.error, reloadData = _a.reloadData;
                return error ? (<notFound_1.default />) : dashboard ? (<detail_1.default {..._this.props} initialState={types_1.DashboardState.VIEW} dashboard={dashboard} dashboards={dashboards} reloadData={reloadData}/>) : (<loadingIndicator_1.default />);
            }}
        </orgDashboards_1.default>
      </view_1.DashboardBasicFeature>);
    };
    return DashboardsV2Container;
}(React.Component));
exports.default = withApi_1.default(withOrganization_1.default(DashboardsV2Container));
//# sourceMappingURL=index.jsx.map