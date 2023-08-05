Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var capitalize_1 = tslib_1.__importDefault(require("lodash/capitalize"));
var access_1 = tslib_1.__importDefault(require("app/components/acl/access"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var panels_1 = require("app/components/panels");
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var integrationUtil_1 = require("app/utils/integrationUtil");
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var IntegrationExternalMappings = /** @class */ (function (_super) {
    tslib_1.__extends(IntegrationExternalMappings, _super);
    function IntegrationExternalMappings() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    IntegrationExternalMappings.prototype.render = function () {
        var _a = this.props, integration = _a.integration, mappings = _a.mappings, type = _a.type, onCreateOrEdit = _a.onCreateOrEdit, onDelete = _a.onDelete;
        return (<react_1.Fragment>
        <panels_1.Panel>
          <panels_1.PanelHeader disablePadding hasButtons>
            <HeaderLayout>
              <ExternalNameColumn>{locale_1.tct('External [type]', { type: type })}</ExternalNameColumn>
              <SentryNameColumn>{locale_1.tct('Sentry [type]', { type: type })}</SentryNameColumn>
              <ButtonColumn>
                <AddButton data-test-id="add-mapping-button" onClick={function () { return onCreateOrEdit(); }} size="xsmall" icon={<icons_1.IconAdd size="xs" isCircled/>}>
                  {locale_1.tct('Add [type] Mapping', { type: type })}
                </AddButton>
              </ButtonColumn>
            </HeaderLayout>
          </panels_1.PanelHeader>
          <panels_1.PanelBody>
            {!mappings.length && (<emptyMessage_1.default icon={integrationUtil_1.getIntegrationIcon(integration.provider.key, 'lg')}>
                {locale_1.tct('Set up External [type] Mappings.', { type: capitalize_1.default(type) })}
              </emptyMessage_1.default>)}
            {mappings.map(function (item) { return (<access_1.default access={['org:integrations']} key={item.id}>
                {function (_a) {
                    var hasAccess = _a.hasAccess;
                    return (<ConfigPanelItem>
                    <Layout>
                      <ExternalNameColumn>{item.externalName}</ExternalNameColumn>
                      <SentryNameColumn>{item.sentryName}</SentryNameColumn>
                      <ButtonColumn>
                        <tooltip_1.default title={locale_1.t('You must be an organization owner, manager or admin to edit or remove an external user mapping.')} disabled={hasAccess}>
                          <StyledButton size="small" icon={<icons_1.IconEdit size="sm"/>} label={locale_1.t('edit')} disabled={!hasAccess} onClick={function () { return onCreateOrEdit(item); }}/>
                          <confirm_1.default disabled={!hasAccess} onConfirm={function () { return onDelete(item); }} message={locale_1.t('Are you sure you want to remove this external user mapping?')}>
                            <StyledButton size="small" icon={<icons_1.IconDelete size="sm"/>} label={locale_1.t('delete')} disabled={!hasAccess}/>
                          </confirm_1.default>
                        </tooltip_1.default>
                      </ButtonColumn>
                    </Layout>
                  </ConfigPanelItem>);
                }}
              </access_1.default>); })}
          </panels_1.PanelBody>
        </panels_1.Panel>
      </react_1.Fragment>);
    };
    return IntegrationExternalMappings;
}(react_1.Component));
exports.default = IntegrationExternalMappings;
var AddButton = styled_1.default(button_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  text-transform: capitalize;\n"], ["\n  text-transform: capitalize;\n"])));
var Layout = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-column-gap: ", ";\n  width: 100%;\n  align-items: center;\n  grid-template-columns: 2.5fr 2.5fr 1fr;\n  grid-template-areas: 'external-name sentry-name button';\n"], ["\n  display: grid;\n  grid-column-gap: ", ";\n  width: 100%;\n  align-items: center;\n  grid-template-columns: 2.5fr 2.5fr 1fr;\n  grid-template-areas: 'external-name sentry-name button';\n"])), space_1.default(1));
var HeaderLayout = styled_1.default(Layout)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  align-items: center;\n  margin: 0;\n  margin-left: ", ";\n  text-transform: uppercase;\n"], ["\n  align-items: center;\n  margin: 0;\n  margin-left: ", ";\n  text-transform: uppercase;\n"])), space_1.default(2));
var ConfigPanelItem = styled_1.default(panels_1.PanelItem)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject([""], [""])));
var StyledButton = styled_1.default(button_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  margin: ", ";\n"], ["\n  margin: ", ";\n"])), space_1.default(0.5));
// Columns below
var Column = styled_1.default('span')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  overflow: hidden;\n  overflow-wrap: break-word;\n"], ["\n  overflow: hidden;\n  overflow-wrap: break-word;\n"])));
var ExternalNameColumn = styled_1.default(Column)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  grid-area: external-name;\n"], ["\n  grid-area: external-name;\n"])));
var SentryNameColumn = styled_1.default(Column)(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  grid-area: sentry-name;\n"], ["\n  grid-area: sentry-name;\n"])));
var ButtonColumn = styled_1.default(Column)(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  grid-area: button;\n  text-align: right;\n"], ["\n  grid-area: button;\n  text-align: right;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=integrationExternalMappings.jsx.map