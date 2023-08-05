Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var access_1 = tslib_1.__importDefault(require("app/components/acl/access"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var featureDisabled_1 = tslib_1.__importDefault(require("app/components/acl/featureDisabled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var hovercard_1 = tslib_1.__importDefault(require("app/components/hovercard"));
var panels_1 = require("app/components/panels");
var tag_1 = tslib_1.__importDefault(require("app/components/tag"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var ProviderItem = function (_a) {
    var provider = _a.provider, active = _a.active, onConfigure = _a.onConfigure;
    var handleConfigure = function (e) {
        onConfigure === null || onConfigure === void 0 ? void 0 : onConfigure(provider.key, e);
    };
    var renderDisabledLock = function (p) { return (<LockedFeature provider={p.provider} features={p.features}/>); };
    var defaultRenderInstallButton = function (_a) {
        var hasFeature = _a.hasFeature;
        return (<access_1.default access={['org:write']}>
      {function (_a) {
                var hasAccess = _a.hasAccess;
                return (<button_1.default type="submit" name="provider" size="small" value={provider.key} disabled={!hasFeature || !hasAccess} onClick={handleConfigure}>
          {locale_1.t('Configure')}
        </button_1.default>);
            }}
    </access_1.default>);
    };
    // TODO(epurkhiser): We should probably use a more explicit hook name,
    // instead of just the feature names (sso-basic, sso-saml2, etc).
    var featureKey = provider.requiredFeature;
    var hookName = featureKey
        ? "feature-disabled:" + utils_1.descopeFeatureName(featureKey)
        : null;
    var featureProps = hookName ? { hookName: hookName } : {};
    var getProviderDescription = function (providerName) {
        if (providerName === 'SAML2') {
            return locale_1.t('your preferred SAML2 compliant provider like Ping Identity, Google SAML, Keycloak, or VMware Identity Manager');
        }
        if (providerName === 'Google') {
            return locale_1.t('Google (OAuth)');
        }
        return providerName;
    };
    return (<feature_1.default {...featureProps} features={[featureKey].filter(function (f) { return f; })} renderDisabled={function (_a) {
            var children = _a.children, props = tslib_1.__rest(_a, ["children"]);
            return typeof children === 'function' &&
                // TODO(ts): the Feature component isn't correctly templatized to allow
                // for custom props in the renderDisabled function
                children(tslib_1.__assign(tslib_1.__assign({}, props), { renderDisabled: renderDisabledLock }));
        }}>
      {function (_a) {
            var hasFeature = _a.hasFeature, features = _a.features, renderDisabled = _a.renderDisabled, renderInstallButton = _a.renderInstallButton;
            return (<panels_1.PanelItem center>
          <ProviderInfo>
            <ProviderLogo className={"provider-logo " + provider.name
                    .replace(/\s/g, '-')
                    .toLowerCase()}/>
            <div>
              <ProviderName>{provider.name}</ProviderName>
              <ProviderDescription>
                {locale_1.t('Enable your organization to sign in with %s.', getProviderDescription(provider.name))}
              </ProviderDescription>
            </div>
          </ProviderInfo>

          <FeatureBadge>
            {!hasFeature && renderDisabled({ provider: provider, features: features })}
          </FeatureBadge>

          <div>
            {active ? (<ActiveIndicator />) : ((renderInstallButton !== null && renderInstallButton !== void 0 ? renderInstallButton : defaultRenderInstallButton)({ provider: provider, hasFeature: hasFeature }))}
          </div>
        </panels_1.PanelItem>);
        }}
    </feature_1.default>);
};
exports.default = ProviderItem;
var ProviderInfo = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n"], ["\n  flex: 1;\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n"])), space_1.default(2));
var ProviderLogo = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  height: 36px;\n  width: 36px;\n  border-radius: 3px;\n  margin-right: 0;\n  top: auto;\n"], ["\n  height: 36px;\n  width: 36px;\n  border-radius: 3px;\n  margin-right: 0;\n  top: auto;\n"])));
var ProviderName = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  font-weight: bold;\n"], ["\n  font-weight: bold;\n"])));
var ProviderDescription = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n  font-size: 0.8em;\n"], ["\n  margin-top: ", ";\n  font-size: 0.8em;\n"])), space_1.default(0.75));
var FeatureBadge = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var ActiveIndicator = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  background: ", ";\n  color: ", ";\n  padding: ", " ", ";\n  border-radius: 2px;\n  font-size: 0.8em;\n"], ["\n  background: ", ";\n  color: ", ";\n  padding: ", " ", ";\n  border-radius: 2px;\n  font-size: 0.8em;\n"])), function (p) { return p.theme.green300; }, function (p) { return p.theme.white; }, space_1.default(1), space_1.default(1.5));
ActiveIndicator.defaultProps = {
    children: locale_1.t('Active'),
};
var DisabledHovercard = styled_1.default(hovercard_1.default)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  width: 350px;\n"], ["\n  width: 350px;\n"])));
var LockedFeature = function (_a) {
    var provider = _a.provider, features = _a.features, className = _a.className;
    return (<DisabledHovercard containerClassName={className} body={<featureDisabled_1.default features={features} hideHelpToggle message={locale_1.t('%s SSO is disabled.', provider.name)} featureName={locale_1.t('SSO Auth')}/>}>
    <tag_1.default icon={<icons_1.IconLock />}>{locale_1.t('disabled')}</tag_1.default>
  </DisabledHovercard>);
};
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=providerItem.jsx.map