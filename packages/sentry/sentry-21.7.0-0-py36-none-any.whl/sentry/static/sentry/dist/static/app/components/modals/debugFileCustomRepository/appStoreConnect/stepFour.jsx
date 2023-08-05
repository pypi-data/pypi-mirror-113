Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var input_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/controls/input"));
var field_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field"));
function StepFour(_a) {
    var onStartItunesAuthentication = _a.onStartItunesAuthentication, onStartSmsAuthentication = _a.onStartSmsAuthentication, stepFourData = _a.stepFourData, onSetStepFourData = _a.onSetStepFourData;
    return (<react_1.Fragment>
      <StyledAlert type="info" icon={<icons_1.IconInfo />}>
        <AlertContent>
          {locale_1.t('Did not get a verification code?')}
          <buttonBar_1.default gap={1}>
            <button_1.default size="small" title={locale_1.t('Get a new verification code')} onClick={function () { return onStartItunesAuthentication(false); }} icon={<icons_1.IconRefresh />}>
              {locale_1.t('Resend code')}
            </button_1.default>
            <button_1.default size="small" title={locale_1.t('Get a text message with a code')} onClick={function () { return onStartSmsAuthentication(); }} icon={<icons_1.IconMobile />}>
              {locale_1.t('Text me')}
            </button_1.default>
          </buttonBar_1.default>
        </AlertContent>
      </StyledAlert>
      <field_1.default label={locale_1.t('Two Factor authentication code')} inline={false} flexibleControlStateSize stacked required>
        <input_1.default type="text" name="two-factor-authentication-code" placeholder={locale_1.t('Enter your code')} value={stepFourData.authenticationCode} onChange={function (e) {
            return onSetStepFourData(tslib_1.__assign(tslib_1.__assign({}, stepFourData), { authenticationCode: e.target.value }));
        }}/>
      </field_1.default>
    </react_1.Fragment>);
}
exports.default = StepFour;
var StyledAlert = styled_1.default(alert_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  align-items: center;\n  span:nth-child(2) {\n    margin: 0;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  align-items: center;\n  span:nth-child(2) {\n    margin: 0;\n  }\n"])));
var AlertContent = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  align-items: center;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  align-items: center;\n  grid-gap: ", ";\n"])), space_1.default(2));
var templateObject_1, templateObject_2;
//# sourceMappingURL=stepFour.jsx.map