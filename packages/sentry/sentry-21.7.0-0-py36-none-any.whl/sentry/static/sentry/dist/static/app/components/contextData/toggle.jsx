Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var icons_1 = require("app/icons");
function Toggle(_a) {
    var highUp = _a.highUp, wrapClassName = _a.wrapClassName, children = _a.children;
    var _b = tslib_1.__read(react_1.useState(false), 2), isExpanded = _b[0], setIsExpanded = _b[1];
    if (react_1.Children.count(children) === 0) {
        return null;
    }
    var wrappedChildren = <span className={wrapClassName}>{children}</span>;
    if (highUp) {
        return wrappedChildren;
    }
    return (<span>
      <IconWrapper isExpanded={isExpanded} onClick={function (evt) {
            setIsExpanded(!isExpanded);
            evt.preventDefault();
        }}>
        {isExpanded ? (<icons_1.IconSubtract size="9px" color="white"/>) : (<icons_1.IconAdd size="9px" color="white"/>)}
      </IconWrapper>
      {isExpanded && wrappedChildren}
    </span>);
}
exports.default = Toggle;
var IconWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  border-radius: 2px;\n  background: ", ";\n  display: inline-flex;\n  align-items: center;\n  justify-content: center;\n  cursor: pointer;\n  ", "\n"], ["\n  border-radius: 2px;\n  background: ", ";\n  display: inline-flex;\n  align-items: center;\n  justify-content: center;\n  cursor: pointer;\n  ", "\n"])), function (p) { return p.theme.white; }, function (p) {
    return p.isExpanded
        ? "\n          background: " + p.theme.gray300 + ";\n          border: 1px solid " + p.theme.gray300 + ";\n          &:hover {\n            background: " + p.theme.gray400 + ";\n          }\n        "
        : "\n          background: " + p.theme.blue300 + ";\n          border: 1px solid " + p.theme.blue300 + ";\n          &:hover {\n            background: " + p.theme.blue200 + ";\n          }\n        ";
});
var templateObject_1;
//# sourceMappingURL=toggle.jsx.map