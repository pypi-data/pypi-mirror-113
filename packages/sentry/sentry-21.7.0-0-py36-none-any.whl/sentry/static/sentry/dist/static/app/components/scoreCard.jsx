Object.defineProperty(exports, "__esModule", { value: true });
exports.Trend = exports.ScoreWrapper = exports.Score = exports.StyledPanel = exports.HeaderTitle = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var panels_1 = require("app/components/panels");
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var textOverflow_1 = tslib_1.__importDefault(require("app/components/textOverflow"));
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
function ScoreCard(_a) {
    var title = _a.title, score = _a.score, help = _a.help, trend = _a.trend, trendStatus = _a.trendStatus, className = _a.className;
    return (<StyledPanel className={className}>
      <HeaderTitle>
        <Title>{title}</Title>
        {help && <questionTooltip_1.default title={help} size="sm" position="top"/>}
      </HeaderTitle>

      <ScoreWrapper>
        <Score>{score !== null && score !== void 0 ? score : '\u2014'}</Score>
        {utils_1.defined(trend) && (<Trend trendStatus={trendStatus}>
            <textOverflow_1.default>{trend}</textOverflow_1.default>
          </Trend>)}
      </ScoreWrapper>
    </StyledPanel>);
}
function getTrendColor(p) {
    switch (p.trendStatus) {
        case 'good':
            return p.theme.green300;
        case 'bad':
            return p.theme.red300;
        default:
            return p.theme.gray300;
    }
}
var StyledPanel = styled_1.default(panels_1.Panel)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  justify-content: space-between;\n  padding: ", " ", ";\n  min-height: 96px;\n"], ["\n  display: flex;\n  flex-direction: column;\n  justify-content: space-between;\n  padding: ", " ", ";\n  min-height: 96px;\n"])), space_1.default(2), space_1.default(3));
exports.StyledPanel = StyledPanel;
var HeaderTitle = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: center;\n  width: fit-content;\n"], ["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: center;\n  width: fit-content;\n"])), space_1.default(1));
exports.HeaderTitle = HeaderTitle;
var Title = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), overflowEllipsis_1.default);
var ScoreWrapper = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n  align-items: flex-end;\n  max-width: 100%;\n"], ["\n  display: flex;\n  flex-direction: row;\n  align-items: flex-end;\n  max-width: 100%;\n"])));
exports.ScoreWrapper = ScoreWrapper;
var Score = styled_1.default('span')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  flex-shrink: 1;\n  font-size: 32px;\n  line-height: 1;\n  white-space: nowrap;\n"], ["\n  flex-shrink: 1;\n  font-size: 32px;\n  line-height: 1;\n  white-space: nowrap;\n"])));
exports.Score = Score;
var Trend = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  margin-left: ", ";\n  line-height: 1;\n  overflow: hidden;\n"], ["\n  color: ", ";\n  margin-left: ", ";\n  line-height: 1;\n  overflow: hidden;\n"])), getTrendColor, space_1.default(1));
exports.Trend = Trend;
exports.default = ScoreCard;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=scoreCard.jsx.map