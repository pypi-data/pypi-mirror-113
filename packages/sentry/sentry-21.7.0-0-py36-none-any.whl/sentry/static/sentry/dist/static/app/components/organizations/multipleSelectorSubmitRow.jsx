Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var locale_1 = require("app/locale");
var animations_1 = require("app/styles/animations");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var MultipleSelectorSubmitRow = function (_a) {
    var onSubmit = _a.onSubmit, _b = _a.disabled, disabled = _b === void 0 ? false : _b;
    return (<SubmitButtonContainer>
    <SubmitButton disabled={disabled} onClick={onSubmit} size="xsmall" priority="primary">
      {locale_1.t('Apply')}
    </SubmitButton>
  </SubmitButtonContainer>);
};
var SubmitButtonContainer = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n"], ["\n  display: flex;\n  justify-content: flex-end;\n"])));
var SubmitButton = styled_1.default(button_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  animation: 0.1s ", " ease-in;\n  margin: ", " 0;\n"], ["\n  animation: 0.1s ", " ease-in;\n  margin: ", " 0;\n"])), animations_1.growIn, space_1.default(0.5));
exports.default = MultipleSelectorSubmitRow;
var templateObject_1, templateObject_2;
//# sourceMappingURL=multipleSelectorSubmitRow.jsx.map