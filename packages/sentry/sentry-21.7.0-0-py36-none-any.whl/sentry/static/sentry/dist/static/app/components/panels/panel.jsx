Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var Panel = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  background: ", ";\n  border-radius: ", ";\n  border: 1px\n    ", ";\n  box-shadow: ", ";\n  margin-bottom: ", ";\n  position: relative;\n"], ["\n  background: ", ";\n  border-radius: ", ";\n  border: 1px\n    ", ";\n  box-shadow: ", ";\n  margin-bottom: ", ";\n  position: relative;\n"])), function (p) { return (p.dashedBorder ? p.theme.backgroundSecondary : p.theme.background); }, function (p) { return p.theme.borderRadius; }, function (p) { return (p.dashedBorder ? 'dashed' + p.theme.gray300 : 'solid ' + p.theme.border); }, function (p) { return (p.dashedBorder ? 'none' : p.theme.dropShadowLight); }, space_1.default(3));
exports.default = Panel;
var templateObject_1;
//# sourceMappingURL=panel.jsx.map