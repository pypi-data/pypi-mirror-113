Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var is_prop_valid_1 = tslib_1.__importDefault(require("@emotion/is-prop-valid"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var input_1 = require("app/styles/input");
/**
 * Do not forward required to `input` to avoid default browser behavior
 */
var Input = styled_1.default('input', {
    shouldForwardProp: function (prop) {
        return typeof prop === 'string' && is_prop_valid_1.default(prop) && prop !== 'required';
    },
})(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), input_1.inputStyles);
// Cast type to avoid exporting theme
exports.default = Input;
var templateObject_1;
//# sourceMappingURL=input.jsx.map