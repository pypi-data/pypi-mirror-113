Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var defaultProps = {
    shape: 'rect',
    bottomGutter: 0,
    width: '100%',
    height: '60px',
    testId: 'loading-placeholder',
};
var Placeholder = styled_1.default(function (_a) {
    var className = _a.className, children = _a.children, error = _a.error, testId = _a.testId;
    return (<div data-test-id={testId} className={className}>
      {error || children}
    </div>);
})(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  flex-shrink: 0;\n  justify-content: center;\n  align-items: center;\n\n  background-color: ", ";\n  ", "\n  width: ", ";\n  height: ", ";\n  ", "\n  ", "\n"], ["\n  display: flex;\n  flex-direction: column;\n  flex-shrink: 0;\n  justify-content: center;\n  align-items: center;\n\n  background-color: ", ";\n  ", "\n  width: ", ";\n  height: ", ";\n  ", "\n  ", "\n"])), function (p) { return (p.error ? p.theme.red100 : p.theme.backgroundSecondary); }, function (p) { return p.error && "color: " + p.theme.red200 + ";"; }, function (p) { return p.width; }, function (p) { return p.height; }, function (p) { return (p.shape === 'circle' ? 'border-radius: 100%;' : ''); }, function (p) {
    return typeof p.bottomGutter === 'number' && p.bottomGutter > 0
        ? "margin-bottom: " + space_1.default(p.bottomGutter) + ";"
        : '';
});
Placeholder.defaultProps = defaultProps;
exports.default = Placeholder;
var templateObject_1;
//# sourceMappingURL=placeholder.jsx.map