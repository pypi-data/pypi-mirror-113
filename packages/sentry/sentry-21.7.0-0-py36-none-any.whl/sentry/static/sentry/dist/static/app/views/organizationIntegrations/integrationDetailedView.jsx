Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var abstractIntegrationDetailedView_1 = tslib_1.__importDefault(require("./abstractIntegrationDetailedView"));
var addIntegrationButton_1 = tslib_1.__importDefault(require("./addIntegrationButton"));
var installedIntegration_1 = tslib_1.__importDefault(require("./installedIntegration"));
var IntegrationDetailedView = /** @class */ (function (_super) {
    tslib_1.__extends(IntegrationDetailedView, _super);
    function IntegrationDetailedView() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onInstall = function (integration) {
            // send the user to the configure integration view for that integration
            var orgId = _this.props.params.orgId;
            _this.props.router.push("/settings/" + orgId + "/integrations/" + integration.provider.key + "/" + integration.id + "/");
        };
        _this.onRemove = function (integration) {
            var orgId = _this.props.params.orgId;
            var origIntegrations = tslib_1.__spreadArray([], tslib_1.__read(_this.state.configurations));
            var integrations = _this.state.configurations.filter(function (i) { return i.id !== integration.id; });
            _this.setState({ configurations: integrations });
            var options = {
                method: 'DELETE',
                error: function () {
                    _this.setState({ configurations: origIntegrations });
                    indicator_1.addErrorMessage(locale_1.t('Failed to remove Integration'));
                },
            };
            _this.api.request("/organizations/" + orgId + "/integrations/" + integration.id + "/", options);
        };
        _this.onDisable = function (integration) {
            var url;
            var _a = tslib_1.__read(integration.domainName.split('/'), 2), domainName = _a[0], orgName = _a[1];
            if (integration.accountType === 'User') {
                url = "https://" + domainName + "/settings/installations/";
            }
            else {
                url = "https://" + domainName + "/organizations/" + orgName + "/settings/installations/";
            }
            window.open(url, '_blank');
        };
        _this.handleExternalInstall = function () {
            _this.trackIntegrationEvent('integrations.installation_start');
        };
        return _this;
    }
    IntegrationDetailedView.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, integrationSlug = _a.integrationSlug;
        var baseEndpoints = [
            [
                'information',
                "/organizations/" + orgId + "/config/integrations/?provider_key=" + integrationSlug,
            ],
            [
                'configurations',
                "/organizations/" + orgId + "/integrations/?provider_key=" + integrationSlug + "&includeConfig=0",
            ],
        ];
        return baseEndpoints;
    };
    Object.defineProperty(IntegrationDetailedView.prototype, "integrationType", {
        get: function () {
            return 'first_party';
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(IntegrationDetailedView.prototype, "provider", {
        get: function () {
            return this.state.information.providers[0];
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(IntegrationDetailedView.prototype, "description", {
        get: function () {
            return this.metadata.description;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(IntegrationDetailedView.prototype, "author", {
        get: function () {
            return this.metadata.author;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(IntegrationDetailedView.prototype, "alerts", {
        get: function () {
            var provider = this.provider;
            var metadata = this.metadata;
            // The server response for integration installations includes old icon CSS classes
            // We map those to the currently in use values to their react equivalents
            // and fallback to IconFlag just in case.
            var alerts = (metadata.aspects.alerts || []).map(function (item) {
                switch (item.icon) {
                    case 'icon-warning':
                    case 'icon-warning-sm':
                        return tslib_1.__assign(tslib_1.__assign({}, item), { icon: <icons_1.IconWarning /> });
                    default:
                        return tslib_1.__assign(tslib_1.__assign({}, item), { icon: <icons_1.IconFlag /> });
                }
            });
            if (!provider.canAdd && metadata.aspects.externalInstall) {
                alerts.push({
                    type: 'warning',
                    icon: <icons_1.IconOpen />,
                    text: metadata.aspects.externalInstall.noticeText,
                });
            }
            return alerts;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(IntegrationDetailedView.prototype, "resourceLinks", {
        get: function () {
            var metadata = this.metadata;
            return [
                { url: metadata.source_url, title: 'View Source' },
                { url: metadata.issue_url, title: 'Report Issue' },
            ];
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(IntegrationDetailedView.prototype, "metadata", {
        get: function () {
            return this.provider.metadata;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(IntegrationDetailedView.prototype, "isEnabled", {
        get: function () {
            return this.state.configurations.length > 0;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(IntegrationDetailedView.prototype, "installationStatus", {
        get: function () {
            return this.isEnabled ? 'Installed' : 'Not Installed';
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(IntegrationDetailedView.prototype, "integrationName", {
        get: function () {
            return this.provider.name;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(IntegrationDetailedView.prototype, "featureData", {
        get: function () {
            return this.metadata.features;
        },
        enumerable: false,
        configurable: true
    });
    IntegrationDetailedView.prototype.renderTopButton = function (disabledFromFeatures, userHasAccess) {
        var organization = this.props.organization;
        var provider = this.provider;
        var metadata = provider.metadata;
        var size = 'small';
        var priority = 'primary';
        var buttonProps = {
            style: { marginBottom: space_1.default(1) },
            size: size,
            priority: priority,
            'data-test-id': 'install-button',
            disabled: disabledFromFeatures,
            organization: organization,
        };
        if (!userHasAccess) {
            return this.renderRequestIntegrationButton();
        }
        if (provider.canAdd) {
            return (<addIntegrationButton_1.default provider={provider} onAddIntegration={this.onInstall} analyticsParams={{
                    view: 'integrations_directory_integration_detail',
                    already_installed: this.installationStatus !== 'Not Installed',
                }} {...buttonProps}/>);
        }
        if (metadata.aspects.externalInstall) {
            return (<button_1.default icon={<icons_1.IconOpen />} href={metadata.aspects.externalInstall.url} onClick={this.handleExternalInstall} external {...buttonProps}>
          {metadata.aspects.externalInstall.buttonText}
        </button_1.default>);
        }
        // This should never happen but we can't return undefined without some refactoring.
        return <react_1.Fragment />;
    };
    IntegrationDetailedView.prototype.renderConfigurations = function () {
        var _this = this;
        var configurations = this.state.configurations;
        var organization = this.props.organization;
        var provider = this.provider;
        if (configurations.length) {
            return configurations.map(function (integration) {
                return (<InstallWrapper key={integration.id}>
            <installedIntegration_1.default organization={organization} provider={provider} integration={integration} onRemove={_this.onRemove} onDisable={_this.onDisable} data-test-id={integration.id} trackIntegrationEvent={_this.trackIntegrationEvent}/>
          </InstallWrapper>);
            });
        }
        return this.renderEmptyConfigurations();
    };
    return IntegrationDetailedView;
}(abstractIntegrationDetailedView_1.default));
var InstallWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n  border: 1px solid ", ";\n  border-bottom: none;\n  background-color: ", ";\n\n  &:last-child {\n    border-bottom: 1px solid ", ";\n  }\n"], ["\n  padding: ", ";\n  border: 1px solid ", ";\n  border-bottom: none;\n  background-color: ", ";\n\n  &:last-child {\n    border-bottom: 1px solid ", ";\n  }\n"])), space_1.default(2), function (p) { return p.theme.border; }, function (p) { return p.theme.background; }, function (p) { return p.theme.border; });
exports.default = withOrganization_1.default(IntegrationDetailedView);
var templateObject_1;
//# sourceMappingURL=integrationDetailedView.jsx.map