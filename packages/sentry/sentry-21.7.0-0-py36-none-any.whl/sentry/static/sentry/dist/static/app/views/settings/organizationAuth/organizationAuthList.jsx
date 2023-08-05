Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var utils_1 = require("app/utils");
var getCsrfToken_1 = tslib_1.__importDefault(require("app/utils/getCsrfToken"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var permissionAlert_1 = tslib_1.__importDefault(require("app/views/settings/organization/permissionAlert"));
var providerItem_1 = tslib_1.__importDefault(require("./providerItem"));
var providerPopularity = {
    google: 0,
    github: 1,
    okta: 2,
    'active-directory': 3,
    saml2: 4,
    onelogin: 5,
    rippling: 6,
    auth0: 7,
};
var OrganizationAuthList = function (_a) {
    var organization = _a.organization, providerList = _a.providerList, activeProvider = _a.activeProvider;
    var features = organization.features;
    // Sort provider list twice: first, by popularity,
    // and then a second time, to sort unavailable providers for the current plan to the end of the list.
    var sortedByPopularity = (providerList !== null && providerList !== void 0 ? providerList : []).sort(function (a, b) {
        if (!(a.key in providerPopularity)) {
            return -1;
        }
        if (!(b.key in providerPopularity)) {
            return 1;
        }
        if (providerPopularity[a.key] === providerPopularity[b.key]) {
            return 0;
        }
        return providerPopularity[a.key] > providerPopularity[b.key] ? 1 : -1;
    });
    var list = sortedByPopularity.sort(function (a, b) {
        var aEnabled = features.includes(utils_1.descopeFeatureName(a.requiredFeature));
        var bEnabled = features.includes(utils_1.descopeFeatureName(b.requiredFeature));
        if (aEnabled === bEnabled) {
            return 0;
        }
        return aEnabled ? -1 : 1;
    });
    var warn2FADisable = organization.require2FA &&
        list.some(function (_a) {
            var requiredFeature = _a.requiredFeature;
            return features.includes(utils_1.descopeFeatureName(requiredFeature));
        });
    return (<div className="sso">
      <settingsPageHeader_1.default title="Authentication"/>
      <permissionAlert_1.default />
      <panels_1.Panel>
        <panels_1.PanelHeader>{locale_1.t('Choose a provider')}</panels_1.PanelHeader>
        <panels_1.PanelBody>
          {!activeProvider && (<panels_1.PanelAlert type="info">
              {locale_1.tct('Get started with Single Sign-on for your organization by selecting a provider. Read more in our [link:SSO documentation].', {
                link: (<externalLink_1.default href="https://docs.sentry.io/product/accounts/sso/"/>),
            })}
            </panels_1.PanelAlert>)}

          {warn2FADisable && (<panels_1.PanelAlert type="warning">
              {locale_1.t('Require 2FA will be disabled if you enable SSO.')}
            </panels_1.PanelAlert>)}

          <form action={"/organizations/" + organization.slug + "/auth/configure/"} method="POST">
            <input type="hidden" name="csrfmiddlewaretoken" value={getCsrfToken_1.default()}/>
            <input type="hidden" name="init" value="1"/>

            {list.map(function (provider) { return (<providerItem_1.default key={provider.key} provider={provider} active={!!activeProvider && provider.key === activeProvider.key}/>); })}
            {list.length === 0 && (<emptyMessage_1.default>
                {locale_1.t('No authentication providers are available.')}
              </emptyMessage_1.default>)}
          </form>
        </panels_1.PanelBody>
      </panels_1.Panel>
    </div>);
};
exports.default = withOrganization_1.default(OrganizationAuthList);
//# sourceMappingURL=organizationAuthList.jsx.map