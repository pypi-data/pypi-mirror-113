Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var count_1 = tslib_1.__importDefault(require("app/components/count"));
var progressBar_1 = tslib_1.__importDefault(require("app/components/progressBar"));
var textOverflow_1 = tslib_1.__importDefault(require("app/components/textOverflow"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("../utils");
function ReleaseAdoption(_a) {
    var adoption = _a.adoption, releaseCount = _a.releaseCount, projectCount = _a.projectCount, displayOption = _a.displayOption, theme = _a.theme, withLabels = _a.withLabels;
    return (<div>
      {withLabels && (<Labels>
          <textOverflow_1.default>
            <count_1.default value={releaseCount}/>/<count_1.default value={projectCount}/>{' '}
            {utils_1.releaseDisplayLabel(displayOption, projectCount)}
          </textOverflow_1.default>

          <span>{!adoption ? 0 : adoption < 1 ? '<1' : Math.round(adoption)}%</span>
        </Labels>)}

      <tooltip_1.default containerDisplayMode="block" popperStyle={{
            background: theme.gray500,
            maxWidth: '300px',
        }} title={<TooltipWrapper>
            <TooltipRow>
              <Title>
                <Dot color={theme.progressBar}/>
                {locale_1.t('This Release')}
              </Title>
              <Value>
                <count_1.default value={releaseCount}/>{' '}
                {utils_1.releaseDisplayLabel(displayOption, releaseCount)}
              </Value>
            </TooltipRow>
            <TooltipRow>
              <Title>
                <Dot color={theme.progressBackground}/>
                {locale_1.t('Total Project')}
              </Title>
              <Value>
                <count_1.default value={projectCount}/>{' '}
                {utils_1.releaseDisplayLabel(displayOption, projectCount)}
              </Value>
            </TooltipRow>
            <Divider />

            <Time>{locale_1.t('Last 24 hours')}</Time>
          </TooltipWrapper>}>
        <ProgressBarWrapper>
          <progressBar_1.default value={Math.ceil(adoption)}/>
        </ProgressBarWrapper>
      </tooltip_1.default>
    </div>);
}
var Labels = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: 1fr max-content;\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: 1fr max-content;\n"])), space_1.default(1));
var TooltipWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n  font-size: ", ";\n  line-height: 21px;\n  font-weight: normal;\n"], ["\n  padding: ", ";\n  font-size: ", ";\n  line-height: 21px;\n  font-weight: normal;\n"])), space_1.default(0.75), function (p) { return p.theme.fontSizeMedium; });
var TooltipRow = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: auto auto;\n  grid-gap: ", ";\n  justify-content: space-between;\n  padding-bottom: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: auto auto;\n  grid-gap: ", ";\n  justify-content: space-between;\n  padding-bottom: ", ";\n"])), space_1.default(3), space_1.default(0.25));
var Title = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  text-align: left;\n"], ["\n  text-align: left;\n"])));
var Dot = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: inline-block;\n  margin-right: ", ";\n  border-radius: 10px;\n  width: 10px;\n  height: 10px;\n  background-color: ", ";\n"], ["\n  display: inline-block;\n  margin-right: ", ";\n  border-radius: 10px;\n  width: 10px;\n  height: 10px;\n  background-color: ", ";\n"])), space_1.default(0.75), function (p) { return p.color; });
var Value = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  text-align: right;\n"], ["\n  color: ", ";\n  text-align: right;\n"])), function (p) { return p.theme.gray300; });
var Divider = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  border-top: 1px solid ", ";\n  margin: ", " -", " ", ";\n"], ["\n  border-top: 1px solid ", ";\n  margin: ", " -", " ", ";\n"])), function (p) { return p.theme.gray400; }, space_1.default(0.75), space_1.default(2), space_1.default(1));
var Time = styled_1.default('div')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  text-align: center;\n"], ["\n  color: ", ";\n  text-align: center;\n"])), function (p) { return p.theme.gray300; });
var ProgressBarWrapper = styled_1.default('div')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  /* A bit of padding makes hovering for tooltip easier */\n  padding: ", " 0;\n"], ["\n  /* A bit of padding makes hovering for tooltip easier */\n  padding: ", " 0;\n"])), space_1.default(0.5));
exports.default = react_1.withTheme(ReleaseAdoption);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=releaseAdoption.jsx.map