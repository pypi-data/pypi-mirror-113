Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var listItem_1 = tslib_1.__importDefault(require("app/components/list/listItem"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var Item = styled_1.default(function (_a) {
    var title = _a.title, subtitle = _a.subtitle, children = _a.children, className = _a.className;
    return (<listItem_1.default className={className}>
    {title}
    {subtitle && <small>{subtitle}</small>}
    <div>{children}</div>
  </listItem_1.default>);
})(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n"])), space_1.default(1.5));
exports.default = Item;
var templateObject_1;
//# sourceMappingURL=item.jsx.map