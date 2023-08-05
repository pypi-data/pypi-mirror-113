Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var classnames_1 = tslib_1.__importDefault(require("classnames"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var Item = function (_a) {
    var children = _a.children, icon = _a.icon, className = _a.className;
    return (<Wrapper className={classnames_1.default('context-item', className)}>
    {icon}
    {children && <Details>{children}</Details>}
  </Wrapper>);
};
exports.default = Item;
var Details = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n  max-width: 100%;\n  min-height: 48px;\n"], ["\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n  max-width: 100%;\n  min-height: 48px;\n"])));
var Wrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  border-top: 1px solid ", ";\n  padding: 4px 0 4px 40px;\n  display: flex;\n  margin-right: ", ";\n  align-items: center;\n  position: relative;\n  min-width: 0;\n\n  @media (min-width: ", ") {\n    max-width: 25%;\n    border: 0;\n    padding: 0px 0px 0px 42px;\n  }\n"], ["\n  border-top: 1px solid ", ";\n  padding: 4px 0 4px 40px;\n  display: flex;\n  margin-right: ", ";\n  align-items: center;\n  position: relative;\n  min-width: 0;\n\n  @media (min-width: ", ") {\n    max-width: 25%;\n    border: 0;\n    padding: 0px 0px 0px 42px;\n  }\n"])), function (p) { return p.theme.innerBorder; }, space_1.default(3), function (p) { return p.theme.breakpoints[0]; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=item.jsx.map