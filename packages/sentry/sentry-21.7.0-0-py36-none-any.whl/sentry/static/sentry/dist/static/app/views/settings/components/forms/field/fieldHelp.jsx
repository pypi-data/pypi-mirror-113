Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var FieldHelp = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-size: 14px;\n  margin-top: ", ";\n  line-height: 1.4;\n"], ["\n  color: ", ";\n  font-size: 14px;\n  margin-top: ", ";\n  line-height: 1.4;\n"])), function (p) { return p.theme.gray300; }, function (p) { return (p.stacked && !p.inline ? 0 : space_1.default(1)); });
exports.default = FieldHelp;
var templateObject_1;
//# sourceMappingURL=fieldHelp.jsx.map