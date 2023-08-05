Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
var EmptyMessage = styled_1.default(function (_a) {
    var title = _a.title, description = _a.description, icon = _a.icon, children = _a.children, action = _a.action, _leftAligned = _a.leftAligned, props = tslib_1.__rest(_a, ["title", "description", "icon", "children", "action", "leftAligned"]);
    return (<div data-test-id="empty-message" {...props}>
      {icon && <IconWrapper>{icon}</IconWrapper>}
      {title && <Title noMargin={!description && !children && !action}>{title}</Title>}
      {description && <Description>{description}</Description>}
      {children && <Description noMargin>{children}</Description>}
      {action && <Action>{action}</Action>}
    </div>);
})(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  ", ";\n  flex-direction: column;\n  color: ", ";\n  font-size: ", ";\n"], ["\n  display: flex;\n  ", ";\n  flex-direction: column;\n  color: ", ";\n  font-size: ", ";\n"])), function (p) {
    return p.leftAligned
        ? react_1.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n          max-width: 70%;\n          align-items: flex-start;\n          padding: ", ";\n        "], ["\n          max-width: 70%;\n          align-items: flex-start;\n          padding: ", ";\n        "])), space_1.default(4)) : react_1.css(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n          text-align: center;\n          align-items: center;\n          padding: ", " 15%;\n        "], ["\n          text-align: center;\n          align-items: center;\n          padding: ", " 15%;\n        "])), space_1.default(4));
}, function (p) { return p.theme.textColor; }, function (p) {
    return p.size && p.size === 'large' ? p.theme.fontSizeExtraLarge : p.theme.fontSizeLarge;
});
var IconWrapper = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  margin-bottom: ", ";\n"], ["\n  color: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.gray200; }, space_1.default(1));
var Title = styled_1.default('strong')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  ", "\n"], ["\n  font-size: ", ";\n  ", "\n"])), function (p) { return p.theme.fontSizeExtraLarge; }, function (p) { return !p.noMargin && "margin-bottom: " + space_1.default(1) + ";"; });
var Description = styled_1.default(textBlock_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
var Action = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space_1.default(2));
exports.default = EmptyMessage;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=emptyMessage.jsx.map