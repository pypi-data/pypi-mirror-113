Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var plugins_1 = require("app/actionCreators/plugins");
var sentryDocumentTitle_1 = tslib_1.__importDefault(require("app/components/sentryDocumentTitle"));
var locale_1 = require("app/locale");
var integrationUtil_1 = require("app/utils/integrationUtil");
var withPlugins_1 = tslib_1.__importDefault(require("app/utils/withPlugins"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var permissionAlert_1 = tslib_1.__importDefault(require("app/views/settings/project/permissionAlert"));
var projectPlugins_1 = tslib_1.__importDefault(require("./projectPlugins"));
var ProjectPluginsContainer = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectPluginsContainer, _super);
    function ProjectPluginsContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.fetchData = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var plugins, installCount;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, plugins_1.fetchPlugins(this.props.params)];
                    case 1:
                        plugins = _a.sent();
                        installCount = plugins.filter(function (plugin) { return plugin.hasConfiguration && plugin.enabled; }).length;
                        integrationUtil_1.trackIntegrationEvent('integrations.index_viewed', {
                            integrations_installed: installCount,
                            view: 'legacy_integrations',
                        }, this.props.organization, { startSession: true });
                        return [2 /*return*/];
                }
            });
        }); };
        _this.handleChange = function (pluginId, shouldEnable) {
            var _a = _this.props.params, projectId = _a.projectId, orgId = _a.orgId;
            var actionCreator = shouldEnable ? plugins_1.enablePlugin : plugins_1.disablePlugin;
            actionCreator({ projectId: projectId, orgId: orgId, pluginId: pluginId });
        };
        return _this;
    }
    ProjectPluginsContainer.prototype.componentDidMount = function () {
        this.fetchData();
    };
    ProjectPluginsContainer.prototype.render = function () {
        var _a = this.props.plugins || {}, loading = _a.loading, error = _a.error, plugins = _a.plugins;
        var orgId = this.props.params.orgId;
        var title = locale_1.t('Legacy Integrations');
        return (<React.Fragment>
        <sentryDocumentTitle_1.default title={title} orgSlug={orgId}/>
        <settingsPageHeader_1.default title={title}/>
        <permissionAlert_1.default />

        <projectPlugins_1.default {...this.props} onChange={this.handleChange} loading={loading} error={error} plugins={plugins}/>
      </React.Fragment>);
    };
    return ProjectPluginsContainer;
}(React.Component));
exports.default = withPlugins_1.default(ProjectPluginsContainer);
//# sourceMappingURL=index.jsx.map