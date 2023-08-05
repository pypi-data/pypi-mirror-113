Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var classnames_1 = tslib_1.__importDefault(require("classnames"));
var count_1 = tslib_1.__importDefault(require("app/components/count"));
var eventOrGroupTitle_1 = tslib_1.__importDefault(require("app/components/eventOrGroupTitle"));
var eventAnnotation_1 = tslib_1.__importDefault(require("app/components/events/eventAnnotation"));
var eventMessage_1 = tslib_1.__importDefault(require("app/components/events/eventMessage"));
var hovercard_1 = tslib_1.__importDefault(require("app/components/hovercard"));
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var events_1 = require("app/utils/events");
var IssueLink = function (_a) {
    var children = _a.children, orgId = _a.orgId, issue = _a.issue, to = _a.to, _b = _a.card, card = _b === void 0 ? true : _b;
    if (!card) {
        return <react_router_1.Link to={to}>{children}</react_router_1.Link>;
    }
    var message = events_1.getMessage(issue);
    var className = classnames_1.default({
        isBookmarked: issue.isBookmarked,
        hasSeen: issue.hasSeen,
        isResolved: issue.status === 'resolved',
    });
    var streamPath = "/organizations/" + orgId + "/issues/";
    var hovercardBody = (<div className={className}>
      <Section>
        <Title>
          <eventOrGroupTitle_1.default data={issue}/>
        </Title>

        <HovercardEventMessage level={issue.level} levelIndicatorSize="9px" message={message} annotations={<React.Fragment>
              {issue.logger && (<eventAnnotation_1.default>
                  <react_router_1.Link to={{
                    pathname: streamPath,
                    query: { query: "logger:" + issue.logger },
                }}>
                    {issue.logger}
                  </react_router_1.Link>
                </eventAnnotation_1.default>)}
              {issue.annotations.map(function (annotation, i) { return (<eventAnnotation_1.default key={i} dangerouslySetInnerHTML={{ __html: annotation }}/>); })}
            </React.Fragment>}/>
      </Section>

      <Grid>
        <div>
          <GridHeader>{locale_1.t('First Seen')}</GridHeader>
          <StyledTimeSince date={issue.firstSeen}/>
        </div>
        <div>
          <GridHeader>{locale_1.t('Last Seen')}</GridHeader>
          <StyledTimeSince date={issue.lastSeen}/>
        </div>
        <div>
          <GridHeader>{locale_1.t('Occurrences')}</GridHeader>
          <count_1.default value={issue.count}/>
        </div>
        <div>
          <GridHeader>{locale_1.t('Users Affected')}</GridHeader>
          <count_1.default value={issue.userCount}/>
        </div>
      </Grid>
    </div>);
    return (<hovercard_1.default body={hovercardBody} header={issue.shortId}>
      <react_router_1.Link to={to}>{children}</react_router_1.Link>
    </hovercard_1.default>);
};
exports.default = IssueLink;
var Title = styled_1.default('h3')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  margin: 0 0 ", ";\n  ", ";\n\n  em {\n    font-style: normal;\n    font-weight: 400;\n    color: ", ";\n    font-size: 90%;\n  }\n"], ["\n  font-size: ", ";\n  margin: 0 0 ", ";\n  ", ";\n\n  em {\n    font-style: normal;\n    font-weight: 400;\n    color: ", ";\n    font-size: 90%;\n  }\n"])), function (p) { return p.theme.fontSizeMedium; }, space_1.default(0.5), overflowEllipsis_1.default, function (p) { return p.theme.gray300; });
var Section = styled_1.default('section')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(2));
var Grid = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr 1fr;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 1fr 1fr;\n  grid-gap: ", ";\n"])), space_1.default(2));
var HovercardEventMessage = styled_1.default(eventMessage_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  font-size: 12px;\n"], ["\n  font-size: 12px;\n"])));
var GridHeader = styled_1.default('h5')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-size: 11px;\n  margin-bottom: ", ";\n  text-transform: uppercase;\n"], ["\n  color: ", ";\n  font-size: 11px;\n  margin-bottom: ", ";\n  text-transform: uppercase;\n"])), function (p) { return p.theme.gray300; }, space_1.default(0.5));
var StyledTimeSince = styled_1.default(timeSince_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  color: inherit;\n"], ["\n  color: inherit;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=issueLink.jsx.map