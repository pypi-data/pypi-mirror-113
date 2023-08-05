Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var react_2 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var access_1 = tslib_1.__importDefault(require("app/components/acl/access"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var switchButton_1 = tslib_1.__importDefault(require("app/components/switchButton"));
var locale_1 = require("app/locale");
var pluginIcon_1 = tslib_1.__importDefault(require("app/plugins/components/pluginIcon"));
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var integrationUtil_1 = require("app/utils/integrationUtil");
var recreateRoute_1 = tslib_1.__importDefault(require("app/utils/recreateRoute"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var grayText = react_2.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  color: #979ba0;\n"], ["\n  color: #979ba0;\n"])));
var ProjectPluginRow = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectPluginRow, _super);
    function ProjectPluginRow() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleChange = function () {
            var _a = _this.props, onChange = _a.onChange, id = _a.id, enabled = _a.enabled;
            onChange(id, !enabled);
            var eventKey = !enabled ? 'integrations.enabled' : 'integrations.disabled';
            integrationUtil_1.trackIntegrationEvent(eventKey, {
                integration: id,
                integration_type: 'plugin',
                view: 'legacy_integrations',
            }, _this.props.organization);
        };
        return _this;
    }
    ProjectPluginRow.prototype.render = function () {
        var _this = this;
        var _a = this.props, id = _a.id, name = _a.name, slug = _a.slug, version = _a.version, author = _a.author, hasConfiguration = _a.hasConfiguration, enabled = _a.enabled, canDisable = _a.canDisable;
        var configureUrl = recreateRoute_1.default(id, this.props);
        return (<access_1.default access={['project:write']}>
        {function (_a) {
                var hasAccess = _a.hasAccess;
                var LinkOrSpan = hasAccess ? react_router_1.Link : 'span';
                return (<PluginItem key={id} className={slug}>
              <PluginInfo>
                <StyledPluginIcon size={48} pluginId={id}/>
                <PluginDescription>
                  <PluginName>
                    {name + " "}
                    {getDynamicText_1.default({
                        value: (<Version>{version ? "v" + version : <em>{locale_1.t('n/a')}</em>}</Version>),
                        fixed: <Version>v10</Version>,
                    })}
                  </PluginName>
                  <div>
                    {author && (<externalLink_1.default css={grayText} href={author.url}>
                        {author.name}
                      </externalLink_1.default>)}
                    {hasConfiguration && (<span>
                        {' '}
                        &middot;{' '}
                        <LinkOrSpan css={grayText} to={configureUrl}>
                          {locale_1.t('Configure plugin')}
                        </LinkOrSpan>
                      </span>)}
                  </div>
                </PluginDescription>
              </PluginInfo>
              <switchButton_1.default size="lg" isDisabled={!hasAccess || !canDisable} isActive={enabled} toggle={_this.handleChange}/>
            </PluginItem>);
            }}
      </access_1.default>);
    };
    return ProjectPluginRow;
}(react_1.PureComponent));
exports.default = withOrganization_1.default(ProjectPluginRow);
var PluginItem = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  align-items: center;\n"], ["\n  display: flex;\n  flex: 1;\n  align-items: center;\n"])));
var PluginDescription = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: center;\n  flex-direction: column;\n"], ["\n  display: flex;\n  justify-content: center;\n  flex-direction: column;\n"])));
var PluginInfo = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  line-height: 24px;\n"], ["\n  display: flex;\n  flex: 1;\n  line-height: 24px;\n"])));
var PluginName = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  font-size: 16px;\n"], ["\n  font-size: 16px;\n"])));
var StyledPluginIcon = styled_1.default(pluginIcon_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  margin-right: 16px;\n"], ["\n  margin-right: 16px;\n"])));
// Keeping these colors the same from old integrations page
var Version = styled_1.default('span')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  color: #babec2;\n"], ["\n  color: #babec2;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=projectPluginRow.jsx.map