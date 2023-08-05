Object.defineProperty(exports, "__esModule", { value: true });
exports.menuItemStyles = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var sidebarMenuItemLink_1 = tslib_1.__importDefault(require("./sidebarMenuItemLink"));
var sidebarOrgSummary_1 = require("./sidebarOrgSummary");
var SidebarMenuItem = function (_a) {
    var to = _a.to, children = _a.children, href = _a.href, props = tslib_1.__rest(_a, ["to", "children", "href"]);
    var hasMenu = !to && !href;
    return (<StyledSidebarMenuItemLink to={to} href={href} {...props}>
      <MenuItemLabel hasMenu={hasMenu}>{children}</MenuItemLabel>
    </StyledSidebarMenuItemLink>);
};
var menuItemStyles = function (p) { return react_1.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  cursor: pointer;\n  display: flex;\n  font-size: ", ";\n  line-height: 32px;\n  padding: 0 ", ";\n  position: relative;\n  transition: 0.1s all linear;\n  ", ";\n\n  &:hover,\n  &:active,\n  &.focus-visible {\n    background: ", ";\n    color: ", ";\n    outline: none;\n  }\n\n  ", " {\n    padding-left: 0;\n    padding-right: 0;\n  }\n"], ["\n  color: ", ";\n  cursor: pointer;\n  display: flex;\n  font-size: ", ";\n  line-height: 32px;\n  padding: 0 ", ";\n  position: relative;\n  transition: 0.1s all linear;\n  ", ";\n\n  &:hover,\n  &:active,\n  &.focus-visible {\n    background: ", ";\n    color: ", ";\n    outline: none;\n  }\n\n  ", " {\n    padding-left: 0;\n    padding-right: 0;\n  }\n"])), p.theme.textColor, p.theme.fontSizeMedium, p.theme.sidebar.menuSpacing, (!!p.to || !!p.href) && 'overflow: hidden', p.theme.backgroundSecondary, p.theme.textColor, sidebarOrgSummary_1.OrgSummary); };
exports.menuItemStyles = menuItemStyles;
var MenuItemLabel = styled_1.default('span')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n  ", ";\n"], ["\n  flex: 1;\n  ", ";\n"])), function (p) {
    return p.hasMenu
        ? react_1.css(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n          margin: 0 -15px;\n          padding: 0 15px;\n        "], ["\n          margin: 0 -15px;\n          padding: 0 15px;\n        "]))) : react_1.css(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n          overflow: hidden;\n        "], ["\n          overflow: hidden;\n        "])));
});
var StyledSidebarMenuItemLink = styled_1.default(sidebarMenuItemLink_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), menuItemStyles);
exports.default = SidebarMenuItem;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=sidebarMenuItem.jsx.map