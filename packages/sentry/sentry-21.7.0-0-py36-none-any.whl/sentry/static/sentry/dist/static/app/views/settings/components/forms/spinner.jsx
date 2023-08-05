Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var spin = react_1.keyframes(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  0% {\n    transform: rotate(0deg);\n  }\n  100% {\n    transform: rotate(360deg);\n  }\n"], ["\n  0% {\n    transform: rotate(0deg);\n  }\n  100% {\n    transform: rotate(360deg);\n  }\n"])));
var Spinner = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  animation: ", " 0.4s linear infinite;\n  width: 18px;\n  height: 18px;\n  border-radius: 18px;\n  border-top: 2px solid ", ";\n  border-right: 2px solid ", ";\n  border-bottom: 2px solid ", ";\n  border-left: 2px solid ", ";\n  margin-left: auto;\n"], ["\n  animation: ", " 0.4s linear infinite;\n  width: 18px;\n  height: 18px;\n  border-radius: 18px;\n  border-top: 2px solid ", ";\n  border-right: 2px solid ", ";\n  border-bottom: 2px solid ", ";\n  border-left: 2px solid ", ";\n  margin-left: auto;\n"])), spin, function (p) { return p.theme.border; }, function (p) { return p.theme.border; }, function (p) { return p.theme.border; }, function (p) { return p.theme.purple300; });
exports.default = Spinner;
var templateObject_1, templateObject_2;
//# sourceMappingURL=spinner.jsx.map