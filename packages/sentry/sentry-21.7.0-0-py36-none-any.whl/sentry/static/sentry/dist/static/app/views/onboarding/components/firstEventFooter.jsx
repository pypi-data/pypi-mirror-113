Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var createSampleEventButton_1 = tslib_1.__importDefault(require("app/views/onboarding/createSampleEventButton"));
var firstEventIndicator_1 = tslib_1.__importDefault(require("./firstEventIndicator"));
function FirstEventFooter(_a) {
    var organization = _a.organization, project = _a.project, docsLink = _a.docsLink, docsOnClick = _a.docsOnClick;
    return (<react_1.Fragment>
      <firstEventIndicator_1.default organization={organization} project={project} eventType="error">
        {function (_a) {
            var indicator = _a.indicator, firstEventButton = _a.firstEventButton;
            return (<CTAFooter>
            <Actions gap={2}>
              {firstEventButton}
              <button_1.default external href={docsLink} onClick={docsOnClick}>
                {locale_1.t('View full documentation')}
              </button_1.default>
            </Actions>
            {indicator}
          </CTAFooter>);
        }}
      </firstEventIndicator_1.default>
      <CTASecondary>
        {locale_1.tct('Just want to poke around before getting too cozy with the SDK? [sample:View a sample event for this SDK] and finish setup later.', {
            sample: (<createSampleEventButton_1.default project={project} source="onboarding" priority="link"/>),
        })}
      </CTASecondary>
    </react_1.Fragment>);
}
exports.default = FirstEventFooter;
var CTAFooter = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  margin: ", " 0;\n  margin-top: ", ";\n"], ["\n  display: flex;\n  justify-content: space-between;\n  margin: ", " 0;\n  margin-top: ", ";\n"])), space_1.default(2), space_1.default(4));
var CTASecondary = styled_1.default('p')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  margin: 0;\n  max-width: 500px;\n"], ["\n  color: ", ";\n  font-size: ", ";\n  margin: 0;\n  max-width: 500px;\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeMedium; });
var Actions = styled_1.default(buttonBar_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: inline-grid;\n  justify-self: start;\n"], ["\n  display: inline-grid;\n  justify-self: start;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=firstEventFooter.jsx.map