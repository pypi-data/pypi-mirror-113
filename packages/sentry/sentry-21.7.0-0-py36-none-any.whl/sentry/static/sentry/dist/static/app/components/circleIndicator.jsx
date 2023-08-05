Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var defaultProps = {
    enabled: true,
    size: 14,
};
var getBackgroundColor = function (p) {
    if (p.color) {
        return "background: " + p.color + ";";
    }
    return "background: " + (p.enabled ? p.theme.success : p.theme.error) + ";";
};
var getSize = function (p) { return "\n  height: " + p.size + "px;\n  width: " + p.size + "px;\n"; };
var CircleIndicator = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: inline-block;\n  position: relative;\n  border-radius: 50%;\n  ", ";\n  ", ";\n"], ["\n  display: inline-block;\n  position: relative;\n  border-radius: 50%;\n  ", ";\n  ", ";\n"])), getSize, getBackgroundColor);
CircleIndicator.defaultProps = defaultProps;
exports.default = CircleIndicator;
var templateObject_1;
//# sourceMappingURL=circleIndicator.jsx.map