Object.defineProperty(exports, "__esModule", { value: true });
exports.modalCss = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var issueDiff_1 = tslib_1.__importDefault(require("app/components/issueDiff"));
var DiffModal = function (_a) {
    var className = _a.className, Body = _a.Body, CloseButton = _a.CloseButton, props = tslib_1.__rest(_a, ["className", "Body", "CloseButton"]);
    return (<Body>
    <CloseButton />
    <issueDiff_1.default className={className} {...props}/>
  </Body>);
};
var modalCss = react_1.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  left: 20px;\n  right: 20px;\n  top: 20px;\n  bottom: 20px;\n  display: flex;\n  padding: 0;\n  width: auto;\n\n  [role='document'] {\n    overflow: scroll;\n    height: 100%;\n    display: flex;\n    flex: 1;\n  }\n\n  section {\n    display: flex;\n    width: 100%;\n  }\n"], ["\n  position: absolute;\n  left: 20px;\n  right: 20px;\n  top: 20px;\n  bottom: 20px;\n  display: flex;\n  padding: 0;\n  width: auto;\n\n  [role='document'] {\n    overflow: scroll;\n    height: 100%;\n    display: flex;\n    flex: 1;\n  }\n\n  section {\n    display: flex;\n    width: 100%;\n  }\n"])));
exports.modalCss = modalCss;
exports.default = DiffModal;
var templateObject_1;
//# sourceMappingURL=diffModal.jsx.map