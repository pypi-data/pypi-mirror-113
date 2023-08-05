Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var sentryAppInstallations_1 = require("app/actionCreators/sentryAppInstallations");
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var organizationAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/organizationAvatar"));
var selectControl_1 = tslib_1.__importDefault(require("app/components/forms/selectControl"));
var sentryAppDetailsModal_1 = tslib_1.__importDefault(require("app/components/modals/sentryAppDetailsModal"));
var narrowLayout_1 = tslib_1.__importDefault(require("app/components/narrowLayout"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var integrationUtil_1 = require("app/utils/integrationUtil");
var queryString_1 = require("app/utils/queryString");
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var field_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field"));
var SentryAppExternalInstallation = /** @class */ (function (_super) {
    tslib_1.__extends(SentryAppExternalInstallation, _super);
    function SentryAppExternalInstallation() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.hasAccess = function (org) { return org.access.includes('org:integrations'); };
        _this.onClose = function () {
            // if we came from somewhere, go back there. Otherwise, back to the integrations page
            var selectedOrgSlug = _this.state.selectedOrgSlug;
            var newUrl = document.referrer || "/settings/" + selectedOrgSlug + "/integrations/";
            window.location.assign(newUrl);
        };
        _this.onInstall = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, organization, sentryApp, install, queryParams, redirectUrl;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.state, organization = _a.organization, sentryApp = _a.sentryApp;
                        if (!organization || !sentryApp) {
                            return [2 /*return*/, undefined];
                        }
                        integrationUtil_1.trackIntegrationEvent('integrations.installation_start', {
                            integration_type: 'sentry_app',
                            integration: sentryApp.slug,
                            view: 'external_install',
                            integration_status: sentryApp.status,
                        }, organization);
                        return [4 /*yield*/, sentryAppInstallations_1.installSentryApp(this.api, organization.slug, sentryApp)];
                    case 1:
                        install = _b.sent();
                        // installation is complete if the status is installed
                        if (install.status === 'installed') {
                            integrationUtil_1.trackIntegrationEvent('integrations.installation_complete', {
                                integration_type: 'sentry_app',
                                integration: sentryApp.slug,
                                view: 'external_install',
                                integration_status: sentryApp.status,
                            }, organization);
                        }
                        if (sentryApp.redirectUrl) {
                            queryParams = {
                                installationId: install.uuid,
                                code: install.code,
                                orgSlug: organization.slug,
                            };
                            redirectUrl = queryString_1.addQueryParamsToExistingUrl(sentryApp.redirectUrl, queryParams);
                            return [2 /*return*/, window.location.assign(redirectUrl)];
                        }
                        return [2 /*return*/, this.onClose()];
                }
            });
        }); };
        _this.onSelectOrg = function (orgSlug) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, organization, installations, isInstalled, err_1;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        this.setState({ selectedOrgSlug: orgSlug, reloading: true });
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, Promise.all([
                                this.api.requestPromise("/organizations/" + orgSlug + "/"),
                                this.api.requestPromise("/organizations/" + orgSlug + "/sentry-app-installations/"),
                            ])];
                    case 2:
                        _a = tslib_1.__read.apply(void 0, [_b.sent(), 2]), organization = _a[0], installations = _a[1];
                        isInstalled = installations
                            .map(function (install) { return install.app.slug; })
                            .includes(this.sentryAppSlug);
                        // all state fields should be set at the same time so analytics in SentryAppDetailsModal works properly
                        this.setState({ organization: organization, isInstalled: isInstalled, reloading: false });
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _b.sent();
                        indicator_1.addErrorMessage(locale_1.t('Failed to retrieve organization or integration details'));
                        this.setState({ reloading: false });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.onRequestSuccess = function (_a) {
            var stateKey = _a.stateKey, data = _a.data;
            // if only one org, we can immediately update our selected org
            if (stateKey === 'organizations' && data.length === 1) {
                _this.onSelectOrg(data[0].slug);
            }
        };
        return _this;
    }
    SentryAppExternalInstallation.prototype.getDefaultState = function () {
        var state = _super.prototype.getDefaultState.call(this);
        return tslib_1.__assign(tslib_1.__assign({}, state), { selectedOrgSlug: null, organization: null, organizations: [], reloading: false });
    };
    SentryAppExternalInstallation.prototype.getEndpoints = function () {
        return [
            ['organizations', '/organizations/'],
            ['sentryApp', "/sentry-apps/" + this.sentryAppSlug + "/"],
        ];
    };
    SentryAppExternalInstallation.prototype.getTitle = function () {
        return locale_1.t('Choose Installation Organization');
    };
    Object.defineProperty(SentryAppExternalInstallation.prototype, "sentryAppSlug", {
        get: function () {
            return this.props.params.sentryAppSlug;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SentryAppExternalInstallation.prototype, "isSingleOrg", {
        get: function () {
            return this.state.organizations.length === 1;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SentryAppExternalInstallation.prototype, "isSentryAppInternal", {
        get: function () {
            var sentryApp = this.state.sentryApp;
            return sentryApp && sentryApp.status === 'internal';
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SentryAppExternalInstallation.prototype, "isSentryAppUnavailableForOrg", {
        get: function () {
            var _a;
            var _b = this.state, sentryApp = _b.sentryApp, selectedOrgSlug = _b.selectedOrgSlug;
            // if the app is unpublished for a different org
            return (selectedOrgSlug &&
                ((_a = sentryApp === null || sentryApp === void 0 ? void 0 : sentryApp.owner) === null || _a === void 0 ? void 0 : _a.slug) !== selectedOrgSlug &&
                sentryApp.status === 'unpublished');
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SentryAppExternalInstallation.prototype, "disableInstall", {
        get: function () {
            var _a = this.state, reloading = _a.reloading, isInstalled = _a.isInstalled;
            return isInstalled || reloading || this.isSentryAppUnavailableForOrg;
        },
        enumerable: false,
        configurable: true
    });
    SentryAppExternalInstallation.prototype.getOptions = function () {
        return this.state.organizations.map(function (org) { return [
            org.slug,
            <div key={org.slug}>
        <organizationAvatar_1.default organization={org}/>
        <OrgNameHolder>{org.slug}</OrgNameHolder>
      </div>,
        ]; });
    };
    SentryAppExternalInstallation.prototype.renderInternalAppError = function () {
        var sentryApp = this.state.sentryApp;
        return (<alert_1.default type="error" icon={<icons_1.IconFlag size="md"/>}>
        {locale_1.tct('Integration [sentryAppName] is an internal integration. Internal integrations are automatically installed', {
                sentryAppName: <strong>{sentryApp.name}</strong>,
            })}
      </alert_1.default>);
    };
    SentryAppExternalInstallation.prototype.checkAndRenderError = function () {
        var _a, _b;
        var _c = this.state, organization = _c.organization, selectedOrgSlug = _c.selectedOrgSlug, isInstalled = _c.isInstalled, sentryApp = _c.sentryApp;
        if (selectedOrgSlug && organization && !this.hasAccess(organization)) {
            return (<alert_1.default type="error" icon={<icons_1.IconFlag size="md"/>}>
          <p>
            {locale_1.tct("You do not have permission to install integrations in\n          [organization]. Ask an organization owner or manager to\n          visit this page to finish installing this integration.", { organization: <strong>{organization.slug}</strong> })}
          </p>
          <InstallLink>{window.location.href}</InstallLink>
        </alert_1.default>);
        }
        if (isInstalled && organization) {
            return (<alert_1.default type="error" icon={<icons_1.IconFlag size="md"/>}>
          {locale_1.tct('Integration [sentryAppName] already installed for [organization]', {
                    organization: <strong>{organization.name}</strong>,
                    sentryAppName: <strong>{sentryApp.name}</strong>,
                })}
        </alert_1.default>);
        }
        if (this.isSentryAppUnavailableForOrg) {
            // use the slug of the owner if we have it, otherwise use 'another organization'
            var ownerSlug = (_b = (_a = sentryApp === null || sentryApp === void 0 ? void 0 : sentryApp.owner) === null || _a === void 0 ? void 0 : _a.slug) !== null && _b !== void 0 ? _b : 'another organization';
            return (<alert_1.default type="error" icon={<icons_1.IconFlag size="md"/>}>
          {locale_1.tct('Integration [sentryAppName] is an unpublished integration for [otherOrg]. An unpublished integration can only be installed on the organization which created it.', {
                    sentryAppName: <strong>{sentryApp.name}</strong>,
                    otherOrg: <strong>{ownerSlug}</strong>,
                })}
        </alert_1.default>);
        }
        return null;
    };
    SentryAppExternalInstallation.prototype.renderMultiOrgView = function () {
        var _this = this;
        var _a = this.state, selectedOrgSlug = _a.selectedOrgSlug, sentryApp = _a.sentryApp;
        return (<div>
        <p>
          {locale_1.tct('Please pick a specific [organization:organization] to install [sentryAppName]', {
                organization: <strong />,
                sentryAppName: <strong>{sentryApp.name}</strong>,
            })}
        </p>
        <field_1.default label={locale_1.t('Organization')} inline={false} stacked required>
          {function () { return (<selectControl_1.default onChange={function (_a) {
                var value = _a.value;
                return _this.onSelectOrg(value);
            }} value={selectedOrgSlug} placeholder={locale_1.t('Select an organization')} choices={_this.getOptions()}/>); }}
        </field_1.default>
      </div>);
    };
    SentryAppExternalInstallation.prototype.renderSingleOrgView = function () {
        var _a = this.state, organizations = _a.organizations, sentryApp = _a.sentryApp;
        // pull the name out of organizations since state.organization won't be loaded initially
        var organizationName = organizations[0].name;
        return (<div>
        <p>
          {locale_1.tct('You are installing [sentryAppName] for organization [organization]', {
                organization: <strong>{organizationName}</strong>,
                sentryAppName: <strong>{sentryApp.name}</strong>,
            })}
        </p>
      </div>);
    };
    SentryAppExternalInstallation.prototype.renderMainContent = function () {
        var _a = this.state, organization = _a.organization, sentryApp = _a.sentryApp;
        return (<div>
        <OrgViewHolder>
          {this.isSingleOrg ? this.renderSingleOrgView() : this.renderMultiOrgView()}
        </OrgViewHolder>
        {this.checkAndRenderError()}
        {organization && (<sentryAppDetailsModal_1.default sentryApp={sentryApp} organization={organization} onInstall={this.onInstall} closeModal={this.onClose} isInstalled={this.disableInstall}/>)}
      </div>);
    };
    SentryAppExternalInstallation.prototype.renderBody = function () {
        return (<narrowLayout_1.default>
        <Content>
          <h3>{locale_1.t('Finish integration installation')}</h3>
          {this.isSentryAppInternal
                ? this.renderInternalAppError()
                : this.renderMainContent()}
        </Content>
      </narrowLayout_1.default>);
    };
    return SentryAppExternalInstallation;
}(asyncView_1.default));
exports.default = SentryAppExternalInstallation;
var InstallLink = styled_1.default('pre')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: 0;\n  background: #fbe3e1;\n"], ["\n  margin-bottom: 0;\n  background: #fbe3e1;\n"])));
var OrgNameHolder = styled_1.default('span')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-left: 5px;\n"], ["\n  margin-left: 5px;\n"])));
var Content = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin-bottom: 40px;\n"], ["\n  margin-bottom: 40px;\n"])));
var OrgViewHolder = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin-bottom: 20px;\n"], ["\n  margin-bottom: 20px;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=sentryAppExternalInstallation.jsx.map