Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var Crumb = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  position: relative;\n  font-size: 18px;\n  color: ", ";\n  padding-right: ", ";\n  cursor: pointer;\n  white-space: nowrap;\n\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  position: relative;\n  font-size: 18px;\n  color: ", ";\n  padding-right: ", ";\n  cursor: pointer;\n  white-space: nowrap;\n\n  &:hover {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.subText; }, space_1.default(1), function (p) { return p.theme.textColor; });
exports.default = Crumb;
var templateObject_1;
//# sourceMappingURL=crumb.jsx.map