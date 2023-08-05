Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var featureDisabled_1 = tslib_1.__importDefault(require("app/components/acl/featureDisabled"));
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var relayWrapper_1 = tslib_1.__importDefault(require("./relayWrapper"));
var OrganizationRelay = function (_a) {
    var organization = _a.organization, props = tslib_1.__rest(_a, ["organization"]);
    return (<feature_1.default features={['relay']} organization={organization} renderDisabled={function () { return (<featureDisabled_1.default alert={panels_1.PanelAlert} features={organization.features} featureName={locale_1.t('Relay')}/>); }}>
    <relayWrapper_1.default organization={organization} {...props}/>
  </feature_1.default>);
};
exports.default = withOrganization_1.default(OrganizationRelay);
//# sourceMappingURL=index.jsx.map