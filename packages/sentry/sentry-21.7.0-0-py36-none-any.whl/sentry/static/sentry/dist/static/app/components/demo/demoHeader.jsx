Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var logoSentry_1 = tslib_1.__importDefault(require("app/components/logoSentry"));
var locale_1 = require("app/locale");
var preferencesStore_1 = tslib_1.__importDefault(require("app/stores/preferencesStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var advancedAnalytics_1 = require("app/utils/advancedAnalytics");
var getCookie_1 = tslib_1.__importDefault(require("app/utils/getCookie"));
function DemoHeader() {
    // if the user came from a SaaS org, we should send them back to upgrade when they leave the sandbox
    var saasOrgSlug = getCookie_1.default('saas_org_slug');
    var email = localStorage.getItem('email');
    var queryParameter = email ? "?email=" + email : '';
    var getStartedText = saasOrgSlug ? locale_1.t('Upgrade Now') : locale_1.t('Sign Up for Free');
    var getStartedUrl = saasOrgSlug
        ? "https://sentry.io/settings/" + saasOrgSlug + "/billing/checkout/"
        : "https://sentry.io/signup/" + queryParameter;
    var _a = tslib_1.__read(react_1.useState(preferencesStore_1.default.prefs.collapsed), 2), collapsed = _a[0], setCollapsed = _a[1];
    var preferenceUnsubscribe = preferencesStore_1.default.listen(function (preferences) { return onPreferenceChange(preferences); }, undefined);
    function onPreferenceChange(preferences) {
        if (preferences.collapsed === collapsed) {
            return;
        }
        setCollapsed(!collapsed);
    }
    react_1.useEffect(function () {
        return function () {
            preferenceUnsubscribe();
        };
    });
    return (<Wrapper collapsed={collapsed}>
      <StyledLogoSentry />
      <buttonBar_1.default gap={4}>
        <StyledExternalLink onClick={function () { return advancedAnalytics_1.trackAdvancedAnalyticsEvent('growth.demo_click_docs', {}, null); }} href="https://docs.sentry.io">
          {locale_1.t('Documentation')}
        </StyledExternalLink>
        <BaseButton priority="form" onClick={function () {
            return advancedAnalytics_1.trackAdvancedAnalyticsEvent('growth.demo_click_request_demo', {}, null);
        }} href="https://sentry.io/_/demo/">
          {locale_1.t('Request a Demo')}
        </BaseButton>
        <GetStarted onClick={function () {
            return advancedAnalytics_1.trackAdvancedAnalyticsEvent('growth.demo_click_get_started', {
                is_upgrade: !!saasOrgSlug,
            }, null);
        }} href={getStartedUrl}>
          {getStartedText}
        </GetStarted>
      </buttonBar_1.default>
    </Wrapper>);
}
exports.default = DemoHeader;
// Note many of the colors don't come from the theme as they come from the marketing site
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding-right: ", ";\n  background-color: ", ";\n  height: ", ";\n  display: flex;\n  justify-content: space-between;\n  text-transform: uppercase;\n\n  margin-left: calc(\n    -1 * ", "\n  );\n\n  position: fixed;\n  width: 100%;\n  border-bottom: 1px solid ", ";\n  z-index: ", ";\n\n  @media (max-width: ", ") {\n    height: ", ";\n    margin-left: 0;\n  }\n"], ["\n  padding-right: ", ";\n  background-color: ", ";\n  height: ", ";\n  display: flex;\n  justify-content: space-between;\n  text-transform: uppercase;\n\n  margin-left: calc(\n    -1 * ", "\n  );\n\n  position: fixed;\n  width: 100%;\n  border-bottom: 1px solid ", ";\n  z-index: ", ";\n\n  @media (max-width: ", ") {\n    height: ", ";\n    margin-left: 0;\n  }\n"])), space_1.default(3), function (p) { return p.theme.white; }, function (p) { return p.theme.demo.headerSize; }, function (p) { return (p.collapsed ? p.theme.sidebar.collapsedWidth : p.theme.sidebar.expandedWidth); }, function (p) { return p.theme.border; }, function (p) { return p.theme.zIndex.settingsSidebarNav; }, function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.sidebar.mobileHeight; });
var StyledLogoSentry = styled_1.default(logoSentry_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-top: auto;\n  margin-bottom: auto;\n  margin-left: 20px;\n  width: 130px;\n  height: 30px;\n  color: ", ";\n"], ["\n  margin-top: auto;\n  margin-bottom: auto;\n  margin-left: 20px;\n  width: 130px;\n  height: 30px;\n  color: ", ";\n"])), function (p) { return p.theme.textColor; });
var BaseButton = styled_1.default(button_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  border-radius: 2rem;\n  text-transform: uppercase;\n"], ["\n  border-radius: 2rem;\n  text-transform: uppercase;\n"])));
// Note many of the colors don't come from the theme as they come from the marketing site
var GetStarted = styled_1.default(BaseButton)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  border-color: transparent;\n  box-shadow: 0 2px 0 rgb(54 45 89 / 10%);\n  background-color: #e1567c;\n  color: #fff;\n"], ["\n  border-color: transparent;\n  box-shadow: 0 2px 0 rgb(54 45 89 / 10%);\n  background-color: #e1567c;\n  color: #fff;\n"])));
var StyledExternalLink = styled_1.default(externalLink_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  color: #584774;\n"], ["\n  color: #584774;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=demoHeader.jsx.map