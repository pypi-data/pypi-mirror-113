Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var alerts_empty_state_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/alerts-empty-state.svg"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var onboardingPanel_1 = tslib_1.__importDefault(require("app/components/onboardingPanel"));
var locale_1 = require("app/locale");
function Onboarding(_a) {
    var actions = _a.actions;
    return (<onboardingPanel_1.default image={<AlertsImage src={alerts_empty_state_svg_1.default}/>}>
      <h3>{locale_1.t('More signal, less noise')}</h3>
      <p>
        {locale_1.t('Not every error is worth an email. Set your own rules for alerts you need, with information that helps.')}
      </p>
      <ButtonList gap={1}>{actions}</ButtonList>
    </onboardingPanel_1.default>);
}
var AlertsImage = styled_1.default('img')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  @media (min-width: ", ") {\n    user-select: none;\n    position: absolute;\n    top: 0;\n    bottom: 0;\n    width: 220px;\n    margin-top: auto;\n    margin-bottom: auto;\n    transform: translateX(-50%);\n    left: 50%;\n  }\n\n  @media (min-width: ", ") {\n    transform: translateX(-60%);\n    width: 280px;\n  }\n\n  @media (min-width: ", ") {\n    transform: translateX(-75%);\n    width: 320px;\n  }\n"], ["\n  @media (min-width: ", ") {\n    user-select: none;\n    position: absolute;\n    top: 0;\n    bottom: 0;\n    width: 220px;\n    margin-top: auto;\n    margin-bottom: auto;\n    transform: translateX(-50%);\n    left: 50%;\n  }\n\n  @media (min-width: ", ") {\n    transform: translateX(-60%);\n    width: 280px;\n  }\n\n  @media (min-width: ", ") {\n    transform: translateX(-75%);\n    width: 320px;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.breakpoints[2]; }, function (p) { return p.theme.breakpoints[3]; });
var ButtonList = styled_1.default(buttonBar_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  grid-template-columns: repeat(auto-fit, minmax(130px, max-content));\n"], ["\n  grid-template-columns: repeat(auto-fit, minmax(130px, max-content));\n"])));
exports.default = Onboarding;
var templateObject_1, templateObject_2;
//# sourceMappingURL=onboarding.jsx.map