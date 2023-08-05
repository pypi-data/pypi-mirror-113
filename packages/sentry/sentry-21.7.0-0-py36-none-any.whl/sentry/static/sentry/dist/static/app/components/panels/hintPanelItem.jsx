Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var HintPanelItem = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  padding: ", ";\n  border-bottom: 1px solid ", ";\n  background: ", ";\n  font-size: ", ";\n\n  h2 {\n    font-size: ", ";\n    margin-bottom: 0;\n  }\n\n  &:last-child {\n    border: 0;\n  }\n"], ["\n  display: flex;\n  padding: ", ";\n  border-bottom: 1px solid ", ";\n  background: ", ";\n  font-size: ", ";\n\n  h2 {\n    font-size: ", ";\n    margin-bottom: 0;\n  }\n\n  &:last-child {\n    border: 0;\n  }\n"])), space_1.default(2), function (p) { return p.theme.innerBorder; }, function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.fontSizeLarge; });
exports.default = HintPanelItem;
var templateObject_1;
//# sourceMappingURL=hintPanelItem.jsx.map