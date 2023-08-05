Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Well = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  border: 1px solid ", ";\n  box-shadow: none;\n  background: ", ";\n  padding: ", ";\n  margin-bottom: 20px;\n  border-radius: 3px;\n  ", ";\n"], ["\n  border: 1px solid ", ";\n  box-shadow: none;\n  background: ", ";\n  padding: ", ";\n  margin-bottom: 20px;\n  border-radius: 3px;\n  ", ";\n"])), function (p) { return p.theme.border; }, function (p) { return p.theme.backgroundSecondary; }, function (p) { return (p.hasImage ? '80px 30px' : '15px 20px'); }, function (p) { return p.centered && 'text-align: center'; });
exports.default = Well;
var templateObject_1;
//# sourceMappingURL=well.jsx.map