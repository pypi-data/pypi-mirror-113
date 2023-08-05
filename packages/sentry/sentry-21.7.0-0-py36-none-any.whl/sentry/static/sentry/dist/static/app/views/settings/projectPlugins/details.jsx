Object.defineProperty(exports, "__esModule", { value: true });
exports.ProjectPluginDetails = void 0;
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var plugins_1 = require("app/actionCreators/plugins");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var pluginConfig_1 = tslib_1.__importDefault(require("app/components/pluginConfig"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var integrationUtil_1 = require("app/utils/integrationUtil");
var withPlugins_1 = tslib_1.__importDefault(require("app/utils/withPlugins"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
/**
 * There are currently two sources of truths for plugin details:
 *
 * 1) PluginsStore has a list of plugins, and this is where ENABLED state lives
 * 2) We fetch "plugin details" via API and save it to local state as `pluginDetails`.
 *    This is because "details" call contains form `config` and the "list" endpoint does not.
 *    The more correct way would be to pass `config` to PluginConfig and use plugin from
 *    PluginsStore
 */
var ProjectPluginDetails = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectPluginDetails, _super);
    function ProjectPluginDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleReset = function () {
            var _a = _this.props.params, projectId = _a.projectId, orgId = _a.orgId, pluginId = _a.pluginId;
            indicator_1.addLoadingMessage(locale_1.t('Saving changes\u2026'));
            integrationUtil_1.trackIntegrationEvent('integrations.uninstall_clicked', {
                integration: pluginId,
                integration_type: 'plugin',
                view: 'plugin_details',
            }, _this.props.organization);
            _this.api.request("/projects/" + orgId + "/" + projectId + "/plugins/" + pluginId + "/", {
                method: 'POST',
                data: { reset: true },
                success: function (pluginDetails) {
                    _this.setState({ pluginDetails: pluginDetails });
                    indicator_1.addSuccessMessage(locale_1.t('Plugin was reset'));
                    integrationUtil_1.trackIntegrationEvent('integrations.uninstall_completed', {
                        integration: pluginId,
                        integration_type: 'plugin',
                        view: 'plugin_details',
                    }, _this.props.organization);
                },
                error: function () {
                    indicator_1.addErrorMessage(locale_1.t('An error occurred'));
                },
            });
        };
        _this.handleEnable = function () {
            plugins_1.enablePlugin(_this.props.params);
            _this.analyticsChangeEnableStatus(true);
        };
        _this.handleDisable = function () {
            plugins_1.disablePlugin(_this.props.params);
            _this.analyticsChangeEnableStatus(false);
        };
        _this.analyticsChangeEnableStatus = function (enabled) {
            var pluginId = _this.props.params.pluginId;
            var eventKey = enabled ? 'integrations.enabled' : 'integrations.disabled';
            integrationUtil_1.trackIntegrationEvent(eventKey, {
                integration: pluginId,
                integration_type: 'plugin',
                view: 'plugin_details',
            }, _this.props.organization);
        };
        return _this;
    }
    ProjectPluginDetails.prototype.componentDidUpdate = function (prevProps, prevContext) {
        _super.prototype.componentDidUpdate.call(this, prevProps, prevContext);
        if (prevProps.params.pluginId !== this.props.params.pluginId) {
            this.recordDetailsViewed();
        }
    };
    ProjectPluginDetails.prototype.componentDidMount = function () {
        this.recordDetailsViewed();
    };
    ProjectPluginDetails.prototype.recordDetailsViewed = function () {
        var pluginId = this.props.params.pluginId;
        integrationUtil_1.trackIntegrationEvent('integrations.details_viewed', {
            integration: pluginId,
            integration_type: 'plugin',
            view: 'plugin_details',
        }, this.props.organization);
    };
    ProjectPluginDetails.prototype.getTitle = function () {
        var plugin = this.state.plugin;
        if (plugin && plugin.name) {
            return plugin.name;
        }
        else {
            return 'Sentry';
        }
    };
    ProjectPluginDetails.prototype.getEndpoints = function () {
        var _a = this.props.params, projectId = _a.projectId, orgId = _a.orgId, pluginId = _a.pluginId;
        return [['pluginDetails', "/projects/" + orgId + "/" + projectId + "/plugins/" + pluginId + "/"]];
    };
    ProjectPluginDetails.prototype.trimSchema = function (value) {
        return value.split('//')[1];
    };
    // Enabled state is handled via PluginsStore and not via plugins detail
    ProjectPluginDetails.prototype.getEnabled = function () {
        var _this = this;
        var pluginDetails = this.state.pluginDetails;
        var plugins = this.props.plugins;
        var plugin = plugins &&
            plugins.plugins &&
            plugins.plugins.find(function (_a) {
                var slug = _a.slug;
                return slug === _this.props.params.pluginId;
            });
        return plugin ? plugin.enabled : pluginDetails && pluginDetails.enabled;
    };
    ProjectPluginDetails.prototype.renderActions = function () {
        var pluginDetails = this.state.pluginDetails;
        if (!pluginDetails) {
            return null;
        }
        var enabled = this.getEnabled();
        var enable = (<StyledButton size="small" onClick={this.handleEnable}>
        {locale_1.t('Enable Plugin')}
      </StyledButton>);
        var disable = (<StyledButton size="small" priority="danger" onClick={this.handleDisable}>
        {locale_1.t('Disable Plugin')}
      </StyledButton>);
        var toggleEnable = enabled ? disable : enable;
        return (<div className="pull-right">
        {pluginDetails.canDisable && toggleEnable}
        <button_1.default size="small" onClick={this.handleReset}>
          {locale_1.t('Reset Configuration')}
        </button_1.default>
      </div>);
    };
    ProjectPluginDetails.prototype.renderBody = function () {
        var _a, _b;
        var _c = this.props, organization = _c.organization, project = _c.project;
        var pluginDetails = this.state.pluginDetails;
        if (!pluginDetails) {
            return null;
        }
        return (<div>
        <settingsPageHeader_1.default title={pluginDetails.name} action={this.renderActions()}/>
        <div className="row">
          <div className="col-md-7">
            <pluginConfig_1.default organization={organization} project={project} data={pluginDetails} enabled={this.getEnabled()} onDisablePlugin={this.handleDisable}/>
          </div>
          <div className="col-md-4 col-md-offset-1">
            <div className="pluginDetails-meta">
              <h4>{locale_1.t('Plugin Information')}</h4>

              <dl className="flat">
                <dt>{locale_1.t('Name')}</dt>
                <dd>{pluginDetails.name}</dd>
                <dt>{locale_1.t('Author')}</dt>
                <dd>{(_a = pluginDetails.author) === null || _a === void 0 ? void 0 : _a.name}</dd>
                {((_b = pluginDetails.author) === null || _b === void 0 ? void 0 : _b.url) && (<div>
                    <dt>{locale_1.t('URL')}</dt>
                    <dd>
                      <externalLink_1.default href={pluginDetails.author.url}>
                        {this.trimSchema(pluginDetails.author.url)}
                      </externalLink_1.default>
                    </dd>
                  </div>)}
                <dt>{locale_1.t('Version')}</dt>
                <dd>{pluginDetails.version}</dd>
              </dl>

              {pluginDetails.description && (<div>
                  <h4>{locale_1.t('Description')}</h4>
                  <p className="description">{pluginDetails.description}</p>
                </div>)}

              {pluginDetails.resourceLinks && (<div>
                  <h4>{locale_1.t('Resources')}</h4>
                  <dl className="flat">
                    {pluginDetails.resourceLinks.map(function (_a) {
                    var title = _a.title, url = _a.url;
                    return (<dd key={url}>
                        <externalLink_1.default href={url}>{title}</externalLink_1.default>
                      </dd>);
                })}
                  </dl>
                </div>)}
            </div>
          </div>
        </div>
      </div>);
    };
    return ProjectPluginDetails;
}(asyncView_1.default));
exports.ProjectPluginDetails = ProjectPluginDetails;
exports.default = withPlugins_1.default(ProjectPluginDetails);
var StyledButton = styled_1.default(button_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(0.75));
var templateObject_1;
//# sourceMappingURL=details.jsx.map