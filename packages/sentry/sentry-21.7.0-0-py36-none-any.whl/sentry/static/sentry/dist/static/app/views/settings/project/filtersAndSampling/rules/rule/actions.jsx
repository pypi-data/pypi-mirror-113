Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var menuItemActionLink_1 = tslib_1.__importDefault(require("app/components/actions/menuItemActionLink"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var dropdownLink_1 = tslib_1.__importDefault(require("app/components/dropdownLink"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var deleteRuleConfirmMessage = locale_1.t('Are you sure you wish to delete this dynamic sampling rule?');
var deleteRuleMessage = locale_1.t('You do not have permission to delete dynamic sampling rules.');
var editRuleMessage = locale_1.t('You do not have permission to edit dynamic sampling rules.');
function Actions(_a) {
    var disabled = _a.disabled, onEditRule = _a.onEditRule, onDeleteRule = _a.onDeleteRule, onOpenMenuActions = _a.onOpenMenuActions, isMenuActionsOpen = _a.isMenuActionsOpen;
    return (<react_1.Fragment>
      <StyledButtonbar gap={1}>
        <button_1.default label={locale_1.t('Edit Rule')} size="small" onClick={onEditRule} icon={<icons_1.IconEdit />} disabled={disabled} title={disabled ? editRuleMessage : undefined}/>
        <confirm_1.default priority="danger" message={deleteRuleConfirmMessage} onConfirm={onDeleteRule} disabled={disabled}>
          <button_1.default label={locale_1.t('Delete Rule')} size="small" icon={<icons_1.IconDelete />} title={disabled ? deleteRuleMessage : undefined}/>
        </confirm_1.default>
      </StyledButtonbar>
      <StyledDropdownLink caret={false} customTitle={<button_1.default label={locale_1.t('Actions')} icon={<icons_1.IconEllipsis size="sm"/>} size="xsmall" onClick={onOpenMenuActions}/>} isOpen={isMenuActionsOpen} anchorRight>
        <menuItemActionLink_1.default shouldConfirm={false} icon={<icons_1.IconDownload size="xs"/>} title={locale_1.t('Edit')} onClick={!disabled
            ? onEditRule
            : function (event) {
                event === null || event === void 0 ? void 0 : event.stopPropagation();
            }} disabled={disabled}>
          <tooltip_1.default disabled={!disabled} title={editRuleMessage} containerDisplayMode="block">
            {locale_1.t('Edit')}
          </tooltip_1.default>
        </menuItemActionLink_1.default>
        <menuItemActionLink_1.default onAction={onDeleteRule} message={deleteRuleConfirmMessage} icon={<icons_1.IconDownload size="xs"/>} title={locale_1.t('Delete')} disabled={disabled} priority="danger" shouldConfirm>
          <tooltip_1.default disabled={!disabled} title={deleteRuleMessage} containerDisplayMode="block">
            {locale_1.t('Delete')}
          </tooltip_1.default>
        </menuItemActionLink_1.default>
      </StyledDropdownLink>
    </react_1.Fragment>);
}
exports.default = Actions;
var StyledButtonbar = styled_1.default(buttonBar_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  justify-content: flex-end;\n  flex: 1;\n  display: none;\n  @media (min-width: ", ") {\n    display: grid;\n  }\n"], ["\n  justify-content: flex-end;\n  flex: 1;\n  display: none;\n  @media (min-width: ", ") {\n    display: grid;\n  }\n"])), function (p) { return p.theme.breakpoints[2]; });
var StyledDropdownLink = styled_1.default(dropdownLink_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  transition: none;\n  @media (min-width: ", ") {\n    display: none;\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  transition: none;\n  @media (min-width: ", ") {\n    display: none;\n  }\n"])), function (p) { return p.theme.breakpoints[2]; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=actions.jsx.map