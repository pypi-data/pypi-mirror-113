Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var navigation_1 = require("app/actionCreators/navigation");
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var createAlertButton_1 = tslib_1.__importDefault(require("app/components/createAlertButton"));
var globalSelectionLink_1 = tslib_1.__importDefault(require("app/components/globalSelectionLink"));
var Layout = tslib_1.__importStar(require("app/components/layouts/thirds"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var AlertHeader = function (_a) {
    var router = _a.router, organization = _a.organization, activeTab = _a.activeTab;
    /**
     * Incidents list is currently at the organization level, but the link needs to
     * go down to a specific project scope.
     */
    var handleNavigateToSettings = function (e) {
        e.preventDefault();
        navigation_1.navigateTo("/settings/" + organization.slug + "/projects/:projectId/alerts/", router);
    };
    var alertRulesLink = (<li className={activeTab === 'rules' ? 'active' : ''}>
      <globalSelectionLink_1.default to={"/organizations/" + organization.slug + "/alerts/rules/"}>
        {locale_1.t('Alert Rules')}
      </globalSelectionLink_1.default>
    </li>);
    return (<React.Fragment>
      <BorderlessHeader>
        <StyledLayoutHeaderContent>
          <StyledLayoutTitle>{locale_1.t('Alerts')}</StyledLayoutTitle>
        </StyledLayoutHeaderContent>
        <Layout.HeaderActions>
          <Actions gap={1}>
            <createAlertButton_1.default organization={organization} iconProps={{ size: 'sm' }} priority="primary" referrer="alert_stream" showPermissionGuide>
              {locale_1.t('Create Alert Rule')}
            </createAlertButton_1.default>
            <button_1.default onClick={handleNavigateToSettings} href="#" icon={<icons_1.IconSettings size="sm"/>} aria-label="Settings"/>
          </Actions>
        </Layout.HeaderActions>
      </BorderlessHeader>
      <TabLayoutHeader>
        <Layout.HeaderNavTabs underlined>
          <feature_1.default features={['alert-details-redesign']} organization={organization}>
            {function (_a) {
            var hasFeature = _a.hasFeature;
            return !hasFeature ? (<React.Fragment>
                  <feature_1.default features={['incidents']} organization={organization}>
                    <li className={activeTab === 'stream' ? 'active' : ''}>
                      <globalSelectionLink_1.default to={"/organizations/" + organization.slug + "/alerts/"}>
                        {locale_1.t('Metric Alerts')}
                      </globalSelectionLink_1.default>
                    </li>
                  </feature_1.default>
                  {alertRulesLink}
                </React.Fragment>) : (<React.Fragment>
                  {alertRulesLink}
                  <li className={activeTab === 'stream' ? 'active' : ''}>
                    <globalSelectionLink_1.default to={"/organizations/" + organization.slug + "/alerts/"}>
                      {locale_1.t('History')}
                    </globalSelectionLink_1.default>
                  </li>
                </React.Fragment>);
        }}
          </feature_1.default>
        </Layout.HeaderNavTabs>
      </TabLayoutHeader>
    </React.Fragment>);
};
exports.default = AlertHeader;
var BorderlessHeader = styled_1.default(Layout.Header)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  border-bottom: 0;\n\n  /* Not enough buttons to change direction for tablet view */\n  grid-template-columns: 1fr auto;\n"], ["\n  border-bottom: 0;\n\n  /* Not enough buttons to change direction for tablet view */\n  grid-template-columns: 1fr auto;\n"])));
var StyledLayoutHeaderContent = styled_1.default(Layout.HeaderContent)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-bottom: 0;\n  margin-right: ", ";\n"], ["\n  margin-bottom: 0;\n  margin-right: ", ";\n"])), space_1.default(2));
var StyledLayoutTitle = styled_1.default(Layout.Title)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space_1.default(0.5));
var TabLayoutHeader = styled_1.default(Layout.Header)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  padding-top: ", ";\n\n  @media (max-width: ", ") {\n    padding-top: ", ";\n  }\n"], ["\n  padding-top: ", ";\n\n  @media (max-width: ", ") {\n    padding-top: ", ";\n  }\n"])), space_1.default(1), function (p) { return p.theme.breakpoints[1]; }, space_1.default(1));
var Actions = styled_1.default(buttonBar_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  height: 32px;\n"], ["\n  height: 32px;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=header.jsx.map