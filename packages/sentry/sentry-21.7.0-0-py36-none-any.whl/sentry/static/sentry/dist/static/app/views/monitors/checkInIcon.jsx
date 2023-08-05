Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
exports.default = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: inline-block;\n  position: relative;\n  border-radius: 50%;\n  height: ", "px;\n  width: ", "px;\n\n  ", ";\n"], ["\n  display: inline-block;\n  position: relative;\n  border-radius: 50%;\n  height: ", "px;\n  width: ", "px;\n\n  ", ";\n"])), function (p) { return p.size; }, function (p) { return p.size; }, function (p) {
    return p.color
        ? "background: " + p.color + ";"
        : "background: " + (p.status === 'error'
            ? p.theme.error
            : p.status === 'ok'
                ? p.theme.success
                : p.theme.disabled) + ";";
});
var templateObject_1;
//# sourceMappingURL=checkInIcon.jsx.map