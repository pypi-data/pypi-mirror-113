Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var access_1 = tslib_1.__importDefault(require("app/components/acl/access"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var featureDisabled_1 = tslib_1.__importDefault(require("app/components/acl/featureDisabled"));
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var filtersAndSampling_1 = tslib_1.__importDefault(require("./filtersAndSampling"));
var Index = function (_a) {
    var organization = _a.organization, props = tslib_1.__rest(_a, ["organization"]);
    return (<feature_1.default features={['filters-and-sampling']} organization={organization} renderDisabled={function () { return (<featureDisabled_1.default alert={panels_1.PanelAlert} features={organization.features} featureName={locale_1.t('Filters & Sampling')}/>); }}>
    <access_1.default organization={organization} access={['project:write']}>
      {function (_a) {
            var hasAccess = _a.hasAccess;
            return (<filtersAndSampling_1.default {...props} hasAccess={hasAccess} organization={organization}/>);
        }}
    </access_1.default>
  </feature_1.default>);
};
exports.default = withOrganization_1.default(Index);
//# sourceMappingURL=index.jsx.map