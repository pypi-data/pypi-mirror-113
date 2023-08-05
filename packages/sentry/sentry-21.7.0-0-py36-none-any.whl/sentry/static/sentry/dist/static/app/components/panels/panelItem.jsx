Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var PanelItem = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  border-bottom: 1px solid ", ";\n  ", ";\n  ", ";\n\n  &:last-child {\n    border: 0;\n  }\n"], ["\n  display: flex;\n  border-bottom: 1px solid ", ";\n  ", ";\n  ", ";\n\n  &:last-child {\n    border: 0;\n  }\n"])), function (p) { return p.theme.innerBorder; }, function (p) { return p.noPadding || "padding: " + space_1.default(2); }, function (p) { return p.center && 'align-items: center'; });
exports.default = PanelItem;
var templateObject_1;
//# sourceMappingURL=panelItem.jsx.map