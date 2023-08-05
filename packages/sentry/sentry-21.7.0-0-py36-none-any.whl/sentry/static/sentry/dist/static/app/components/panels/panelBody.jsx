Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var text_1 = tslib_1.__importDefault(require("app/styles/text"));
var PanelBody = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  ", ";\n  ", ";\n"], ["\n  ", ";\n  ", ";\n"])), function (p) { return p.withPadding && "padding: " + space_1.default(2); }, text_1.default);
exports.default = PanelBody;
var templateObject_1;
//# sourceMappingURL=panelBody.jsx.map