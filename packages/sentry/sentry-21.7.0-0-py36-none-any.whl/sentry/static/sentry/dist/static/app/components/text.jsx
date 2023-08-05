Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var panel_1 = tslib_1.__importDefault(require("app/components/panels/panel"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var text_1 = tslib_1.__importDefault(require("app/styles/text"));
var Text = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  ", ";\n\n  ", " & {\n    padding-left: ", ";\n    padding-right: ", ";\n\n    &:first-child {\n      padding-top: ", ";\n    }\n  }\n"], ["\n  ", ";\n\n  " /* sc-selector */, " & {\n    padding-left: ", ";\n    padding-right: ", ";\n\n    &:first-child {\n      padding-top: ", ";\n    }\n  }\n"])), text_1.default, /* sc-selector */ panel_1.default, space_1.default(2), space_1.default(2), space_1.default(2));
exports.default = Text;
var templateObject_1;
//# sourceMappingURL=text.jsx.map