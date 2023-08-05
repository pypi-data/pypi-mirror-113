Object.defineProperty(exports, "__esModule", { value: true });
exports.SettingsIndex = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_document_title_1 = tslib_1.__importDefault(require("react-document-title"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var omit_1 = tslib_1.__importDefault(require("lodash/omit"));
var organizations_1 = require("app/actionCreators/organizations");
var demoModeGate_1 = tslib_1.__importDefault(require("app/components/acl/demoModeGate"));
var organizationAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/organizationAvatar"));
var userAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/userAvatar"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var panels_1 = require("app/components/panels");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var withLatestContext_1 = tslib_1.__importDefault(require("app/utils/withLatestContext"));
var settingsLayout_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsLayout"));
var LINKS = {
    DOCUMENTATION: 'https://docs.sentry.io/',
    DOCUMENTATION_PLATFORMS: 'https://docs.sentry.io/clients/',
    DOCUMENTATION_QUICKSTART: 'https://docs.sentry.io/platform-redirect/?next=/',
    DOCUMENTATION_CLI: 'https://docs.sentry.io/product/cli/',
    DOCUMENTATION_API: 'https://docs.sentry.io/api/',
    API: '/settings/account/api/',
    MANAGE: '/manage/',
    FORUM: 'https://forum.sentry.io/',
    GITHUB_ISSUES: 'https://github.com/getsentry/sentry/issues',
    SERVICE_STATUS: 'https://status.sentry.io/',
};
var HOME_ICON_SIZE = 56;
var flexCenter = react_1.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n"], ["\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n"])));
var SettingsIndex = /** @class */ (function (_super) {
    tslib_1.__extends(SettingsIndex, _super);
    function SettingsIndex() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SettingsIndex.prototype.componentDidUpdate = function (prevProps) {
        var organization = this.props.organization;
        if (prevProps.organization === organization) {
            return;
        }
        // if there is no org in context, SidebarDropdown uses an org from `withLatestContext`
        // (which queries the org index endpoint instead of org details)
        // and does not have `access` info
        if (organization && typeof organization.access === 'undefined') {
            organizations_1.fetchOrganizationDetails(organization.slug, {
                setActive: true,
                loadProjects: true,
            });
        }
    };
    SettingsIndex.prototype.render = function () {
        var organization = this.props.organization;
        var user = configStore_1.default.get('user');
        var isOnPremise = configStore_1.default.get('isOnPremise');
        var organizationSettingsUrl = (organization && "/settings/" + organization.slug + "/") || '';
        var supportLinkProps = {
            isOnPremise: isOnPremise,
            href: LINKS.FORUM,
            to: organizationSettingsUrl + "support",
        };
        var supportText = isOnPremise ? locale_1.t('Community Forums') : locale_1.t('Contact Support');
        return (<react_document_title_1.default title={organization ? organization.slug + " Settings" : 'Settings'}>
        <settingsLayout_1.default {...this.props}>
          <GridLayout>
            <demoModeGate_1.default>
              <GridPanel>
                <HomePanelHeader>
                  <HomeLinkIcon to="/settings/account/">
                    <AvatarContainer>
                      <userAvatar_1.default user={user} size={HOME_ICON_SIZE}/>
                    </AvatarContainer>
                    {locale_1.t('My Account')}
                  </HomeLinkIcon>
                </HomePanelHeader>

                <HomePanelBody>
                  <h3>{locale_1.t('Quick links')}:</h3>
                  <ul>
                    <li>
                      <HomeLink to="/settings/account/security/">
                        {locale_1.t('Change my password')}
                      </HomeLink>
                    </li>
                    <li>
                      <HomeLink to="/settings/account/notifications/">
                        {locale_1.t('Notification Preferences')}
                      </HomeLink>
                    </li>
                    <li>
                      <HomeLink to="/settings/account/">{locale_1.t('Change my avatar')}</HomeLink>
                    </li>
                  </ul>
                </HomePanelBody>
              </GridPanel>
            </demoModeGate_1.default>

            {/* if admin */}
            <GridPanel>
              {!organization && <loadingIndicator_1.default overlay hideSpinner/>}
              <HomePanelHeader>
                <HomeLinkIcon to={organizationSettingsUrl}>
                  {organization ? (<AvatarContainer>
                      <organizationAvatar_1.default organization={organization} size={HOME_ICON_SIZE}/>
                    </AvatarContainer>) : (<HomeIcon color="green300">
                      <icons_1.IconStack size="lg"/>
                    </HomeIcon>)}
                  <OrganizationName>
                    {organization ? organization.slug : locale_1.t('No Organization')}
                  </OrganizationName>
                </HomeLinkIcon>
              </HomePanelHeader>
              <HomePanelBody>
                <h3>{locale_1.t('Quick links')}:</h3>
                <ul>
                  <li>
                    <HomeLink to={organizationSettingsUrl + "projects/"}>
                      {locale_1.t('Projects')}
                    </HomeLink>
                  </li>
                  <li>
                    <HomeLink to={organizationSettingsUrl + "teams/"}>
                      {locale_1.t('Teams')}
                    </HomeLink>
                  </li>
                  <li>
                    <HomeLink to={organizationSettingsUrl + "members/"}>
                      {locale_1.t('Members')}
                    </HomeLink>
                  </li>
                </ul>
              </HomePanelBody>
            </GridPanel>

            <GridPanel>
              <HomePanelHeader>
                <ExternalHomeLink isCentered href={LINKS.DOCUMENTATION}>
                  <HomeIcon color="orange400">
                    <icons_1.IconDocs size="lg"/>
                  </HomeIcon>
                </ExternalHomeLink>
                <ExternalHomeLink href={LINKS.DOCUMENTATION}>
                  {locale_1.t('Documentation')}
                </ExternalHomeLink>
              </HomePanelHeader>

              <HomePanelBody>
                <h3>{locale_1.t('Quick links')}:</h3>
                <ul>
                  <li>
                    <ExternalHomeLink href={LINKS.DOCUMENTATION_QUICKSTART}>
                      {locale_1.t('Quickstart Guide')}
                    </ExternalHomeLink>
                  </li>
                  <li>
                    <ExternalHomeLink href={LINKS.DOCUMENTATION_PLATFORMS}>
                      {locale_1.t('Platforms & Frameworks')}
                    </ExternalHomeLink>
                  </li>
                  <li>
                    <ExternalHomeLink href={LINKS.DOCUMENTATION_CLI}>
                      {locale_1.t('Sentry CLI')}
                    </ExternalHomeLink>
                  </li>
                </ul>
              </HomePanelBody>
            </GridPanel>

            <GridPanel>
              <HomePanelHeader>
                <SupportLinkComponent isCentered {...supportLinkProps}>
                  <HomeIcon color="purple300">
                    <icons_1.IconSupport size="lg"/>
                  </HomeIcon>
                  {locale_1.t('Support')}
                </SupportLinkComponent>
              </HomePanelHeader>

              <HomePanelBody>
                <h3>{locale_1.t('Quick links')}:</h3>
                <ul>
                  <li>
                    <SupportLinkComponent {...supportLinkProps}>
                      {supportText}
                    </SupportLinkComponent>
                  </li>
                  <li>
                    <ExternalHomeLink href={LINKS.GITHUB_ISSUES}>
                      {locale_1.t('Sentry on GitHub')}
                    </ExternalHomeLink>
                  </li>
                  <li>
                    <ExternalHomeLink href={LINKS.SERVICE_STATUS}>
                      {locale_1.t('Service Status')}
                    </ExternalHomeLink>
                  </li>
                </ul>
              </HomePanelBody>
            </GridPanel>

            <demoModeGate_1.default>
              <GridPanel>
                <HomePanelHeader>
                  <HomeLinkIcon to={LINKS.API}>
                    <HomeIcon>
                      <icons_1.IconLock size="lg"/>
                    </HomeIcon>
                    {locale_1.t('API Keys')}
                  </HomeLinkIcon>
                </HomePanelHeader>

                <HomePanelBody>
                  <h3>{locale_1.t('Quick links')}:</h3>
                  <ul>
                    <li>
                      <HomeLink to={LINKS.API}>{locale_1.t('Auth Tokens')}</HomeLink>
                    </li>
                    <li>
                      <HomeLink to={organizationSettingsUrl + "developer-settings/"}>
                        {locale_1.t('Your Integrations')}
                      </HomeLink>
                    </li>
                    <li>
                      <ExternalHomeLink href={LINKS.DOCUMENTATION_API}>
                        {locale_1.t('Documentation')}
                      </ExternalHomeLink>
                    </li>
                  </ul>
                </HomePanelBody>
              </GridPanel>
            </demoModeGate_1.default>
          </GridLayout>
        </settingsLayout_1.default>
      </react_document_title_1.default>);
    };
    return SettingsIndex;
}(React.Component));
exports.SettingsIndex = SettingsIndex;
exports.default = withLatestContext_1.default(SettingsIndex);
var HomePanelHeader = styled_1.default(panels_1.PanelHeader)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  background: ", ";\n  flex-direction: column;\n  text-align: center;\n  justify-content: center;\n  font-size: 18px;\n  text-transform: unset;\n  padding: 35px 30px;\n"], ["\n  background: ", ";\n  flex-direction: column;\n  text-align: center;\n  justify-content: center;\n  font-size: 18px;\n  text-transform: unset;\n  padding: 35px 30px;\n"])), function (p) { return p.theme.background; });
var HomePanelBody = styled_1.default(panels_1.PanelBody)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  padding: 30px;\n\n  h3 {\n    font-size: 14px;\n  }\n\n  ul {\n    margin: 0;\n    li {\n      line-height: 1.6;\n      /* Bullet color */\n      color: ", ";\n    }\n  }\n"], ["\n  padding: 30px;\n\n  h3 {\n    font-size: 14px;\n  }\n\n  ul {\n    margin: 0;\n    li {\n      line-height: 1.6;\n      /* Bullet color */\n      color: ", ";\n    }\n  }\n"])), function (p) { return p.theme.gray200; });
var HomeIcon = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  background: ", ";\n  color: ", ";\n  width: ", "px;\n  height: ", "px;\n  border-radius: ", "px;\n  display: flex;\n  justify-content: center;\n  align-items: center;\n  margin-bottom: 20px;\n"], ["\n  background: ", ";\n  color: ", ";\n  width: ", "px;\n  height: ", "px;\n  border-radius: ", "px;\n  display: flex;\n  justify-content: center;\n  align-items: center;\n  margin-bottom: 20px;\n"])), function (p) { return p.theme[p.color || 'gray300']; }, function (p) { return p.theme.white; }, HOME_ICON_SIZE, HOME_ICON_SIZE, HOME_ICON_SIZE);
var HomeLink = styled_1.default(link_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n\n  &:hover {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.purple300; }, function (p) { return p.theme.purple300; });
var HomeLinkIcon = styled_1.default(HomeLink)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  overflow: hidden;\n  width: 100%;\n  ", ";\n"], ["\n  overflow: hidden;\n  width: 100%;\n  ", ";\n"])), flexCenter);
var ExternalHomeLink = styled_1.default(function (props) { return (<externalLink_1.default {...omit_1.default(props, 'isCentered')}/>); })(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n\n  &:hover {\n    color: ", ";\n  }\n\n  ", ";\n"], ["\n  color: ", ";\n\n  &:hover {\n    color: ", ";\n  }\n\n  ", ";\n"])), function (p) { return p.theme.purple300; }, function (p) { return p.theme.purple300; }, function (p) { return p.isCentered && flexCenter; });
var SupportLinkComponent = function (_a) {
    var isCentered = _a.isCentered, isOnPremise = _a.isOnPremise, href = _a.href, to = _a.to, props = tslib_1.__rest(_a, ["isCentered", "isOnPremise", "href", "to"]);
    return isOnPremise ? (<ExternalHomeLink isCentered={isCentered} href={href} {...props}/>) : (<HomeLink to={to} {...props}/>);
};
var AvatarContainer = styled_1.default('div')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  margin-bottom: 20px;\n"], ["\n  margin-bottom: 20px;\n"])));
var OrganizationName = styled_1.default('div')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  line-height: 1.1em;\n\n  ", ";\n"], ["\n  line-height: 1.1em;\n\n  ", ";\n"])), overflowEllipsis_1.default);
var GridLayout = styled_1.default('div')(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr 1fr 1fr;\n  grid-gap: 16px;\n"], ["\n  display: grid;\n  grid-template-columns: 1fr 1fr 1fr;\n  grid-gap: 16px;\n"])));
var GridPanel = styled_1.default(panels_1.Panel)(templateObject_11 || (templateObject_11 = tslib_1.__makeTemplateObject(["\n  margin-bottom: 0;\n"], ["\n  margin-bottom: 0;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11;
//# sourceMappingURL=settingsIndex.jsx.map