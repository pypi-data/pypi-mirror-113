Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var FieldRequiredBadge = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: inline-block;\n  background: ", ";\n  opacity: 0.6;\n  width: 5px;\n  height: 5px;\n  border-radius: 5px;\n  text-indent: -9999em;\n  vertical-align: super;\n  margin-left: ", ";\n"], ["\n  display: inline-block;\n  background: ", ";\n  opacity: 0.6;\n  width: 5px;\n  height: 5px;\n  border-radius: 5px;\n  text-indent: -9999em;\n  vertical-align: super;\n  margin-left: ", ";\n"])), function (p) { return p.theme.red300; }, space_1.default(0.5));
exports.default = FieldRequiredBadge;
var templateObject_1;
//# sourceMappingURL=fieldRequiredBadge.jsx.map