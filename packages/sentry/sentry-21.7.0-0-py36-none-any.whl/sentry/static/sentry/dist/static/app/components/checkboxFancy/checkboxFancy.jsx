Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var checkboxFancyContent_1 = tslib_1.__importDefault(require("./checkboxFancyContent"));
var disabledStyles = function (p) {
    return p.isDisabled && react_1.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n    background: ", ";\n    border-color: ", ";\n  "], ["\n    background: ", ";\n    border-color: ", ";\n  "])), p.isChecked || p.isIndeterminate
        ? p.theme.gray200
        : p.theme.backgroundSecondary, p.theme.border);
};
var hoverStyles = function (p) {
    return !p.isDisabled && react_1.css(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n    border: 2px solid\n      ", ";\n  "], ["\n    border: 2px solid\n      ", ";\n  "])), p.isChecked || p.isIndeterminate ? p.theme.active : p.theme.textColor);
};
var CheckboxFancy = styled_1.default(function (_a) {
    var isChecked = _a.isChecked, className = _a.className, isDisabled = _a.isDisabled, isIndeterminate = _a.isIndeterminate, onClick = _a.onClick;
    return (<div data-test-id="checkbox-fancy" role="checkbox" aria-disabled={isDisabled} aria-checked={isChecked} className={className} onClick={onClick}>
      <checkboxFancyContent_1.default isIndeterminate={isIndeterminate} isChecked={isChecked}/>
    </div>);
})(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  box-shadow: 1px 1px 5px 0px rgba(0, 0, 0, 0.05) inset;\n  width: ", ";\n  height: ", ";\n  border-radius: 5px;\n  background: ", ";\n  border: 2px solid\n    ", ";\n  cursor: ", ";\n  ", ";\n\n  &:hover {\n    ", "\n  }\n\n  ", "\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  box-shadow: 1px 1px 5px 0px rgba(0, 0, 0, 0.05) inset;\n  width: ", ";\n  height: ", ";\n  border-radius: 5px;\n  background: ", ";\n  border: 2px solid\n    ", ";\n  cursor: ", ";\n  ", ";\n\n  &:hover {\n    ", "\n  }\n\n  ", "\n"])), function (p) { return p.size; }, function (p) { return p.size; }, function (p) { return (p.isChecked || p.isIndeterminate ? p.theme.active : 'transparent'); }, function (p) { return (p.isChecked || p.isIndeterminate ? p.theme.active : p.theme.gray300); }, function (p) { return (p.isDisabled ? 'not-allowed' : 'pointer'); }, function (p) { return (!p.isChecked || !p.isIndeterminate) && 'transition: 500ms border ease-out'; }, hoverStyles, disabledStyles);
CheckboxFancy.defaultProps = {
    size: '16px',
    isChecked: false,
    isIndeterminate: false,
};
exports.default = CheckboxFancy;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=checkboxFancy.jsx.map