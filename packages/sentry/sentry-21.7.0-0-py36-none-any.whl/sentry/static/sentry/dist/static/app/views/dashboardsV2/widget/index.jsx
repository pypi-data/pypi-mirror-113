Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var locale_1 = require("app/locale");
var organization_1 = require("app/styles/organization");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var widgetBuilder_1 = tslib_1.__importDefault(require("./widgetBuilder"));
function WidgetBuilderContainer(_a) {
    var organization = _a.organization, props = tslib_1.__rest(_a, ["organization"]);
    return (<feature_1.default features={['metrics', 'dashboards-edit']} organization={organization} renderDisabled={function () { return (<organization_1.PageContent>
          <alert_1.default type="warning">{locale_1.t("You don't have access to this feature")}</alert_1.default>
        </organization_1.PageContent>); }}>
      <widgetBuilder_1.default {...props} organization={organization}/>
    </feature_1.default>);
}
exports.default = withOrganization_1.default(WidgetBuilderContainer);
//# sourceMappingURL=index.jsx.map