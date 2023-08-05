Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var BackToIssues = styled_1.default(react_router_1.Link)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  width: ", ";\n  height: ", ";\n  align-items: center;\n  justify-content: center;\n\n  box-sizing: content-box;\n  padding: ", ";\n  border-radius: 50%;\n\n  color: ", ";\n  background: ", ";\n  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);\n\n  z-index: 1;\n\n  &:hover {\n    background: ", ";\n    transform: scale(1.125);\n  }\n"], ["\n  display: flex;\n  width: ", ";\n  height: ", ";\n  align-items: center;\n  justify-content: center;\n\n  box-sizing: content-box;\n  padding: ", ";\n  border-radius: 50%;\n\n  color: ", ";\n  background: ", ";\n  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);\n\n  z-index: 1;\n\n  &:hover {\n    background: ", ";\n    transform: scale(1.125);\n  }\n"])), space_1.default(1.5), space_1.default(1.5), space_1.default(1), function (p) { return p.theme.textColor; }, function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.background; });
exports.default = BackToIssues;
var templateObject_1;
//# sourceMappingURL=backToIssues.jsx.map