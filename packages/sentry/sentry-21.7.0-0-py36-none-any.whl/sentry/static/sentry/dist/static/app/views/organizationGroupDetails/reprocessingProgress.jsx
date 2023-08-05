Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var progressBar_1 = tslib_1.__importDefault(require("app/components/progressBar"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
function ReprocessingProgress(_a) {
    var totalEvents = _a.totalEvents, pendingEvents = _a.pendingEvents;
    var remainingEventsToReprocess = totalEvents - pendingEvents;
    var remainingEventsToReprocessPercent = utils_1.percent(remainingEventsToReprocess, totalEvents);
    return (<Wrapper>
      <Inner>
        <Header>
          <Title>{locale_1.t('Reprocessing\u2026')}</Title>
          {locale_1.t('Once the events in this issue have been reprocessed, you’ll be able to make changes and view any new issues that may have been created.')}
        </Header>
        <Content>
          <progressBar_1.default value={remainingEventsToReprocessPercent} variant="large"/>
          {locale_1.tct('[remainingEventsToReprocess]/[totalEvents] [event] reprocessed', {
            remainingEventsToReprocess: remainingEventsToReprocess,
            totalEvents: totalEvents,
            event: locale_1.tn('event', 'events', totalEvents),
        })}
        </Content>
      </Inner>
    </Wrapper>);
}
exports.default = ReprocessingProgress;
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin: ", " 40px;\n  flex: 1;\n  text-align: center;\n\n  @media (min-width: ", ") {\n    margin: 40px;\n  }\n"], ["\n  margin: ", " 40px;\n  flex: 1;\n  text-align: center;\n\n  @media (min-width: ", ") {\n    margin: 40px;\n  }\n"])), space_1.default(4), function (p) { return p.theme.breakpoints[0]; });
var Content = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  display: grid;\n  grid-gap: ", ";\n  justify-items: center;\n  max-width: 402px;\n  width: 100%;\n"], ["\n  color: ", ";\n  font-size: ", ";\n  display: grid;\n  grid-gap: ", ";\n  justify-items: center;\n  max-width: 402px;\n  width: 100%;\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeMedium; }, space_1.default(1.5));
var Inner = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  justify-items: center;\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  justify-items: center;\n"])), space_1.default(3));
var Header = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  color: ", ";\n  max-width: 557px;\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  color: ", ";\n  max-width: 557px;\n"])), space_1.default(1), function (p) { return p.theme.textColor; });
var Title = styled_1.default('h3')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  font-weight: 600;\n  margin-bottom: 0;\n"], ["\n  font-size: ", ";\n  font-weight: 600;\n  margin-bottom: 0;\n"])), function (p) { return p.theme.headerFontSize; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=reprocessingProgress.jsx.map