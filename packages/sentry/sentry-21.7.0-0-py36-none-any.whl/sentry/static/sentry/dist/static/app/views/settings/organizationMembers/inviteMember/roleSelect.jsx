Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var panels_1 = require("app/components/panels");
var radio_1 = tslib_1.__importDefault(require("app/components/radio"));
var locale_1 = require("app/locale");
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
var Label = styled_1.default('label')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  align-items: center;\n  margin-bottom: 0;\n"], ["\n  display: flex;\n  flex: 1;\n  align-items: center;\n  margin-bottom: 0;\n"])));
var RoleSelect = /** @class */ (function (_super) {
    tslib_1.__extends(RoleSelect, _super);
    function RoleSelect() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    RoleSelect.prototype.render = function () {
        var _this = this;
        var _a = this.props, disabled = _a.disabled, enforceAllowed = _a.enforceAllowed, roleList = _a.roleList, selectedRole = _a.selectedRole;
        return (<panels_1.Panel>
        <panels_1.PanelHeader>{locale_1.t('Role')}</panels_1.PanelHeader>

        <panels_1.PanelBody>
          {roleList.map(function (role) {
                var desc = role.desc, name = role.name, id = role.id, allowed = role.allowed;
                var isDisabled = disabled || (enforceAllowed && !allowed);
                return (<panels_1.PanelItem key={id} onClick={function () { return !isDisabled && _this.props.setRole(id); }} css={!isDisabled ? {} : { color: 'grey', cursor: 'default' }}>
                <Label>
                  <radio_1.default id={id} value={name} checked={id === selectedRole} readOnly/>
                  <div style={{ flex: 1, padding: '0 16px' }}>
                    {name}
                    <textBlock_1.default noMargin>
                      <div className="help-block">{desc}</div>
                    </textBlock_1.default>
                  </div>
                </Label>
              </panels_1.PanelItem>);
            })}
        </panels_1.PanelBody>
      </panels_1.Panel>);
    };
    return RoleSelect;
}(react_1.Component));
exports.default = RoleSelect;
var templateObject_1;
//# sourceMappingURL=roleSelect.jsx.map