Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var loadingMask_1 = tslib_1.__importDefault(require("app/components/loadingMask"));
var LoadingPanel = styled_1.default(function (_a) {
    var _height = _a.height, props = tslib_1.__rest(_a, ["height"]);
    return (<div {...props}>
    <loadingMask_1.default />
  </div>);
})(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n  flex-shrink: 0;\n  overflow: hidden;\n  height: ", ";\n  position: relative;\n  border-color: transparent;\n  margin-bottom: 0;\n"], ["\n  flex: 1;\n  flex-shrink: 0;\n  overflow: hidden;\n  height: ", ";\n  position: relative;\n  border-color: transparent;\n  margin-bottom: 0;\n"])), function (p) { return p.height; });
LoadingPanel.defaultProps = {
    height: '200px',
};
exports.default = LoadingPanel;
var templateObject_1;
//# sourceMappingURL=loadingPanel.jsx.map