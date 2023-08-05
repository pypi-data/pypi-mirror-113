Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var EventAnnotation = styled_1.default('span')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  border-left: 1px solid ", ";\n  padding-left: ", ";\n  color: ", ";\n\n  a {\n    color: ", ";\n\n    &:hover {\n      color: ", ";\n    }\n  }\n"], ["\n  font-size: ", ";\n  border-left: 1px solid ", ";\n  padding-left: ", ";\n  color: ", ";\n\n  a {\n    color: ", ";\n\n    &:hover {\n      color: ", ";\n    }\n  }\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.innerBorder; }, space_1.default(1), function (p) { return p.theme.gray300; }, function (p) { return p.theme.gray300; }, function (p) { return p.theme.subText; });
exports.default = EventAnnotation;
var templateObject_1;
//# sourceMappingURL=eventAnnotation.jsx.map