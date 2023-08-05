Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var clippedBox_1 = tslib_1.__importDefault(require("app/components/clippedBox"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var panels_1 = require("app/components/panels");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var recreateRoute_1 = tslib_1.__importDefault(require("app/utils/recreateRoute"));
var projectKeyCredentials_1 = tslib_1.__importDefault(require("app/views/settings/project/projectKeys/projectKeyCredentials"));
var KeyRow = /** @class */ (function (_super) {
    tslib_1.__extends(KeyRow, _super);
    function KeyRow() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleRemove = function () {
            var _a = _this.props, data = _a.data, onRemove = _a.onRemove;
            onRemove(data);
        };
        _this.handleEnable = function () {
            var _a = _this.props, onToggle = _a.onToggle, data = _a.data;
            onToggle(true, data);
        };
        _this.handleDisable = function () {
            var _a = _this.props, onToggle = _a.onToggle, data = _a.data;
            onToggle(false, data);
        };
        return _this;
    }
    KeyRow.prototype.render = function () {
        var _a = this.props, access = _a.access, data = _a.data, routes = _a.routes, location = _a.location, params = _a.params;
        var editUrl = recreateRoute_1.default(data.id + "/", { routes: routes, params: params, location: location });
        var controlActive = access.has('project:write');
        var controls = [
            <button_1.default key="edit" to={editUrl} size="small">
        {locale_1.t('Configure')}
      </button_1.default>,
            <button_1.default key="toggle" size="small" onClick={data.isActive ? this.handleDisable : this.handleEnable} disabled={!controlActive}>
        {data.isActive ? locale_1.t('Disable') : locale_1.t('Enable')}
      </button_1.default>,
            <confirm_1.default key="remove" priority="danger" disabled={!controlActive} onConfirm={this.handleRemove} confirmText={locale_1.t('Remove Key')} message={locale_1.t('Are you sure you want to remove this key? This action is irreversible.')}>
        <button_1.default size="small" disabled={!controlActive} icon={<icons_1.IconDelete />}/>
      </confirm_1.default>,
        ];
        return (<panels_1.Panel>
        <panels_1.PanelHeader hasButtons>
          <Title disabled={!data.isActive}>
            <PanelHeaderLink to={editUrl}>{data.label}</PanelHeaderLink>
            {!data.isActive && (<small>
                {' \u2014  '}
                {locale_1.t('Disabled')}
              </small>)}
          </Title>
          <Controls>
            {controls.map(function (c, n) { return (<span key={n}> {c}</span>); })}
          </Controls>
        </panels_1.PanelHeader>

        <StyledClippedBox clipHeight={300} defaultClipped btnText={locale_1.t('Expand')}>
          <StyledPanelBody disabled={!data.isActive}>
            <projectKeyCredentials_1.default projectId={"" + data.projectId} data={data}/>
          </StyledPanelBody>
        </StyledClippedBox>
      </panels_1.Panel>);
    };
    return KeyRow;
}(react_1.Component));
exports.default = KeyRow;
var StyledClippedBox = styled_1.default(clippedBox_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: 0;\n  margin: 0;\n  > *:last-child {\n    padding-bottom: ", ";\n  }\n"], ["\n  padding: 0;\n  margin: 0;\n  > *:last-child {\n    padding-bottom: ", ";\n  }\n"])), space_1.default(3));
var PanelHeaderLink = styled_1.default(react_router_1.Link)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.subText; });
var Title = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n  ", ";\n  margin-right: ", ";\n"], ["\n  flex: 1;\n  ", ";\n  margin-right: ", ";\n"])), function (p) { return (p.disabled ? 'opacity: 0.5;' : ''); }, space_1.default(1));
var Controls = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  align-items: center;\n  grid-gap: ", ";\n  grid-auto-flow: column;\n"], ["\n  display: grid;\n  align-items: center;\n  grid-gap: ", ";\n  grid-auto-flow: column;\n"])), space_1.default(1));
var StyledPanelBody = styled_1.default(panels_1.PanelBody)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), function (p) { return (p.disabled ? 'opacity: 0.5;' : ''); });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=keyRow.jsx.map