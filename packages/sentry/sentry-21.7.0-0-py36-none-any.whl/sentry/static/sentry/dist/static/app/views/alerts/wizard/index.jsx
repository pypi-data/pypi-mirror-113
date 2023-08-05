Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var featureDisabled_1 = tslib_1.__importDefault(require("app/components/acl/featureDisabled"));
var createAlertButton_1 = tslib_1.__importDefault(require("app/components/createAlertButton"));
var hovercard_1 = tslib_1.__importDefault(require("app/components/hovercard"));
var Layout = tslib_1.__importStar(require("app/components/layouts/thirds"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var list_1 = tslib_1.__importDefault(require("app/components/list"));
var listItem_1 = tslib_1.__importDefault(require("app/components/list/listItem"));
var panels_1 = require("app/components/panels");
var sentryDocumentTitle_1 = tslib_1.__importDefault(require("app/components/sentryDocumentTitle"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var builderBreadCrumbs_1 = tslib_1.__importDefault(require("app/views/alerts/builder/builderBreadCrumbs"));
var types_1 = require("app/views/alerts/incidentRules/types");
var options_1 = require("./options");
var radioPanelGroup_1 = tslib_1.__importDefault(require("./radioPanelGroup"));
var DEFAULT_ALERT_OPTION = 'issues';
var AlertWizard = /** @class */ (function (_super) {
    tslib_1.__extends(AlertWizard, _super);
    function AlertWizard() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            alertOption: DEFAULT_ALERT_OPTION,
        };
        _this.handleChangeAlertOption = function (alertOption) {
            var organization = _this.props.organization;
            _this.setState({ alertOption: alertOption });
            analytics_1.trackAnalyticsEvent({
                eventKey: 'alert_wizard.option_viewed',
                eventName: 'Alert Wizard: Option Viewed',
                organization_id: organization.id,
                alert_type: alertOption,
            });
        };
        return _this;
    }
    AlertWizard.prototype.componentDidMount = function () {
        // capture landing on the alert wizard page and viewing the issue alert by default
        var organization = this.props.organization;
        analytics_1.trackAnalyticsEvent({
            eventKey: 'alert_wizard.option_viewed',
            eventName: 'Alert Wizard: Option Viewed',
            organization_id: organization.id,
            alert_type: DEFAULT_ALERT_OPTION,
        });
    };
    AlertWizard.prototype.renderCreateAlertButton = function () {
        var _a;
        var _b = this.props, organization = _b.organization, location = _b.location, projectId = _b.params.projectId;
        var alertOption = this.state.alertOption;
        var metricRuleTemplate = options_1.AlertWizardRuleTemplates[alertOption];
        var isMetricAlert = !!metricRuleTemplate;
        var isTransactionDataset = (metricRuleTemplate === null || metricRuleTemplate === void 0 ? void 0 : metricRuleTemplate.dataset) === types_1.Dataset.TRANSACTIONS;
        var to = {
            pathname: "/organizations/" + organization.slug + "/alerts/" + projectId + "/new/",
            query: tslib_1.__assign(tslib_1.__assign({}, (metricRuleTemplate && metricRuleTemplate)), { createFromWizard: true, referrer: (_a = location === null || location === void 0 ? void 0 : location.query) === null || _a === void 0 ? void 0 : _a.referrer }),
        };
        var noFeatureMessage = locale_1.t('Requires incidents feature.');
        var renderNoAccess = function (p) { return (<hovercard_1.default body={<featureDisabled_1.default features={p.features} hideHelpToggle message={noFeatureMessage} featureName={noFeatureMessage}/>}>
        {p.children(p)}
      </hovercard_1.default>); };
        return (<feature_1.default features={isTransactionDataset
                ? ['incidents', 'performance-view']
                : isMetricAlert
                    ? ['incidents']
                    : []} requireAll organization={organization} hookName="feature-disabled:alert-wizard-performance" renderDisabled={renderNoAccess}>
        {function (_a) {
                var hasFeature = _a.hasFeature;
                return (<WizardButtonContainer onClick={function () {
                        return analytics_1.trackAnalyticsEvent({
                            eventKey: 'alert_wizard.option_selected',
                            eventName: 'Alert Wizard: Option Selected',
                            organization_id: organization.id,
                            alert_type: alertOption,
                        });
                    }}>
            <createAlertButton_1.default organization={organization} projectSlug={projectId} disabled={!hasFeature} priority="primary" to={to} hideIcon>
              {locale_1.t('Set Conditions')}
            </createAlertButton_1.default>
          </WizardButtonContainer>);
            }}
      </feature_1.default>);
    };
    AlertWizard.prototype.render = function () {
        var _this = this;
        var _a = this.props, hasMetricAlerts = _a.hasMetricAlerts, organization = _a.organization, projectId = _a.params.projectId, routes = _a.routes, location = _a.location;
        var alertOption = this.state.alertOption;
        var title = locale_1.t('Alert Creation Wizard');
        var panelContent = options_1.AlertWizardPanelContent[alertOption];
        return (<react_1.Fragment>
        <sentryDocumentTitle_1.default title={title} projectSlug={projectId}/>

        <Layout.Header>
          <StyledHeaderContent>
            <builderBreadCrumbs_1.default hasMetricAlerts={hasMetricAlerts} orgSlug={organization.slug} projectSlug={projectId} title={locale_1.t('Select Alert')} routes={routes} location={location} canChangeProject/>
            <Layout.Title>{locale_1.t('Select Alert')}</Layout.Title>
          </StyledHeaderContent>
        </Layout.Header>
        <StyledLayoutBody>
          <Layout.Main fullWidth>
            <WizardBody>
              <WizardOptions>
                <Styledh2>{locale_1.t('Errors')}</Styledh2>
                {options_1.AlertWizardOptions.map(function (_a, i) {
                var categoryHeading = _a.categoryHeading, options = _a.options;
                return (<OptionsWrapper key={categoryHeading}>
                    {i > 0 && <Styledh2>{categoryHeading}</Styledh2>}
                    <radioPanelGroup_1.default choices={options.map(function (alertType) {
                        return [alertType, options_1.AlertWizardAlertNames[alertType]];
                    })} onChange={_this.handleChangeAlertOption} value={alertOption} label="alert-option"/>
                  </OptionsWrapper>);
            })}
              </WizardOptions>
              <WizardPanel visible={!!panelContent && !!alertOption}>
                <WizardPanelBody>
                  <div>
                    <panels_1.PanelHeader>{options_1.AlertWizardAlertNames[alertOption]}</panels_1.PanelHeader>
                    <panels_1.PanelBody withPadding>
                      <PanelDescription>
                        {panelContent.description}{' '}
                        {panelContent.docsLink && (<externalLink_1.default href={panelContent.docsLink}>
                            {locale_1.t('Learn more')}
                          </externalLink_1.default>)}
                      </PanelDescription>
                      <WizardImage src={panelContent.illustration}/>
                      <ExampleHeader>{locale_1.t('Examples')}</ExampleHeader>
                      <ExampleList symbol="bullet">
                        {panelContent.examples.map(function (example, i) { return (<ExampleItem key={i}>{example}</ExampleItem>); })}
                      </ExampleList>
                    </panels_1.PanelBody>
                  </div>
                  <WizardFooter>{this.renderCreateAlertButton()}</WizardFooter>
                </WizardPanelBody>
              </WizardPanel>
            </WizardBody>
          </Layout.Main>
        </StyledLayoutBody>
      </react_1.Fragment>);
    };
    return AlertWizard;
}(react_1.Component));
var StyledLayoutBody = styled_1.default(Layout.Body)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: -", ";\n"], ["\n  margin-bottom: -", ";\n"])), space_1.default(3));
var StyledHeaderContent = styled_1.default(Layout.HeaderContent)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  overflow: visible;\n"], ["\n  overflow: visible;\n"])));
var Styledh2 = styled_1.default('h2')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  font-weight: normal;\n  font-size: ", ";\n  margin-bottom: ", " !important;\n"], ["\n  font-weight: normal;\n  font-size: ", ";\n  margin-bottom: ", " !important;\n"])), function (p) { return p.theme.fontSizeExtraLarge; }, space_1.default(1));
var WizardBody = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  padding-top: ", ";\n"], ["\n  display: flex;\n  padding-top: ", ";\n"])), space_1.default(1));
var WizardOptions = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  flex: 3;\n  margin-right: ", ";\n  padding-right: ", ";\n  max-width: 300px;\n"], ["\n  flex: 3;\n  margin-right: ", ";\n  padding-right: ", ";\n  max-width: 300px;\n"])), space_1.default(3), space_1.default(3));
var WizardImage = styled_1.default('img')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  max-height: 300px;\n"], ["\n  max-height: 300px;\n"])));
var WizardPanel = styled_1.default(panels_1.Panel)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  max-width: 700px;\n  position: sticky;\n  top: 20px;\n  flex: 5;\n  display: flex;\n  ", ";\n  flex-direction: column;\n  align-items: start;\n  align-self: flex-start;\n  ", ";\n\n  @keyframes pop {\n    0% {\n      transform: translateY(30px);\n      opacity: 0;\n    }\n    100% {\n      transform: translateY(0);\n      opacity: 1;\n    }\n  }\n"], ["\n  max-width: 700px;\n  position: sticky;\n  top: 20px;\n  flex: 5;\n  display: flex;\n  ", ";\n  flex-direction: column;\n  align-items: start;\n  align-self: flex-start;\n  ", ";\n\n  @keyframes pop {\n    0% {\n      transform: translateY(30px);\n      opacity: 0;\n    }\n    100% {\n      transform: translateY(0);\n      opacity: 1;\n    }\n  }\n"])), function (p) { return !p.visible && 'visibility: hidden'; }, function (p) { return p.visible && 'animation: 0.6s pop ease forwards'; });
var ExampleList = styled_1.default(list_1.default)(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", " !important;\n"], ["\n  margin-bottom: ", " !important;\n"])), space_1.default(2));
var WizardPanelBody = styled_1.default(panels_1.PanelBody)(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n  min-width: 100%;\n"], ["\n  flex: 1;\n  min-width: 100%;\n"])));
var PanelDescription = styled_1.default('p')(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(2));
var ExampleHeader = styled_1.default('div')(templateObject_11 || (templateObject_11 = tslib_1.__makeTemplateObject(["\n  margin: 0 0 ", " 0;\n  font-size: ", ";\n"], ["\n  margin: 0 0 ", " 0;\n  font-size: ", ";\n"])), space_1.default(1), function (p) { return p.theme.fontSizeLarge; });
var ExampleItem = styled_1.default(listItem_1.default)(templateObject_12 || (templateObject_12 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
var OptionsWrapper = styled_1.default('div')(templateObject_13 || (templateObject_13 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n\n  &:last-child {\n    margin-bottom: 0;\n  }\n"], ["\n  margin-bottom: ", ";\n\n  &:last-child {\n    margin-bottom: 0;\n  }\n"])), space_1.default(4));
var WizardFooter = styled_1.default('div')(templateObject_14 || (templateObject_14 = tslib_1.__makeTemplateObject(["\n  border-top: 1px solid ", ";\n  padding: ", " ", " ", " ", ";\n"], ["\n  border-top: 1px solid ", ";\n  padding: ", " ", " ", " ", ";\n"])), function (p) { return p.theme.border; }, space_1.default(1.5), space_1.default(1.5), space_1.default(1.5), space_1.default(1.5));
var WizardButtonContainer = styled_1.default('div')(templateObject_15 || (templateObject_15 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n"], ["\n  display: flex;\n  justify-content: flex-end;\n"])));
exports.default = AlertWizard;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14, templateObject_15;
//# sourceMappingURL=index.jsx.map