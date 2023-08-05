Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var list_1 = tslib_1.__importDefault(require("app/components/list"));
var listItem_1 = tslib_1.__importDefault(require("app/components/list/listItem"));
var navTabs_1 = tslib_1.__importDefault(require("app/components/navTabs"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var integrationUtil_1 = require("app/utils/integrationUtil");
var marked_1 = require("app/utils/marked");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var addIntegration_1 = tslib_1.__importDefault(require("app/views/organizationIntegrations/addIntegration"));
var integrationAlertRules_1 = tslib_1.__importDefault(require("app/views/organizationIntegrations/integrationAlertRules"));
var integrationCodeMappings_1 = tslib_1.__importDefault(require("app/views/organizationIntegrations/integrationCodeMappings"));
var integrationExternalTeamMappings_1 = tslib_1.__importDefault(require("app/views/organizationIntegrations/integrationExternalTeamMappings"));
var integrationExternalUserMappings_1 = tslib_1.__importDefault(require("app/views/organizationIntegrations/integrationExternalUserMappings"));
var integrationItem_1 = tslib_1.__importDefault(require("app/views/organizationIntegrations/integrationItem"));
var integrationMainSettings_1 = tslib_1.__importDefault(require("app/views/organizationIntegrations/integrationMainSettings"));
var integrationRepos_1 = tslib_1.__importDefault(require("app/views/organizationIntegrations/integrationRepos"));
var integrationServerlessFunctions_1 = tslib_1.__importDefault(require("app/views/organizationIntegrations/integrationServerlessFunctions"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var jsonForm_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/jsonForm"));
var breadcrumbTitle_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsBreadcrumb/breadcrumbTitle"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var ConfigureIntegration = /** @class */ (function (_super) {
    tslib_1.__extends(ConfigureIntegration, _super);
    function ConfigureIntegration() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onTabChange = function (value) {
            _this.setState({ tab: value });
        };
        _this.onUpdateIntegration = function () {
            _this.setState(_this.getDefaultState(), _this.fetchData);
        };
        _this.getAction = function (provider) {
            var integration = _this.state.integration;
            var action = provider && provider.key === 'pagerduty' ? (<addIntegration_1.default provider={provider} onInstall={_this.onUpdateIntegration} account={integration.domainName} organization={_this.props.organization}>
          {function (onClick) { return (<button_1.default priority="primary" size="small" icon={<icons_1.IconAdd size="xs" isCircled/>} onClick={function () { return onClick(); }}>
              {locale_1.t('Add Services')}
            </button_1.default>); }}
        </addIntegration_1.default>) : null;
            return action;
        };
        return _this;
    }
    ConfigureIntegration.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, integrationId = _a.integrationId;
        return [
            ['config', "/organizations/" + orgId + "/config/integrations/"],
            ['integration', "/organizations/" + orgId + "/integrations/" + integrationId + "/"],
        ];
    };
    ConfigureIntegration.prototype.componentDidMount = function () {
        var location = this.props.location;
        var value = ['codeMappings', 'userMappings', 'teamMappings'].find(function (tab) { return tab === location.query.tab; }) || 'repos';
        // eslint-disable-next-line react/no-did-mount-set-state
        this.setState({ tab: value });
    };
    ConfigureIntegration.prototype.onRequestSuccess = function (_a) {
        var stateKey = _a.stateKey, data = _a.data;
        if (stateKey !== 'integration') {
            return;
        }
        integrationUtil_1.trackIntegrationEvent('integrations.details_viewed', {
            integration: data.provider.key,
            integration_type: 'first_party',
        }, this.props.organization);
    };
    ConfigureIntegration.prototype.getTitle = function () {
        return this.state.integration
            ? this.state.integration.provider.name
            : 'Configure Integration';
    };
    ConfigureIntegration.prototype.hasStacktraceLinking = function (provider) {
        // CodeOwners will only work if the provider has StackTrace Linking
        return (provider.features.includes('stacktrace-link') &&
            this.props.organization.features.includes('integrations-stacktrace-link'));
    };
    ConfigureIntegration.prototype.hasCodeOwners = function () {
        return this.props.organization.features.includes('integrations-codeowners');
    };
    ConfigureIntegration.prototype.isCustomIntegration = function () {
        var integration = this.state.integration;
        var organization = this.props.organization;
        return (organization.features.includes('integrations-custom-scm') &&
            integration.provider.key === 'custom_scm');
    };
    Object.defineProperty(ConfigureIntegration.prototype, "tab", {
        get: function () {
            return this.state.tab || 'repos';
        },
        enumerable: false,
        configurable: true
    });
    // TODO(Steve): Refactor components into separate tabs and use more generic tab logic
    ConfigureIntegration.prototype.renderMainTab = function (provider) {
        var _a, _b, _c, _d;
        var orgId = this.props.params.orgId;
        var integration = this.state.integration;
        var instructions = (_b = (_a = integration.dynamicDisplayInformation) === null || _a === void 0 ? void 0 : _a.configure_integration) === null || _b === void 0 ? void 0 : _b.instructions;
        return (<react_1.Fragment>
        <breadcrumbTitle_1.default routes={this.props.routes} title={integration.provider.name}/>

        {integration.configOrganization.length > 0 && (<form_1.default hideFooter saveOnBlur allowUndo apiMethod="POST" initialData={integration.configData || {}} apiEndpoint={"/organizations/" + orgId + "/integrations/" + integration.id + "/"}>
            <jsonForm_1.default fields={integration.configOrganization} title={((_c = integration.provider.aspects.configure_integration) === null || _c === void 0 ? void 0 : _c.title) ||
                    locale_1.t('Organization Integration Settings')}/>
          </form_1.default>)}

        {instructions && instructions.length > 0 && (<alert_1.default type="info">
            {(instructions === null || instructions === void 0 ? void 0 : instructions.length) === 1 ? (<span dangerouslySetInnerHTML={{ __html: marked_1.singleLineRenderer(instructions[0]) }}/>) : (<list_1.default symbol={<icons_1.IconArrow size="xs" direction="right"/>}>
                {(_d = instructions === null || instructions === void 0 ? void 0 : instructions.map(function (instruction, i) { return (<listItem_1.default key={i}>
                    <span dangerouslySetInnerHTML={{ __html: marked_1.singleLineRenderer(instruction) }}/>
                  </listItem_1.default>); })) !== null && _d !== void 0 ? _d : []}
              </list_1.default>)}
          </alert_1.default>)}

        {provider.features.includes('alert-rule') && <integrationAlertRules_1.default />}

        {provider.features.includes('commits') && (<integrationRepos_1.default {...this.props} integration={integration}/>)}

        {provider.features.includes('serverless') && (<integrationServerlessFunctions_1.default integration={integration}/>)}
      </react_1.Fragment>);
    };
    ConfigureIntegration.prototype.renderBody = function () {
        var integration = this.state.integration;
        var provider = this.state.config.providers.find(function (p) { return p.key === integration.provider.key; });
        if (!provider) {
            return null;
        }
        var title = <integrationItem_1.default integration={integration}/>;
        var header = (<settingsPageHeader_1.default noTitleStyles title={title} action={this.getAction(provider)}/>);
        return (<react_1.Fragment>
        {header}
        {this.renderMainContent(provider)}
      </react_1.Fragment>);
    };
    // renders everything below header
    ConfigureIntegration.prototype.renderMainContent = function (provider) {
        var _this = this;
        // if no code mappings, render the single tab
        if (!this.hasStacktraceLinking(provider)) {
            return this.renderMainTab(provider);
        }
        // otherwise render the tab view
        var tabs = tslib_1.__spreadArray(tslib_1.__spreadArray([
            ['repos', locale_1.t('Repositories')],
            ['codeMappings', locale_1.t('Code Mappings')]
        ], tslib_1.__read((this.hasCodeOwners() ? [['userMappings', locale_1.t('User Mappings')]] : []))), tslib_1.__read((this.hasCodeOwners() ? [['teamMappings', locale_1.t('Team Mappings')]] : [])));
        if (this.isCustomIntegration()) {
            tabs.unshift(['settings', locale_1.t('Settings')]);
        }
        return (<react_1.Fragment>
        <navTabs_1.default underlined>
          {tabs.map(function (tabTuple) { return (<li key={tabTuple[0]} className={_this.tab === tabTuple[0] ? 'active' : ''} onClick={function () { return _this.onTabChange(tabTuple[0]); }}>
              <CapitalizedLink>{tabTuple[1]}</CapitalizedLink>
            </li>); })}
        </navTabs_1.default>
        {this.renderTabContent(this.tab, provider)}
      </react_1.Fragment>);
    };
    ConfigureIntegration.prototype.renderTabContent = function (tab, provider) {
        var integration = this.state.integration;
        var organization = this.props.organization;
        switch (tab) {
            case 'codeMappings':
                return <integrationCodeMappings_1.default integration={integration}/>;
            case 'repos':
                return this.renderMainTab(provider);
            case 'userMappings':
                return <integrationExternalUserMappings_1.default integration={integration}/>;
            case 'teamMappings':
                return <integrationExternalTeamMappings_1.default integration={integration}/>;
            case 'settings':
                return (<integrationMainSettings_1.default onUpdate={this.onUpdateIntegration} organization={organization} integration={integration}/>);
            default:
                return this.renderMainTab(provider);
        }
    };
    return ConfigureIntegration;
}(asyncView_1.default));
exports.default = withOrganization_1.default(ConfigureIntegration);
var CapitalizedLink = styled_1.default('a')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  text-transform: capitalize;\n"], ["\n  text-transform: capitalize;\n"])));
var templateObject_1;
//# sourceMappingURL=configureIntegration.jsx.map