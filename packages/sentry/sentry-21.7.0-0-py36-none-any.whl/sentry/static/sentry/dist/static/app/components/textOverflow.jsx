Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var overflowEllipsisLeft_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsisLeft"));
var TextOverflow = styled_1.default(function (_a) {
    var isParagraph = _a.isParagraph, className = _a.className, children = _a.children;
    var Component = isParagraph ? 'p' : 'div';
    return <Component className={className}>{children}</Component>;
})(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  ", ";\n  width: auto;\n  line-height: 1.1;\n"], ["\n  ", ";\n  width: auto;\n  line-height: 1.1;\n"])), function (p) { return (p.ellipsisDirection === 'right' ? overflowEllipsis_1.default : overflowEllipsisLeft_1.default); });
TextOverflow.defaultProps = {
    ellipsisDirection: 'right',
    isParagraph: false,
};
exports.default = TextOverflow;
var templateObject_1;
//# sourceMappingURL=textOverflow.jsx.map