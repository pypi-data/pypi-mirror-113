Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var guideAnchor_1 = tslib_1.__importDefault(require("app/components/assistant/guideAnchor"));
var eventAnnotation_1 = tslib_1.__importDefault(require("app/components/events/eventAnnotation"));
var inboxReason_1 = tslib_1.__importDefault(require("app/components/group/inboxBadges/inboxReason"));
var shortId_1 = tslib_1.__importDefault(require("app/components/group/inboxBadges/shortId"));
var timesTag_1 = tslib_1.__importDefault(require("app/components/group/inboxBadges/timesTag"));
var unhandledTag_1 = tslib_1.__importDefault(require("app/components/group/inboxBadges/unhandledTag"));
var projectBadge_1 = tslib_1.__importDefault(require("app/components/idBadge/projectBadge"));
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
function EventOrGroupExtraDetails(_a) {
    var data = _a.data, showAssignee = _a.showAssignee, params = _a.params, hasGuideAnchor = _a.hasGuideAnchor, showInboxTime = _a.showInboxTime;
    var _b = data, id = _b.id, lastSeen = _b.lastSeen, firstSeen = _b.firstSeen, subscriptionDetails = _b.subscriptionDetails, numComments = _b.numComments, logger = _b.logger, assignedTo = _b.assignedTo, annotations = _b.annotations, shortId = _b.shortId, project = _b.project, lifetime = _b.lifetime, isUnhandled = _b.isUnhandled, inbox = _b.inbox;
    var issuesPath = "/organizations/" + params.orgId + "/issues/";
    var inboxReason = inbox && (<inboxReason_1.default inbox={inbox} showDateAdded={showInboxTime}/>);
    return (<GroupExtra>
      {inbox && (<guideAnchor_1.default target="inbox_guide_reason" disabled={!hasGuideAnchor}>
          {inboxReason}
        </guideAnchor_1.default>)}
      {shortId && (<shortId_1.default shortId={shortId} avatar={project && (<ShadowlessProjectBadge project={project} avatarSize={12} hideName/>)}/>)}
      {isUnhandled && <unhandledTag_1.default />}
      {!lifetime && !firstSeen && !lastSeen ? (<placeholder_1.default height="14px" width="100px"/>) : (<timesTag_1.default lastSeen={(lifetime === null || lifetime === void 0 ? void 0 : lifetime.lastSeen) || lastSeen} firstSeen={(lifetime === null || lifetime === void 0 ? void 0 : lifetime.firstSeen) || firstSeen}/>)}
      {/* Always display comment count on inbox */}
      {numComments > 0 && (<CommentsLink to={"" + issuesPath + id + "/activity/"} className="comments">
          <icons_1.IconChat size="xs" color={(subscriptionDetails === null || subscriptionDetails === void 0 ? void 0 : subscriptionDetails.reason) === 'mentioned' ? 'green300' : undefined}/>
          <span>{numComments}</span>
        </CommentsLink>)}
      {logger && (<LoggerAnnotation>
          <react_router_1.Link to={{
                pathname: issuesPath,
                query: {
                    query: "logger:" + logger,
                },
            }}>
            {logger}
          </react_router_1.Link>
        </LoggerAnnotation>)}
      {annotations === null || annotations === void 0 ? void 0 : annotations.map(function (annotation, key) { return (<AnnotationNoMargin dangerouslySetInnerHTML={{
                __html: annotation,
            }} key={key}/>); })}

      {showAssignee && assignedTo && (<div>{locale_1.tct('Assigned to [name]', { name: assignedTo.name })}</div>)}
    </GroupExtra>);
}
var GroupExtra = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: inline-grid;\n  grid-auto-flow: column dense;\n  grid-gap: ", ";\n  justify-content: start;\n  align-items: center;\n  color: ", ";\n  font-size: ", ";\n  position: relative;\n  min-width: 500px;\n  white-space: nowrap;\n\n  a {\n    color: inherit;\n  }\n"], ["\n  display: inline-grid;\n  grid-auto-flow: column dense;\n  grid-gap: ", ";\n  justify-content: start;\n  align-items: center;\n  color: ", ";\n  font-size: ", ";\n  position: relative;\n  min-width: 500px;\n  white-space: nowrap;\n\n  a {\n    color: inherit;\n  }\n"])), space_1.default(1.5), function (p) { return p.theme.textColor; }, function (p) { return p.theme.fontSizeSmall; });
var ShadowlessProjectBadge = styled_1.default(projectBadge_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  * > img {\n    box-shadow: none;\n  }\n"], ["\n  * > img {\n    box-shadow: none;\n  }\n"])));
var CommentsLink = styled_1.default(react_router_1.Link)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: inline-grid;\n  grid-gap: ", ";\n  align-items: center;\n  grid-auto-flow: column;\n  color: ", ";\n"], ["\n  display: inline-grid;\n  grid-gap: ", ";\n  align-items: center;\n  grid-auto-flow: column;\n  color: ", ";\n"])), space_1.default(0.5), function (p) { return p.theme.textColor; });
var AnnotationNoMargin = styled_1.default(eventAnnotation_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin-left: 0;\n  padding-left: 0;\n  border-left: none;\n  & > a {\n    color: ", ";\n  }\n"], ["\n  margin-left: 0;\n  padding-left: 0;\n  border-left: none;\n  & > a {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.textColor; });
var LoggerAnnotation = styled_1.default(AnnotationNoMargin)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.textColor; });
exports.default = react_router_1.withRouter(EventOrGroupExtraDetails);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=eventOrGroupExtraDetails.jsx.map