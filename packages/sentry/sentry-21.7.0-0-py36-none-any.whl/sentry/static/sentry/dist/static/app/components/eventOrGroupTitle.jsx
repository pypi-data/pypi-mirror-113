Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var guideAnchor_1 = tslib_1.__importDefault(require("app/components/assistant/guideAnchor"));
var projectsStore_1 = tslib_1.__importDefault(require("app/stores/projectsStore"));
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var events_1 = require("app/utils/events");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var eventTitleTreeLabel_1 = tslib_1.__importDefault(require("./eventTitleTreeLabel"));
var stacktracePreview_1 = tslib_1.__importDefault(require("./stacktracePreview"));
function EventOrGroupTitle(_a) {
    var _b;
    var _c = _a.guideAnchorName, guideAnchorName = _c === void 0 ? 'issue_title' : _c, organization = _a.organization, data = _a.data, withStackTracePreview = _a.withStackTracePreview, hasGuideAnchor = _a.hasGuideAnchor, className = _a.className;
    var event = data;
    var hasGroupingTreeUI = !!(organization === null || organization === void 0 ? void 0 : organization.features.includes('grouping-tree-ui'));
    var id = event.id, eventID = event.eventID, groupID = event.groupID, projectID = event.projectID;
    var _d = events_1.getTitle(event, organization === null || organization === void 0 ? void 0 : organization.features), title = _d.title, subtitle = _d.subtitle, treeLabel = _d.treeLabel;
    return (<Wrapper className={className} hasGroupingTreeUI={hasGroupingTreeUI}>
      <guideAnchor_1.default disabled={!hasGuideAnchor} target={guideAnchorName} position="bottom">
        <StyledStacktracePreview organization={organization} issueId={groupID ? groupID : id} 
    // we need eventId and projectSlug only when hovering over Event, not Group
    // (different API call is made to get the stack trace then)
    eventId={eventID} projectSlug={eventID ? (_b = projectsStore_1.default.getById(projectID)) === null || _b === void 0 ? void 0 : _b.slug : undefined} disablePreview={!withStackTracePreview} hasGroupingTreeUI={hasGroupingTreeUI}>
          {treeLabel ? <eventTitleTreeLabel_1.default treeLabel={treeLabel}/> : title}
        </StyledStacktracePreview>
      </guideAnchor_1.default>
      {subtitle && (<react_1.Fragment>
          <Spacer />
          <Subtitle title={subtitle}>{subtitle}</Subtitle>
          <br />
        </react_1.Fragment>)}
    </Wrapper>);
}
exports.default = withOrganization_1.default(EventOrGroupTitle);
/**
 * &nbsp; is used instead of margin/padding to split title and subtitle
 * into 2 separate text nodes on the HTML AST. This allows the
 * title to be highlighted without spilling over to the subtitle.
 */
var Spacer = function () { return <span style={{ display: 'inline-block', width: 10 }}>&nbsp;</span>; };
var Subtitle = styled_1.default('em')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-style: normal;\n"], ["\n  color: ", ";\n  font-style: normal;\n"])), function (p) { return p.theme.gray300; });
var StyledStacktracePreview = styled_1.default(stacktracePreview_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), function (p) {
    return p.hasGroupingTreeUI &&
        "\n      display: inline-flex;\n      > span:first-child {\n        display: inline-flex;\n      }\n    ";
});
var Wrapper = styled_1.default('span')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), function (p) {
    return p.hasGroupingTreeUI &&
        "\n\n      display: inline-grid;\n      grid-template-columns: auto max-content 1fr max-content;\n      align-items: flex-end;\n      line-height: 100%;\n\n      " + Subtitle + " {\n        " + overflowEllipsis_1.default + ";\n        display: inline-block;\n      }\n    ";
});
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=eventOrGroupTitle.jsx.map