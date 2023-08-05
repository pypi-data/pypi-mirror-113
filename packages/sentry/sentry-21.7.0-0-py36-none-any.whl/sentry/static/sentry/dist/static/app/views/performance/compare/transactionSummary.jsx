Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var utils_1 = require("app/components/events/interfaces/spans/utils");
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var utils_2 = require("app/components/performance/waterfall/utils");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_3 = require("../utils");
var utils_4 = require("./utils");
var TransactionSummary = /** @class */ (function (_super) {
    tslib_1.__extends(TransactionSummary, _super);
    function TransactionSummary() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TransactionSummary.prototype.render = function () {
        var _a = this.props, baselineEvent = _a.baselineEvent, regressionEvent = _a.regressionEvent, organization = _a.organization, location = _a.location, params = _a.params;
        var baselineEventSlug = params.baselineEventSlug, regressionEventSlug = params.regressionEventSlug;
        if (!utils_4.isTransactionEvent(baselineEvent) || !utils_4.isTransactionEvent(regressionEvent)) {
            return null;
        }
        var baselineTrace = utils_1.parseTrace(baselineEvent);
        var regressionTrace = utils_1.parseTrace(regressionEvent);
        var baselineDuration = Math.abs(baselineTrace.traceStartTimestamp - baselineTrace.traceEndTimestamp);
        var regressionDuration = Math.abs(regressionTrace.traceStartTimestamp - regressionTrace.traceEndTimestamp);
        return (<Container>
        <EventRow>
          <Baseline />
          <EventRowContent>
            <Content>
              <ContentTitle>{locale_1.t('Baseline Event')}</ContentTitle>
              <EventId>
                <span>{locale_1.t('ID')}: </span>
                <StyledLink to={utils_3.getTransactionDetailsUrl(organization, baselineEventSlug.trim(), baselineEvent.title, location.query)}>
                  {shortEventId(baselineEvent.eventID)}
                </StyledLink>
              </EventId>
            </Content>
            <TimeDuration>
              <span>{utils_2.getHumanDuration(baselineDuration)}</span>
            </TimeDuration>
          </EventRowContent>
        </EventRow>
        <EventRow>
          <Regression />
          <EventRowContent>
            <Content>
              <ContentTitle>{locale_1.t('This Event')}</ContentTitle>
              <EventId>
                <span>{locale_1.t('ID')}: </span>
                <StyledLink to={utils_3.getTransactionDetailsUrl(organization, regressionEventSlug.trim(), regressionEvent.title, location.query)}>
                  {shortEventId(regressionEvent.eventID)}
                </StyledLink>
              </EventId>
            </Content>
            <TimeDuration>
              <span>{utils_2.getHumanDuration(regressionDuration)}</span>
            </TimeDuration>
          </EventRowContent>
        </EventRow>
      </Container>);
    };
    return TransactionSummary;
}(react_1.Component));
var Container = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n\n  justify-content: space-between;\n  align-content: space-between;\n\n  padding-bottom: ", ";\n\n  > * + * {\n    margin-top: ", ";\n  }\n"], ["\n  display: flex;\n  flex-direction: column;\n\n  justify-content: space-between;\n  align-content: space-between;\n\n  padding-bottom: ", ";\n\n  > * + * {\n    margin-top: ", ";\n  }\n"])), space_1.default(1), space_1.default(0.75));
var EventRow = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var Baseline = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  background-color: ", ";\n  height: 100%;\n  width: 4px;\n\n  margin-right: ", ";\n"], ["\n  background-color: ", ";\n  height: 100%;\n  width: 4px;\n\n  margin-right: ", ";\n"])), function (p) { return p.theme.textColor; }, space_1.default(1));
var Regression = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  background-color: ", ";\n  height: 100%;\n  width: 4px;\n\n  margin-right: ", ";\n"], ["\n  background-color: ", ";\n  height: 100%;\n  width: 4px;\n\n  margin-right: ", ";\n"])), function (p) { return p.theme.purple200; }, space_1.default(1));
var EventRowContent = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  flex-grow: 1;\n  display: flex;\n"], ["\n  flex-grow: 1;\n  display: flex;\n"])));
var TimeDuration = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n\n  font-size: ", ";\n  line-height: 1.2;\n\n  margin-left: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n\n  font-size: ", ";\n  line-height: 1.2;\n\n  margin-left: ", ";\n"])), function (p) { return p.theme.headerFontSize; }, space_1.default(1));
var Content = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  flex-grow: 1;\n  width: 150px;\n\n  font-size: ", ";\n"], ["\n  flex-grow: 1;\n  width: 150px;\n\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
var ContentTitle = styled_1.default('div')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  font-weight: 600;\n"], ["\n  font-weight: 600;\n"])));
var EventId = styled_1.default('div')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var StyledLink = styled_1.default(link_1.default)(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
function shortEventId(value) {
    return value.substring(0, 8);
}
exports.default = TransactionSummary;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10;
//# sourceMappingURL=transactionSummary.jsx.map