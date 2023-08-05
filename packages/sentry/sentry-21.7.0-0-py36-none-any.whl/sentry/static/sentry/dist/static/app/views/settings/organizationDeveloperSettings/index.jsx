Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var sentryApps_1 = require("app/actionCreators/sentryApps");
var access_1 = tslib_1.__importDefault(require("app/components/acl/access"));
var alertLink_1 = tslib_1.__importDefault(require("app/components/alertLink"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var panels_1 = require("app/components/panels");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var routeTitle_1 = tslib_1.__importDefault(require("app/utils/routeTitle"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var sentryApplicationRow_1 = tslib_1.__importDefault(require("app/views/settings/organizationDeveloperSettings/sentryApplicationRow"));
var OrganizationDeveloperSettings = /** @class */ (function (_super) {
    tslib_1.__extends(OrganizationDeveloperSettings, _super);
    function OrganizationDeveloperSettings() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.removeApp = function (app) {
            var apps = _this.state.applications.filter(function (a) { return a.slug !== app.slug; });
            sentryApps_1.removeSentryApp(_this.api, app).then(function () {
                _this.setState({ applications: apps });
            }, function () { });
        };
        _this.renderApplicationRow = function (app) {
            var organization = _this.props.organization;
            return (<sentryApplicationRow_1.default key={app.uuid} app={app} organization={organization} onRemoveApp={_this.removeApp}/>);
        };
        return _this;
    }
    OrganizationDeveloperSettings.prototype.getTitle = function () {
        var orgId = this.props.params.orgId;
        return routeTitle_1.default(locale_1.t('Developer Settings'), orgId, false);
    };
    OrganizationDeveloperSettings.prototype.getEndpoints = function () {
        var orgId = this.props.params.orgId;
        return [['applications', "/organizations/" + orgId + "/sentry-apps/"]];
    };
    OrganizationDeveloperSettings.prototype.renderInternalIntegrations = function () {
        var orgId = this.props.params.orgId;
        var organization = this.props.organization;
        var integrations = this.state.applications.filter(function (app) { return app.status === 'internal'; });
        var isEmpty = integrations.length === 0;
        var permissionTooltipText = locale_1.t('Manager or Owner permissions required to add an internal integration.');
        var action = (<access_1.default organization={organization} access={['org:write']}>
        {function (_a) {
                var hasAccess = _a.hasAccess;
                return (<button_1.default priority="primary" disabled={!hasAccess} title={!hasAccess ? permissionTooltipText : undefined} size="small" to={"/settings/" + orgId + "/developer-settings/new-internal/"} icon={<icons_1.IconAdd size="xs" isCircled/>}>
            {locale_1.t('New Internal Integration')}
          </button_1.default>);
            }}
      </access_1.default>);
        return (<panels_1.Panel>
        <panels_1.PanelHeader hasButtons>
          {locale_1.t('Internal Integrations')}
          {action}
        </panels_1.PanelHeader>
        <panels_1.PanelBody>
          {!isEmpty ? (integrations.map(this.renderApplicationRow)) : (<emptyMessage_1.default>
              {locale_1.t('No internal integrations have been created yet.')}
            </emptyMessage_1.default>)}
        </panels_1.PanelBody>
      </panels_1.Panel>);
    };
    OrganizationDeveloperSettings.prototype.renderExernalIntegrations = function () {
        var orgId = this.props.params.orgId;
        var organization = this.props.organization;
        var integrations = this.state.applications.filter(function (app) { return app.status !== 'internal'; });
        var isEmpty = integrations.length === 0;
        var permissionTooltipText = locale_1.t('Manager or Owner permissions required to add a public integration.');
        var action = (<access_1.default organization={organization} access={['org:write']}>
        {function (_a) {
                var hasAccess = _a.hasAccess;
                return (<button_1.default priority="primary" disabled={!hasAccess} title={!hasAccess ? permissionTooltipText : undefined} size="small" to={"/settings/" + orgId + "/developer-settings/new-public/"} icon={<icons_1.IconAdd size="xs" isCircled/>}>
            {locale_1.t('New Public Integration')}
          </button_1.default>);
            }}
      </access_1.default>);
        return (<panels_1.Panel>
        <panels_1.PanelHeader hasButtons>
          {locale_1.t('Public Integrations')}
          {action}
        </panels_1.PanelHeader>
        <panels_1.PanelBody>
          {!isEmpty ? (integrations.map(this.renderApplicationRow)) : (<emptyMessage_1.default>
              {locale_1.t('No public integrations have been created yet.')}
            </emptyMessage_1.default>)}
        </panels_1.PanelBody>
      </panels_1.Panel>);
    };
    OrganizationDeveloperSettings.prototype.renderBody = function () {
        return (<div>
        <settingsPageHeader_1.default title={locale_1.t('Developer Settings')}/>
        <alertLink_1.default href="https://docs.sentry.io/product/integrations/integration-platform/">
          {locale_1.t('Have questions about the Integration Platform? Learn more about it in our docs.')}
        </alertLink_1.default>
        {this.renderExernalIntegrations()}
        {this.renderInternalIntegrations()}
      </div>);
    };
    return OrganizationDeveloperSettings;
}(asyncView_1.default));
exports.default = withOrganization_1.default(OrganizationDeveloperSettings);
//# sourceMappingURL=index.jsx.map