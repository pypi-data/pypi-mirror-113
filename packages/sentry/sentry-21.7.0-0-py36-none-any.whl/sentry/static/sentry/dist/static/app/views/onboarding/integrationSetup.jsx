Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
require("prism-sentry/index.css");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var framer_motion_1 = require("framer-motion");
var modal_1 = require("app/actionCreators/modal");
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var platforms_1 = tslib_1.__importDefault(require("app/data/platforms"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var advancedAnalytics_1 = require("app/utils/advancedAnalytics");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var integrationUtil_1 = require("app/utils/integrationUtil");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var addIntegrationButton_1 = tslib_1.__importDefault(require("app/views/organizationIntegrations/addIntegrationButton"));
var firstEventFooter_1 = tslib_1.__importDefault(require("./components/firstEventFooter"));
var addInstallationInstructions_1 = tslib_1.__importDefault(require("./components/integrations/addInstallationInstructions"));
var postInstallCodeSnippet_1 = tslib_1.__importDefault(require("./components/integrations/postInstallCodeSnippet"));
var setupIntroduction_1 = tslib_1.__importDefault(require("./components/setupIntroduction"));
var IntegrationSetup = /** @class */ (function (_super) {
    tslib_1.__extends(IntegrationSetup, _super);
    function IntegrationSetup() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loadedPlatform: null,
            hasError: false,
            provider: null,
            installed: false,
        };
        _this.fetchData = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, api, organization, platform, integrationSlug, endpoint, integrations, provider, error_1;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization, platform = _a.platform, integrationSlug = _a.integrationSlug;
                        if (!integrationSlug) {
                            return [2 /*return*/];
                        }
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        endpoint = "/organizations/" + organization.slug + "/config/integrations/?provider_key=" + integrationSlug;
                        return [4 /*yield*/, api.requestPromise(endpoint)];
                    case 2:
                        integrations = _b.sent();
                        provider = integrations.providers[0];
                        this.setState({ provider: provider, loadedPlatform: platform, hasError: false });
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _b.sent();
                        this.setState({ hasError: error_1 });
                        throw error_1;
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleFullDocsClick = function () {
            var organization = _this.props.organization;
            advancedAnalytics_1.trackAdvancedAnalyticsEvent('growth.onboarding_view_full_docs', {}, organization);
        };
        _this.trackSwitchToManual = function () {
            var _a = _this.props, organization = _a.organization, integrationSlug = _a.integrationSlug;
            integrationUtil_1.trackIntegrationEvent('integrations.switch_manual_sdk_setup', {
                integration_type: 'first_party',
                integration: integrationSlug,
                view: 'onboarding',
            }, organization);
        };
        _this.handleAddIntegration = function () {
            _this.setState({ installed: true });
        };
        _this.renderSetupInstructions = function () {
            var _a, _b, _c;
            var platform = _this.props.platform;
            var loadedPlatform = _this.state.loadedPlatform;
            var currentPlatform = (_a = loadedPlatform !== null && loadedPlatform !== void 0 ? loadedPlatform : platform) !== null && _a !== void 0 ? _a : 'other';
            return (<setupIntroduction_1.default stepHeaderText={locale_1.t('Automatically instrument %s', (_c = (_b = platforms_1.default.find(function (p) { return p.id === currentPlatform; })) === null || _b === void 0 ? void 0 : _b.name) !== null && _c !== void 0 ? _c : '')} platform={currentPlatform}/>);
        };
        return _this;
    }
    IntegrationSetup.prototype.componentDidMount = function () {
        this.fetchData();
    };
    IntegrationSetup.prototype.componentDidUpdate = function (nextProps) {
        if (nextProps.platform !== this.props.platform ||
            nextProps.project !== this.props.project) {
            this.fetchData();
        }
    };
    Object.defineProperty(IntegrationSetup.prototype, "manualSetupUrl", {
        get: function () {
            var search = window.location.search;
            // honor any existing query params
            var separator = search.includes('?') ? '&' : '?';
            return "" + search + separator + "manual=1";
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(IntegrationSetup.prototype, "platformDocs", {
        get: function () {
            // TODO: make dynamic based on the integration
            return 'https://docs.sentry.io/product/integrations/aws-lambda/';
        },
        enumerable: false,
        configurable: true
    });
    IntegrationSetup.prototype.renderIntegrationInstructions = function () {
        var _a = this.props, organization = _a.organization, project = _a.project;
        var provider = this.state.provider;
        if (!provider || !project) {
            return null;
        }
        return (<react_1.Fragment>
        {this.renderSetupInstructions()}
        <framer_motion_1.motion.p variants={{
                initial: { opacity: 0 },
                animate: { opacity: 1 },
                exit: { opacity: 0 },
            }}>
          {locale_1.tct("Don't have have permissions to create a Cloudformation stack? [link:Invite your team instead].", {
                link: <button_1.default priority="link" onClick={modal_1.openInviteMembersModal}/>,
            })}
        </framer_motion_1.motion.p>
        <framer_motion_1.motion.div variants={{
                initial: { opacity: 0 },
                animate: { opacity: 1 },
                exit: { opacity: 0 },
            }}>
          <addInstallationInstructions_1.default />
        </framer_motion_1.motion.div>

        <DocsWrapper>
          <StyledButtonBar gap={1}>
            <addIntegrationButton_1.default provider={provider} onAddIntegration={this.handleAddIntegration} organization={organization} priority="primary" size="small" analyticsParams={{ view: 'onboarding', already_installed: false }} modalParams={{ projectId: project.id }}/>
            <button_1.default size="small" to={{
                pathname: window.location.pathname,
                query: { manual: '1' },
            }} onClick={this.trackSwitchToManual}>
              {locale_1.t('Manual Setup')}
            </button_1.default>
          </StyledButtonBar>
        </DocsWrapper>
      </react_1.Fragment>);
    };
    IntegrationSetup.prototype.renderPostInstallInstructions = function () {
        var _a = this.props, organization = _a.organization, project = _a.project, platform = _a.platform;
        var provider = this.state.provider;
        if (!project || !provider || !platform) {
            return null;
        }
        return (<react_1.Fragment>
        {this.renderSetupInstructions()}
        <postInstallCodeSnippet_1.default provider={provider} platform={platform} isOnboarding/>
        <firstEventFooter_1.default project={project} organization={organization} docsLink={this.platformDocs} docsOnClick={this.handleFullDocsClick}/>
      </react_1.Fragment>);
    };
    IntegrationSetup.prototype.render = function () {
        var platform = this.props.platform;
        var hasError = this.state.hasError;
        var loadingError = (<loadingError_1.default message={locale_1.t('Failed to load the integration for the %s platform.', platform)} onRetry={this.fetchData}/>);
        var testOnlyAlert = (<alert_1.default type="warning">
        Platform documentation is not rendered in for tests in CI
      </alert_1.default>);
        return (<react_1.Fragment>
        {this.state.installed
                ? this.renderPostInstallInstructions()
                : this.renderIntegrationInstructions()}
        {getDynamicText_1.default({
                value: !hasError ? null : loadingError,
                fixed: testOnlyAlert,
            })}
      </react_1.Fragment>);
    };
    return IntegrationSetup;
}(react_1.Component));
var DocsWrapper = styled_1.default(framer_motion_1.motion.div)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject([""], [""])));
DocsWrapper.defaultProps = {
    initial: { opacity: 0, y: 40 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0 },
};
var StyledButtonBar = styled_1.default(buttonBar_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n  width: max-content;\n\n  @media (max-width: ", ") {\n    width: auto;\n    grid-row-gap: ", ";\n    grid-auto-flow: row;\n  }\n"], ["\n  margin-top: ", ";\n  width: max-content;\n\n  @media (max-width: ", ") {\n    width: auto;\n    grid-row-gap: ", ";\n    grid-auto-flow: row;\n  }\n"])), space_1.default(3), function (p) { return p.theme.breakpoints[0]; }, space_1.default(1));
exports.default = withOrganization_1.default(withApi_1.default(IntegrationSetup));
var templateObject_1, templateObject_2;
//# sourceMappingURL=integrationSetup.jsx.map