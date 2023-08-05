Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var locale_1 = require("app/locale");
var organization_1 = require("app/styles/organization");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var grouping_1 = tslib_1.__importDefault(require("./grouping"));
function GroupingContainer(_a) {
    var organization = _a.organization, params = _a.params, location = _a.location, router = _a.router;
    return (<feature_1.default features={['grouping-tree-ui']} organization={organization} renderDisabled={function () { return (<organization_1.PageContent>
          <alert_1.default type="warning">{locale_1.t("You don't have access to this feature")}</alert_1.default>
        </organization_1.PageContent>); }}>
      <grouping_1.default location={location} groupId={params.groupId} organization={organization} router={router}/>
    </feature_1.default>);
}
exports.default = withOrganization_1.default(GroupingContainer);
//# sourceMappingURL=index.jsx.map