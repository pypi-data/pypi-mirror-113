Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var fieldControlState_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field/fieldControlState"));
var defaultProps = {
    flexibleControlStateSize: false,
};
var FieldControl = function (_a) {
    var inline = _a.inline, alignRight = _a.alignRight, disabled = _a.disabled, disabledReason = _a.disabledReason, errorState = _a.errorState, controlState = _a.controlState, children = _a.children, hideControlState = _a.hideControlState, _b = _a.flexibleControlStateSize, flexibleControlStateSize = _b === void 0 ? false : _b;
    return (<FieldControlErrorWrapper inline={inline}>
    <FieldControlWrapper>
      <FieldControlStyled alignRight={alignRight}>{children}</FieldControlStyled>

      {disabled && disabledReason && (<DisabledIndicator className="disabled-indicator">
          <StyledQuestionTooltip title={disabledReason} size="sm" position="top"/>
        </DisabledIndicator>)}

      {!hideControlState && (<fieldControlState_1.default flexibleControlStateSize={!!flexibleControlStateSize}>
          {controlState}
        </fieldControlState_1.default>)}
    </FieldControlWrapper>

    {!hideControlState && errorState}
  </FieldControlErrorWrapper>);
};
exports.default = FieldControl;
// This wraps Control + ControlError message
// * can NOT be a flex box here because of `position: absolute` on "control error message"
// * can NOT have overflow hidden because "control error message" overflows
var FieldControlErrorWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), function (p) { return (p.inline ? 'width: 50%; padding-left: 10px;' : ''); });
var FieldControlStyled = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  flex-direction: column;\n  position: relative;\n  max-width: 100%;\n  ", ";\n"], ["\n  display: flex;\n  flex: 1;\n  flex-direction: column;\n  position: relative;\n  max-width: 100%;\n  ", ";\n"])), function (p) { return (p.alignRight ? 'align-items: flex-end;' : ''); });
var FieldControlWrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-shrink: 0;\n"], ["\n  display: flex;\n  flex-shrink: 0;\n"])));
var StyledQuestionTooltip = styled_1.default(questionTooltip_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: block;\n  margin: 0 auto;\n"], ["\n  display: block;\n  margin: 0 auto;\n"])));
var DisabledIndicator = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin-left: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  margin-left: ", ";\n"])), space_1.default(1));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=fieldControl.jsx.map