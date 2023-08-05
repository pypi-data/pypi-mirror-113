Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = tslib_1.__importDefault(require("react"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var locale_1 = require("app/locale");
var organization_1 = require("app/styles/organization");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var data_1 = require("./data");
var detail_1 = tslib_1.__importDefault(require("./detail"));
var types_1 = require("./types");
var utils_1 = require("./utils");
function CreateDashboard(props) {
    function renderDisabled() {
        return (<organization_1.PageContent>
        <alert_1.default type="warning">{locale_1.t("You don't have access to this feature")}</alert_1.default>
      </organization_1.PageContent>);
    }
    var dashboard = utils_1.cloneDashboard(data_1.EMPTY_DASHBOARD);
    return (<feature_1.default features={['dashboards-edit']} organization={props.organization} renderDisabled={renderDisabled}>
      <detail_1.default {...props} initialState={types_1.DashboardState.CREATE} dashboard={dashboard} dashboards={[]}/>
    </feature_1.default>);
}
exports.default = withOrganization_1.default(CreateDashboard);
//# sourceMappingURL=create.jsx.map