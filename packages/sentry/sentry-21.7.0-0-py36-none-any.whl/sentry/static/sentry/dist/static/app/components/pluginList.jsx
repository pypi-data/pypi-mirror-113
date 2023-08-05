Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var plugins_1 = require("app/actionCreators/plugins");
var inactivePlugins_1 = tslib_1.__importDefault(require("app/components/inactivePlugins"));
var pluginConfig_1 = tslib_1.__importDefault(require("app/components/pluginConfig"));
var locale_1 = require("app/locale");
var panels_1 = require("./panels");
var PluginList = function (_a) {
    var organization = _a.organization, project = _a.project, pluginList = _a.pluginList, _b = _a.onDisablePlugin, onDisablePlugin = _b === void 0 ? function () { } : _b, _c = _a.onEnablePlugin, onEnablePlugin = _c === void 0 ? function () { } : _c;
    var handleEnablePlugin = function (plugin) {
        plugins_1.enablePlugin({
            projectId: project.slug,
            orgId: organization.slug,
            pluginId: plugin.slug,
        });
        onEnablePlugin(plugin);
    };
    var handleDisablePlugin = function (plugin) {
        plugins_1.disablePlugin({
            projectId: project.slug,
            orgId: organization.slug,
            pluginId: plugin.slug,
        });
        onDisablePlugin(plugin);
    };
    if (!pluginList.length) {
        return (<panels_1.Panel>
        <panels_1.PanelItem>
          {locale_1.t("Oops! Looks like there aren't any available integrations installed.")}
        </panels_1.PanelItem>
      </panels_1.Panel>);
    }
    return (<div>
      {pluginList
            .filter(function (p) { return p.enabled; })
            .map(function (data) { return (<pluginConfig_1.default data={data} organization={organization} project={project} key={data.id} onDisablePlugin={handleDisablePlugin}/>); })}

      <inactivePlugins_1.default plugins={pluginList.filter(function (p) { return !p.enabled && !p.isHidden; })} onEnablePlugin={handleEnablePlugin}/>
    </div>);
};
exports.default = PluginList;
//# sourceMappingURL=pluginList.jsx.map