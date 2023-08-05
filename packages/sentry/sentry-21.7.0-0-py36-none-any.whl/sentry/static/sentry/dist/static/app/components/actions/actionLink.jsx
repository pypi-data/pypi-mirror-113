Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var classnames_1 = tslib_1.__importDefault(require("classnames"));
var button_1 = tslib_1.__importDefault(require("./button"));
var confirmableAction_1 = tslib_1.__importDefault(require("./confirmableAction"));
var StyledAction = styled_1.default('a')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  ", "\n"], ["\n  display: flex;\n  align-items: center;\n  ", "\n"])), function (p) { return p.disabled && 'cursor: not-allowed;'; });
var StyledActionButton = styled_1.default(button_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  ", "\n"], ["\n  display: flex;\n  align-items: center;\n  ", "\n"])), function (p) { return p.disabled && 'cursor: not-allowed;'; });
function ActionLink(_a) {
    var _b;
    var message = _a.message, className = _a.className, title = _a.title, onAction = _a.onAction, type = _a.type, confirmLabel = _a.confirmLabel, disabled = _a.disabled, children = _a.children, shouldConfirm = _a.shouldConfirm, confirmPriority = _a.confirmPriority, header = _a.header, props = tslib_1.__rest(_a, ["message", "className", "title", "onAction", "type", "confirmLabel", "disabled", "children", "shouldConfirm", "confirmPriority", "header"]);
    var actionCommonProps = tslib_1.__assign((_b = {}, _b['aria-label'] = title, _b.className = classnames_1.default(className, { disabled: disabled }), _b.onClick = disabled ? undefined : onAction, _b.disabled = disabled, _b.children = children, _b), props);
    var action = type === 'button' ? (<StyledActionButton {...actionCommonProps}/>) : (<StyledAction {...actionCommonProps}/>);
    if (shouldConfirm && onAction) {
        return (<confirmableAction_1.default shouldConfirm={shouldConfirm} priority={confirmPriority} disabled={disabled} message={message} header={header} confirmText={confirmLabel} onConfirm={onAction} stopPropagation={disabled}>
        {action}
      </confirmableAction_1.default>);
    }
    return action;
}
exports.default = ActionLink;
var templateObject_1, templateObject_2;
//# sourceMappingURL=actionLink.jsx.map