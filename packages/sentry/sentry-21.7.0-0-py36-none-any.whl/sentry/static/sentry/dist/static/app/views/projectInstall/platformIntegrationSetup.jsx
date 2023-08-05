Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
require("prism-sentry/index.css");
var react_1 = require("react");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var platforms_1 = tslib_1.__importDefault(require("app/data/platforms"));
var locale_1 = require("app/locale");
var organization_1 = require("app/styles/organization");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var advancedAnalytics_1 = require("app/utils/advancedAnalytics");
var integrationUtil_1 = require("app/utils/integrationUtil");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var firstEventFooter_1 = tslib_1.__importDefault(require("app/views/onboarding/components/firstEventFooter"));
var addInstallationInstructions_1 = tslib_1.__importDefault(require("app/views/onboarding/components/integrations/addInstallationInstructions"));
var postInstallCodeSnippet_1 = tslib_1.__importDefault(require("app/views/onboarding/components/integrations/postInstallCodeSnippet"));
var addIntegrationButton_1 = tslib_1.__importDefault(require("app/views/organizationIntegrations/addIntegrationButton"));
var platformHeaderButtonBar_1 = tslib_1.__importDefault(require("./components/platformHeaderButtonBar"));
var PlatformIntegrationSetup = /** @class */ (function (_super) {
    tslib_1.__extends(PlatformIntegrationSetup, _super);
    function PlatformIntegrationSetup() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleFullDocsClick = function () {
            var organization = _this.props.organization;
            advancedAnalytics_1.trackAdvancedAnalyticsEvent('growth.onboarding_view_full_docs', {}, organization);
        };
        _this.handleAddIntegration = function () {
            _this.setState({ installed: true });
        };
        _this.trackSwitchToManual = function () {
            var _a = _this.props, organization = _a.organization, integrationSlug = _a.integrationSlug;
            integrationUtil_1.trackIntegrationEvent('integrations.switch_manual_sdk_setup', {
                integration_type: 'first_party',
                integration: integrationSlug,
                view: 'project_creation',
            }, organization);
        };
        return _this;
    }
    PlatformIntegrationSetup.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { installed: false, integrations: { providers: [] }, project: null });
    };
    PlatformIntegrationSetup.prototype.componentDidMount = function () {
        window.scrollTo(0, 0);
        var platform = this.props.params.platform;
        // redirect if platform is not known.
        if (!platform || platform === 'other') {
            this.redirectToNeutralDocs();
        }
    };
    Object.defineProperty(PlatformIntegrationSetup.prototype, "provider", {
        get: function () {
            var providers = this.state.integrations.providers;
            return providers.length ? providers[0] : null;
        },
        enumerable: false,
        configurable: true
    });
    PlatformIntegrationSetup.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, integrationSlug = _a.integrationSlug, params = _a.params;
        if (!integrationSlug) {
            return [];
        }
        return [
            [
                'integrations',
                "/organizations/" + organization.slug + "/config/integrations/?provider_key=" + integrationSlug,
            ],
            ['project', "/projects/" + organization.slug + "/" + params.projectId + "/"],
        ];
    };
    PlatformIntegrationSetup.prototype.redirectToNeutralDocs = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        var url = "/organizations/" + orgId + "/projects/" + projectId + "/getting-started/";
        react_router_1.browserHistory.push(url);
    };
    PlatformIntegrationSetup.prototype.render = function () {
        var _a = this.props, organization = _a.organization, params = _a.params;
        var _b = this.state, installed = _b.installed, project = _b.project;
        var projectId = params.projectId, orgId = params.orgId, platform = params.platform;
        var provider = this.provider;
        var platformIntegration = platforms_1.default.find(function (p) { return p.id === platform; });
        if (!provider || !platformIntegration || !project) {
            return null;
        }
        var gettingStartedLink = "/organizations/" + orgId + "/projects/" + projectId + "/getting-started/";
        // TODO: make dynamic when adding more integrations
        var docsLink = 'https://docs.sentry.io/product/integrations/aws-lambda/';
        return (<OuterWrapper>
        <StyledPageHeader>
          <StyledTitle>
            {locale_1.t('Automatically instrument %s', platformIntegration.name)}
          </StyledTitle>
          <platformHeaderButtonBar_1.default gettingStartedLink={gettingStartedLink} docsLink={docsLink}/>
        </StyledPageHeader>
        <InnerWrapper>
          {!installed ? (<react_1.Fragment>
              <addInstallationInstructions_1.default />
              <StyledButtonBar gap={1}>
                <addIntegrationButton_1.default provider={provider} onAddIntegration={this.handleAddIntegration} organization={organization} priority="primary" size="small" analyticsParams={{ view: 'project_creation', already_installed: false }} modalParams={{ projectId: project.id }}/>
                <button_1.default size="small" to={{
                    pathname: window.location.pathname,
                    query: { manual: '1' },
                }} onClick={this.trackSwitchToManual}>
                  {locale_1.t('Manual Setup')}
                </button_1.default>
              </StyledButtonBar>
            </react_1.Fragment>) : (<react_1.Fragment>
              <postInstallCodeSnippet_1.default provider={provider}/>
              <firstEventFooter_1.default project={project} organization={organization} docsLink={docsLink} docsOnClick={this.handleFullDocsClick}/>
            </react_1.Fragment>)}
        </InnerWrapper>
      </OuterWrapper>);
    };
    return PlatformIntegrationSetup;
}(asyncComponent_1.default));
var StyledButtonBar = styled_1.default(buttonBar_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n  width: max-content;\n\n  @media (max-width: ", ") {\n    width: auto;\n    grid-row-gap: ", ";\n    grid-auto-flow: row;\n  }\n"], ["\n  margin-top: ", ";\n  width: max-content;\n\n  @media (max-width: ", ") {\n    width: auto;\n    grid-row-gap: ", ";\n    grid-auto-flow: row;\n  }\n"])), space_1.default(3), function (p) { return p.theme.breakpoints[0]; }, space_1.default(1));
var InnerWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  width: 850px;\n"], ["\n  width: 850px;\n"])));
var OuterWrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  margin-top: 50px;\n"], ["\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  margin-top: 50px;\n"])));
var StyledPageHeader = styled_1.default(organization_1.PageHeader)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(3));
var StyledTitle = styled_1.default('h2')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  margin: 0 ", " 0 0;\n"], ["\n  margin: 0 ", " 0 0;\n"])), space_1.default(3));
exports.default = withOrganization_1.default(PlatformIntegrationSetup);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=platformIntegrationSetup.jsx.map