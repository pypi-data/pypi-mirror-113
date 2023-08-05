Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var panels_1 = require("app/components/panels");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var Header = styled_1.default(panels_1.PanelHeader)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  border-top-left-radius: 0;\n  padding: ", " ", ";\n  font-size: ", ";\n"], ["\n  border-top-left-radius: 0;\n  padding: ", " ", ";\n  font-size: ", ";\n"])), space_1.default(1.5), space_1.default(2), function (p) { return p.theme.fontSizeSmall; });
exports.default = Header;
var templateObject_1;
//# sourceMappingURL=header.jsx.map