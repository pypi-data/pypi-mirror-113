Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var Heading = styled_1.default('h5')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin-bottom: ", ";\n  font-size: ", ";\n\n  &:after {\n    flex: 1;\n    display: block;\n    content: '';\n    border-top: 1px solid ", ";\n    margin-left: ", ";\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  margin-bottom: ", ";\n  font-size: ", ";\n\n  &:after {\n    flex: 1;\n    display: block;\n    content: '';\n    border-top: 1px solid ", ";\n    margin-left: ", ";\n  }\n"])), space_1.default(2), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.innerBorder; }, space_1.default(1));
var Subheading = styled_1.default('h6')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  display: flex;\n  font-size: ", ";\n  text-transform: uppercase;\n  justify-content: space-between;\n  margin-bottom: ", ";\n"], ["\n  color: ", ";\n  display: flex;\n  font-size: ", ";\n  text-transform: uppercase;\n  justify-content: space-between;\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeExtraSmall; }, space_1.default(1));
/**
 * Used to add a new section in Issue Details' sidebar.
 */
function SidebarSection(_a) {
    var title = _a.title, children = _a.children, secondary = _a.secondary, props = tslib_1.__rest(_a, ["title", "children", "secondary"]);
    var HeaderComponent = secondary ? Subheading : Heading;
    return (<React.Fragment>
      <HeaderComponent {...props}>{title}</HeaderComponent>
      <SectionContent secondary={secondary}>{children}</SectionContent>
    </React.Fragment>);
}
var SectionContent = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), function (p) { return (p.secondary ? space_1.default(2) : space_1.default(3)); });
exports.default = SidebarSection;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=sidebarSection.jsx.map