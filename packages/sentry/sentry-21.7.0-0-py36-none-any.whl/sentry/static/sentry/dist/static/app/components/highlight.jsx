Object.defineProperty(exports, "__esModule", { value: true });
exports.HighlightComponent = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var HighlightComponent = function (_a) {
    var className = _a.className, children = _a.children, disabled = _a.disabled, text = _a.text;
    // There are instances when children is not string in breadcrumbs but not caught by TS
    if (!text || disabled || typeof children !== 'string') {
        return <React.Fragment>{children}</React.Fragment>;
    }
    var highlightText = text.toLowerCase();
    var idx = children.toLowerCase().indexOf(highlightText);
    if (idx === -1) {
        return <React.Fragment>{children}</React.Fragment>;
    }
    return (<React.Fragment>
      {children.substr(0, idx)}
      <span className={className}>{children.substr(idx, highlightText.length)}</span>
      {children.substr(idx + highlightText.length)}
    </React.Fragment>);
};
exports.HighlightComponent = HighlightComponent;
var Highlight = styled_1.default(HighlightComponent)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-weight: normal;\n  background-color: ", ";\n  color: ", ";\n"], ["\n  font-weight: normal;\n  background-color: ", ";\n  color: ", ";\n"])), function (p) { return p.theme.yellow200; }, function (p) { return p.theme.textColor; });
exports.default = Highlight;
var templateObject_1;
//# sourceMappingURL=highlight.jsx.map