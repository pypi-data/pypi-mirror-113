Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var is_prop_valid_1 = tslib_1.__importDefault(require("@emotion/is-prop-valid"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var shouldForwardProp = function (p) { return p !== 'disabled' && is_prop_valid_1.default(p); };
var FieldLabel = styled_1.default('div', { shouldForwardProp: shouldForwardProp })(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  display: flex;\n  gap: ", ";\n  line-height: 16px;\n"], ["\n  color: ", ";\n  display: flex;\n  gap: ", ";\n  line-height: 16px;\n"])), function (p) { return (!p.disabled ? p.theme.textColor : p.theme.disabled); }, space_1.default(0.5));
exports.default = FieldLabel;
var templateObject_1;
//# sourceMappingURL=fieldLabel.jsx.map