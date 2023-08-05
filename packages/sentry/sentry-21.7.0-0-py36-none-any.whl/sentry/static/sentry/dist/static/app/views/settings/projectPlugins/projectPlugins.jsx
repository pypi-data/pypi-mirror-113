Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var React = tslib_1.__importStar(require("react"));
var access_1 = tslib_1.__importDefault(require("app/components/acl/access"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var routeError_1 = tslib_1.__importDefault(require("app/views/routeError"));
var projectPluginRow_1 = tslib_1.__importDefault(require("./projectPluginRow"));
var ProjectPlugins = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectPlugins, _super);
    function ProjectPlugins() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ProjectPlugins.prototype.render = function () {
        var _a = this.props, plugins = _a.plugins, loading = _a.loading, error = _a.error, onChange = _a.onChange, routes = _a.routes, params = _a.params, project = _a.project;
        var orgId = this.props.params.orgId;
        var hasError = error;
        var isLoading = !hasError && loading;
        if (hasError) {
            return <routeError_1.default error={error}/>;
        }
        if (isLoading) {
            return <loadingIndicator_1.default />;
        }
        return (<panels_1.Panel>
        <panels_1.PanelHeader>
          <div>{locale_1.t('Legacy Integration')}</div>
          <div>{locale_1.t('Enabled')}</div>
        </panels_1.PanelHeader>
        <panels_1.PanelBody>
          <panels_1.PanelAlert type="warning">
            <access_1.default access={['org:integrations']}>
              {function (_a) {
                var hasAccess = _a.hasAccess;
                return hasAccess
                    ? locale_1.tct("Legacy Integrations must be configured per-project. It's recommended to prefer organization integrations over the legacy project integrations when available. Visit the [link:organization integrations] settings to manage them.", {
                        link: <link_1.default to={"/settings/" + orgId + "/integrations"}/>,
                    })
                    : locale_1.t("Legacy Integrations must be configured per-project. It's recommended to prefer organization integrations over the legacy project integrations when available.");
            }}
            </access_1.default>
          </panels_1.PanelAlert>

          {plugins
                .filter(function (p) {
                return !p.isHidden;
            })
                .map(function (plugin) { return (<panels_1.PanelItem key={plugin.id}>
                <projectPluginRow_1.default params={params} routes={routes} project={project} {...plugin} onChange={onChange}/>
              </panels_1.PanelItem>); })}
        </panels_1.PanelBody>
      </panels_1.Panel>);
    };
    return ProjectPlugins;
}(react_1.Component));
exports.default = ProjectPlugins;
//# sourceMappingURL=projectPlugins.jsx.map