Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var eventOrGroupHeader_1 = tslib_1.__importDefault(require("app/components/eventOrGroupHeader"));
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
function NewIssue(_a) {
    var sampleEvent = _a.sampleEvent, eventCount = _a.eventCount, organization = _a.organization;
    return (<react_1.Fragment>
      <EventDetails>
        <eventOrGroupHeader_1.default data={sampleEvent} organization={organization} hideIcons hideLevel/>
        <ExtraInfo>
          <TimeWrapper>
            <StyledIconClock size="11px"/>
            <timeSince_1.default date={sampleEvent.dateCreated} suffix={locale_1.t('old')}/>
          </TimeWrapper>
        </ExtraInfo>
      </EventDetails>
      <EventCount>{eventCount}</EventCount>
    </react_1.Fragment>);
}
exports.default = NewIssue;
var EventDetails = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  overflow: hidden;\n  line-height: 1.1;\n"], ["\n  overflow: hidden;\n  line-height: 1.1;\n"])));
var ExtraInfo = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  justify-content: flex-start;\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  justify-content: flex-start;\n"])), space_1.default(2));
var TimeWrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: max-content 1fr;\n  align-items: center;\n  font-size: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: max-content 1fr;\n  align-items: center;\n  font-size: ", ";\n"])), space_1.default(0.5), function (p) { return p.theme.fontSizeSmall; });
var EventCount = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  align-items: center;\n  line-height: 1.1;\n"], ["\n  align-items: center;\n  line-height: 1.1;\n"])));
var StyledIconClock = styled_1.default(icons_1.IconClock)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.subText; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=newIssue.jsx.map