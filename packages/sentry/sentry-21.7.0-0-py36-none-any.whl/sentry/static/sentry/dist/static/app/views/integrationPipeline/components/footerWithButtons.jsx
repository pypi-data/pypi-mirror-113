Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/actions/button"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
function FooterWithButtons(_a) {
    var buttonText = _a.buttonText, rest = tslib_1.__rest(_a, ["buttonText"]);
    return (<Footer>
      <button_1.default priority="primary" type="submit" size="xsmall" {...rest}>
        {buttonText}
      </button_1.default>
    </Footer>);
}
exports.default = FooterWithButtons;
// wrap in form so we can keep form submission behavior
var Footer = styled_1.default('form')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  width: 100%;\n  position: fixed;\n  display: flex;\n  justify-content: flex-end;\n  bottom: 0;\n  z-index: 100;\n  background-color: ", ";\n  border-top: 1px solid ", ";\n  padding: ", ";\n"], ["\n  width: 100%;\n  position: fixed;\n  display: flex;\n  justify-content: flex-end;\n  bottom: 0;\n  z-index: 100;\n  background-color: ", ";\n  border-top: 1px solid ", ";\n  padding: ", ";\n"])), function (p) { return p.theme.bodyBackground; }, function (p) { return p.theme.innerBorder; }, space_1.default(2));
var templateObject_1;
//# sourceMappingURL=footerWithButtons.jsx.map