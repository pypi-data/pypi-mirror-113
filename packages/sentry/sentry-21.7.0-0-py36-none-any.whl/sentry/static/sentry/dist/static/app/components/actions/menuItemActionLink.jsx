Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var actionLink_1 = tslib_1.__importDefault(require("app/components/actions/actionLink"));
var menuItem_1 = tslib_1.__importDefault(require("app/components/menuItem"));
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
function MenuItemActionLink(_a) {
    var className = _a.className, props = tslib_1.__rest(_a, ["className"]);
    return (<menuItem_1.default noAnchor withBorder disabled={props.disabled} className={className}>
      <InnerActionLink {...props}/>
    </menuItem_1.default>);
}
var InnerActionLink = styled_1.default(actionLink_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  ", "\n  &:hover {\n    color: ", ";\n  }\n\n  .dropdown-menu > li > &,\n  .dropdown-menu > span > li > & {\n    &.disabled:hover {\n      background: ", ";\n      color: #7a8188;\n    }\n  }\n"], ["\n  color: ", ";\n  ", "\n  &:hover {\n    color: ", ";\n  }\n\n  .dropdown-menu > li > &,\n  .dropdown-menu > span > li > & {\n    &.disabled:hover {\n      background: ", ";\n      color: #7a8188;\n    }\n  }\n"])), function (p) { return p.theme.textColor; }, overflowEllipsis_1.default, function (p) { return p.theme.textColor; }, function (p) { return p.theme.white; });
exports.default = MenuItemActionLink;
var templateObject_1;
//# sourceMappingURL=menuItemActionLink.jsx.map