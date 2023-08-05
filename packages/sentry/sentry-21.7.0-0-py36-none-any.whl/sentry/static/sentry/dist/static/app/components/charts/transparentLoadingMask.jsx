Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var loadingMask_1 = tslib_1.__importDefault(require("app/components/loadingMask"));
var TransparentLoadingMask = styled_1.default(function (_a) {
    var className = _a.className, visible = _a.visible, children = _a.children, props = tslib_1.__rest(_a, ["className", "visible", "children"]);
    var other = visible ? tslib_1.__assign(tslib_1.__assign({}, props), { 'data-test-id': 'loading-placeholder' }) : props;
    return (<loadingMask_1.default className={className} {...other}>
        {children}
      </loadingMask_1.default>);
})(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  ", ";\n  opacity: 0.4;\n  z-index: 1;\n"], ["\n  ", ";\n  opacity: 0.4;\n  z-index: 1;\n"])), function (p) { return !p.visible && 'display: none;'; });
exports.default = TransparentLoadingMask;
var templateObject_1;
//# sourceMappingURL=transparentLoadingMask.jsx.map