Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var DateDivider = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  color: ", ";\n  margin: ", " 0;\n\n  &:before,\n  &:after {\n    content: '';\n    display: block;\n    flex-grow: 1;\n    height: 1px;\n    background-color: ", ";\n  }\n\n  &:before {\n    margin-right: ", ";\n  }\n\n  &:after {\n    margin-left: ", ";\n  }\n"], ["\n  font-size: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  color: ", ";\n  margin: ", " 0;\n\n  &:before,\n  &:after {\n    content: '';\n    display: block;\n    flex-grow: 1;\n    height: 1px;\n    background-color: ", ";\n  }\n\n  &:before {\n    margin-right: ", ";\n  }\n\n  &:after {\n    margin-left: ", ";\n  }\n"])), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.subText; }, space_1.default(1.5), function (p) { return p.theme.gray200; }, space_1.default(2), space_1.default(2));
exports.default = DateDivider;
var templateObject_1;
//# sourceMappingURL=dateDivider.jsx.map