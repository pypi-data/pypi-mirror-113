Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var panels_1 = require("app/components/panels");
var textOverflow_1 = tslib_1.__importDefault(require("app/components/textOverflow"));
var locale_1 = require("app/locale");
var pluginIcon_1 = tslib_1.__importDefault(require("app/plugins/components/pluginIcon"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var InactivePlugins = function (_a) {
    var plugins = _a.plugins, onEnablePlugin = _a.onEnablePlugin;
    if (plugins.length === 0) {
        return null;
    }
    return (<panels_1.Panel>
      <panels_1.PanelHeader>{locale_1.t('Inactive Integrations')}</panels_1.PanelHeader>

      <panels_1.PanelBody>
        <Plugins>
          {plugins.map(function (plugin) { return (<IntegrationButton key={plugin.id} onClick={function () { return onEnablePlugin(plugin); }} className={"ref-plugin-enable-" + plugin.id}>
              <Label>
                <StyledPluginIcon pluginId={plugin.id}/>
                <textOverflow_1.default>{plugin.shortName || plugin.name}</textOverflow_1.default>
              </Label>
            </IntegrationButton>); })}
        </Plugins>
      </panels_1.PanelBody>
    </panels_1.Panel>);
};
var Plugins = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  padding: ", ";\n  flex: 1;\n  flex-wrap: wrap;\n"], ["\n  display: flex;\n  padding: ", ";\n  flex: 1;\n  flex-wrap: wrap;\n"])), space_1.default(1));
var IntegrationButton = styled_1.default('button')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin: ", ";\n  width: 175px;\n  text-align: center;\n  font-size: ", ";\n  color: #889ab0;\n  letter-spacing: 0.1px;\n  font-weight: 600;\n  text-transform: uppercase;\n  border: 1px solid #eee;\n  background: inherit;\n  border-radius: ", ";\n  padding: 10px;\n\n  &:hover {\n    border-color: #ccc;\n  }\n"], ["\n  margin: ", ";\n  width: 175px;\n  text-align: center;\n  font-size: ", ";\n  color: #889ab0;\n  letter-spacing: 0.1px;\n  font-weight: 600;\n  text-transform: uppercase;\n  border: 1px solid #eee;\n  background: inherit;\n  border-radius: ", ";\n  padding: 10px;\n\n  &:hover {\n    border-color: #ccc;\n  }\n"])), space_1.default(1), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.borderRadius; });
var Label = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"])));
var StyledPluginIcon = styled_1.default(pluginIcon_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(1));
exports.default = InactivePlugins;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=inactivePlugins.jsx.map