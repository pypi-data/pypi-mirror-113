Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Redaction = styled_1.default(function (_a) {
    var children = _a.children, className = _a.className;
    return (<span className={className}>{children}</span>);
})(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  cursor: default;\n  vertical-align: middle;\n  ", "\n"], ["\n  cursor: default;\n  vertical-align: middle;\n  ", "\n"])), function (p) { return !p.withoutBackground && "background: rgba(255, 0, 0, 0.05);"; });
exports.default = Redaction;
var templateObject_1;
//# sourceMappingURL=redaction.jsx.map