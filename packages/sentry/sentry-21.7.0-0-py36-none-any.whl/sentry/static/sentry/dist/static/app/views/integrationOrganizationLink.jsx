Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_select_1 = require("react-select");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var utils_1 = require("@sentry/utils");
var indicator_1 = require("app/actionCreators/indicator");
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var selectControl_1 = tslib_1.__importDefault(require("app/components/forms/selectControl"));
var idBadge_1 = tslib_1.__importDefault(require("app/components/idBadge"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var narrowLayout_1 = tslib_1.__importDefault(require("app/components/narrowLayout"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var integrationUtil_1 = require("app/utils/integrationUtil");
var marked_1 = require("app/utils/marked");
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var addIntegration_1 = tslib_1.__importDefault(require("app/views/organizationIntegrations/addIntegration"));
var field_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field"));
var IntegrationOrganizationLink = /** @class */ (function (_super) {
    tslib_1.__extends(IntegrationOrganizationLink, _super);
    function IntegrationOrganizationLink() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.trackIntegrationEvent = function (eventName, startSession) {
            var _a = _this.state, organization = _a.organization, provider = _a.provider;
            // should have these set but need to make TS happy
            if (!organization || !provider) {
                return;
            }
            integrationUtil_1.trackIntegrationEvent(eventName, {
                integration_type: 'first_party',
                integration: provider.key,
                // We actually don't know if it's installed but neither does the user in the view and multiple installs is possible
                already_installed: false,
                view: 'external_install',
            }, organization, { startSession: !!startSession });
        };
        _this.getOrgBySlug = function (orgSlug) {
            return _this.state.organizations.find(function (org) { return org.slug === orgSlug; });
        };
        _this.onSelectOrg = function (_a) {
            var orgSlug = _a.value;
            return tslib_1.__awaiter(_this, void 0, void 0, function () {
                var _b, organization, providers, _err_1;
                return tslib_1.__generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            this.setState({ selectedOrgSlug: orgSlug, reloading: true, organization: undefined });
                            _c.label = 1;
                        case 1:
                            _c.trys.push([1, 3, , 4]);
                            return [4 /*yield*/, Promise.all([
                                    this.api.requestPromise("/organizations/" + orgSlug + "/"),
                                    this.api.requestPromise("/organizations/" + orgSlug + "/config/integrations/?provider_key=" + this.integrationSlug),
                                ])];
                        case 2:
                            _b = tslib_1.__read.apply(void 0, [_c.sent(), 2]), organization = _b[0], providers = _b[1].providers;
                            // should never happen with a valid provider
                            if (providers.length === 0) {
                                throw new Error('Invalid provider');
                            }
                            this.setState({ organization: organization, reloading: false, provider: providers[0] }, this.trackOpened);
                            return [3 /*break*/, 4];
                        case 3:
                            _err_1 = _c.sent();
                            indicator_1.addErrorMessage(locale_1.t('Failed to retrieve organization or integration details'));
                            this.setState({ reloading: false });
                            return [3 /*break*/, 4];
                        case 4: return [2 /*return*/];
                    }
                });
            });
        };
        _this.hasAccess = function () {
            var organization = _this.state.organization;
            return organization === null || organization === void 0 ? void 0 : organization.access.includes('org:integrations');
        };
        // used with Github to redirect to the the integration detail
        _this.onInstallWithInstallationId = function (data) {
            var organization = _this.state.organization;
            var orgId = organization && organization.slug;
            _this.props.router.push("/settings/" + orgId + "/integrations/" + data.provider.key + "/" + data.id + "/");
        };
        // non-Github redirects to the extension view where the backend will finish the installation
        _this.finishInstallation = function () {
            // add the selected org to the query parameters and then redirect back to configure
            var selectedOrgSlug = _this.state.selectedOrgSlug;
            var query = tslib_1.__assign({ orgSlug: selectedOrgSlug }, _this.queryParams);
            _this.trackInstallationStart();
            window.location.assign("/extensions/" + _this.integrationSlug + "/configure/?" + utils_1.urlEncode(query));
        };
        _this.customOption = function (orgProps) {
            var organization = _this.getOrgBySlug(orgProps.value);
            if (!organization) {
                return null;
            }
            return (<react_select_1.components.Option {...orgProps}>
        <idBadge_1.default organization={organization} avatarSize={20} displayName={organization.name} avatarProps={{ consistentWidth: true }}/>
      </react_select_1.components.Option>);
        };
        _this.customValueContainer = function (containerProps) {
            var valueList = containerProps.getValue();
            // if no value set, we want to return the default component that is rendered
            if (valueList.length === 0) {
                return <react_select_1.components.ValueContainer {...containerProps}/>;
            }
            var orgSlug = valueList[0].value;
            var organization = _this.getOrgBySlug(orgSlug);
            if (!organization) {
                return <react_select_1.components.ValueContainer {...containerProps}/>;
            }
            return (<react_select_1.components.ValueContainer {...containerProps}>
        <idBadge_1.default organization={organization} avatarSize={20} displayName={organization.name} avatarProps={{ consistentWidth: true }}/>
      </react_select_1.components.ValueContainer>);
        };
        return _this;
    }
    IntegrationOrganizationLink.prototype.getEndpoints = function () {
        return [['organizations', '/organizations/']];
    };
    IntegrationOrganizationLink.prototype.getTitle = function () {
        return locale_1.t('Choose Installation Organization');
    };
    IntegrationOrganizationLink.prototype.trackOpened = function () {
        this.trackIntegrationEvent('integrations.integration_viewed', true);
    };
    IntegrationOrganizationLink.prototype.trackInstallationStart = function () {
        this.trackIntegrationEvent('integrations.installation_start');
    };
    Object.defineProperty(IntegrationOrganizationLink.prototype, "integrationSlug", {
        get: function () {
            return this.props.params.integrationSlug;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(IntegrationOrganizationLink.prototype, "queryParams", {
        get: function () {
            return this.props.location.query;
        },
        enumerable: false,
        configurable: true
    });
    IntegrationOrganizationLink.prototype.onLoadAllEndpointsSuccess = function () {
        // auto select the org if there is only one
        var organizations = this.state.organizations;
        if (organizations.length === 1) {
            this.onSelectOrg({ value: organizations[0].slug });
        }
    };
    IntegrationOrganizationLink.prototype.renderAddButton = function () {
        var _this = this;
        var installationId = this.props.params.installationId;
        var _a = this.state, organization = _a.organization, provider = _a.provider;
        // should never happen but we need this check for TS
        if (!provider || !organization) {
            return null;
        }
        var features = provider.metadata.features;
        // Prepare the features list
        var featuresComponents = features.map(function (f) { return ({
            featureGate: f.featureGate,
            description: (<FeatureListItem dangerouslySetInnerHTML={{ __html: marked_1.singleLineRenderer(f.description) }}/>),
        }); });
        var IntegrationDirectoryFeatures = integrationUtil_1.getIntegrationFeatureGate().IntegrationDirectoryFeatures;
        // Github uses a different installation flow with the installationId as a parameter
        // We have to wrap our installation button with AddIntegration so we can get the
        // addIntegrationWithInstallationId callback.
        // if we don't hve an installationId, we need to use the finishInstallation callback.
        return (<IntegrationDirectoryFeatures organization={organization} features={featuresComponents}>
        {function (_a) {
                var disabled = _a.disabled;
                return (<addIntegration_1.default provider={provider} onInstall={_this.onInstallWithInstallationId} organization={organization}>
            {function (addIntegrationWithInstallationId) { return (<ButtonWrapper>
                <button_1.default priority="primary" disabled={!_this.hasAccess() || disabled} onClick={function () {
                            return installationId
                                ? addIntegrationWithInstallationId({
                                    installation_id: installationId,
                                })
                                : _this.finishInstallation();
                        }}>
                  {locale_1.t('Install %s', provider.name)}
                </button_1.default>
              </ButtonWrapper>); }}
          </addIntegration_1.default>);
            }}
      </IntegrationDirectoryFeatures>);
    };
    IntegrationOrganizationLink.prototype.renderBottom = function () {
        var _a = this.state, organization = _a.organization, selectedOrgSlug = _a.selectedOrgSlug, provider = _a.provider, reloading = _a.reloading;
        var FeatureList = integrationUtil_1.getIntegrationFeatureGate().FeatureList;
        if (reloading) {
            return <loadingIndicator_1.default />;
        }
        return (<react_1.Fragment>
        {selectedOrgSlug && organization && !this.hasAccess() && (<alert_1.default type="error" icon={<icons_1.IconFlag size="md"/>}>
            <p>
              {locale_1.tct("You do not have permission to install integrations in\n                [organization]. Ask an organization owner or manager to\n                visit this page to finish installing this integration.", { organization: <strong>{organization.slug}</strong> })}
            </p>
            <InstallLink>{window.location.href}</InstallLink>
          </alert_1.default>)}

        {provider && organization && this.hasAccess() && FeatureList && (<react_1.Fragment>
            <p>
              {locale_1.tct('The following features will be available for [organization] when installed.', { organization: <strong>{organization.slug}</strong> })}
            </p>
            <FeatureList organization={organization} features={provider.metadata.features} provider={provider}/>
          </react_1.Fragment>)}

        <div className="form-actions">{this.renderAddButton()}</div>
      </react_1.Fragment>);
    };
    IntegrationOrganizationLink.prototype.renderBody = function () {
        var selectedOrgSlug = this.state.selectedOrgSlug;
        var options = this.state.organizations.map(function (org) { return ({
            value: org.slug,
            label: org.name,
        }); });
        return (<narrowLayout_1.default>
        <h3>{locale_1.t('Finish integration installation')}</h3>
        <p>
          {locale_1.tct("Please pick a specific [organization:organization] to link with\n            your integration installation of [integation].", {
                organization: <strong />,
                integation: <strong>{this.integrationSlug}</strong>,
            })}
        </p>

        <field_1.default label={locale_1.t('Organization')} inline={false} stacked required>
          <selectControl_1.default onChange={this.onSelectOrg} value={selectedOrgSlug} placeholder={locale_1.t('Select an organization')} options={options} components={{
                Option: this.customOption,
                ValueContainer: this.customValueContainer,
            }}/>
        </field_1.default>
        {this.renderBottom()}
      </narrowLayout_1.default>);
    };
    return IntegrationOrganizationLink;
}(asyncView_1.default));
exports.default = IntegrationOrganizationLink;
var InstallLink = styled_1.default('pre')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: 0;\n  background: #fbe3e1;\n"], ["\n  margin-bottom: 0;\n  background: #fbe3e1;\n"])));
var FeatureListItem = styled_1.default('span')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  line-height: 24px;\n"], ["\n  line-height: 24px;\n"])));
var ButtonWrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin-left: auto;\n  align-self: center;\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n"], ["\n  margin-left: auto;\n  align-self: center;\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=integrationOrganizationLink.jsx.map