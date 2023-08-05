Object.defineProperty(exports, "__esModule", { value: true });
exports.TAB = exports.GroupHeader = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var omit_1 = tslib_1.__importDefault(require("lodash/omit"));
var members_1 = require("app/actionCreators/members");
var assigneeSelector_1 = tslib_1.__importDefault(require("app/components/assigneeSelector"));
var guideAnchor_1 = tslib_1.__importDefault(require("app/components/assistant/guideAnchor"));
var badge_1 = tslib_1.__importDefault(require("app/components/badge"));
var count_1 = tslib_1.__importDefault(require("app/components/count"));
var eventOrGroupTitle_1 = tslib_1.__importDefault(require("app/components/eventOrGroupTitle"));
var errorLevel_1 = tslib_1.__importDefault(require("app/components/events/errorLevel"));
var eventAnnotation_1 = tslib_1.__importDefault(require("app/components/events/eventAnnotation"));
var eventMessage_1 = tslib_1.__importDefault(require("app/components/events/eventMessage"));
var inboxReason_1 = tslib_1.__importDefault(require("app/components/group/inboxBadges/inboxReason"));
var unhandledTag_1 = tslib_1.__importDefault(require("app/components/group/inboxBadges/unhandledTag"));
var projectBadge_1 = tslib_1.__importDefault(require("app/components/idBadge/projectBadge"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var listLink_1 = tslib_1.__importDefault(require("app/components/links/listLink"));
var navTabs_1 = tslib_1.__importDefault(require("app/components/navTabs"));
var seenByList_1 = tslib_1.__importDefault(require("app/components/seenByList"));
var shortId_1 = tslib_1.__importDefault(require("app/components/shortId"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var events_1 = require("app/utils/events");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var actions_1 = tslib_1.__importDefault(require("./actions"));
var unhandledTag_2 = require("./unhandledTag");
var utils_1 = require("./utils");
var TAB = {
    DETAILS: 'details',
    ACTIVITY: 'activity',
    USER_FEEDBACK: 'user-feedback',
    ATTACHMENTS: 'attachments',
    TAGS: 'tags',
    EVENTS: 'events',
    MERGED: 'merged',
    GROUPING: 'grouping',
    SIMILAR_ISSUES: 'similar-issues',
};
exports.TAB = TAB;
var GroupHeader = /** @class */ (function (_super) {
    tslib_1.__extends(GroupHeader, _super);
    function GroupHeader() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {};
        return _this;
    }
    GroupHeader.prototype.componentDidMount = function () {
        var _this = this;
        var _a = this.props, group = _a.group, api = _a.api, organization = _a.organization;
        var project = group.project;
        members_1.fetchOrgMembers(api, organization.slug, [project.id]).then(function (memberList) {
            var users = memberList.map(function (member) { return member.user; });
            _this.setState({ memberList: users });
        });
    };
    GroupHeader.prototype.getDisabledTabs = function () {
        var organization = this.props.organization;
        var hasReprocessingV2Feature = organization.features.includes('reprocessing-v2');
        if (!hasReprocessingV2Feature) {
            return [];
        }
        var groupReprocessingStatus = this.props.groupReprocessingStatus;
        if (groupReprocessingStatus === utils_1.ReprocessingStatus.REPROCESSING) {
            return [
                TAB.ACTIVITY,
                TAB.USER_FEEDBACK,
                TAB.ATTACHMENTS,
                TAB.EVENTS,
                TAB.MERGED,
                TAB.GROUPING,
                TAB.SIMILAR_ISSUES,
                TAB.TAGS,
            ];
        }
        if (groupReprocessingStatus === utils_1.ReprocessingStatus.REPROCESSED_AND_HASNT_EVENT) {
            return [
                TAB.DETAILS,
                TAB.ATTACHMENTS,
                TAB.EVENTS,
                TAB.MERGED,
                TAB.GROUPING,
                TAB.SIMILAR_ISSUES,
                TAB.TAGS,
                TAB.USER_FEEDBACK,
            ];
        }
        return [];
    };
    GroupHeader.prototype.render = function () {
        var _a = this.props, project = _a.project, group = _a.group, currentTab = _a.currentTab, baseUrl = _a.baseUrl, event = _a.event, organization = _a.organization, location = _a.location;
        var projectFeatures = new Set(project ? project.features : []);
        var organizationFeatures = new Set(organization ? organization.features : []);
        var userCount = group.userCount;
        var hasGroupingTreeUI = organizationFeatures.has('grouping-tree-ui');
        var hasSimilarView = projectFeatures.has('similarity-view');
        var hasEventAttachments = organizationFeatures.has('event-attachments');
        var className = 'group-detail';
        if (group.hasSeen) {
            className += ' hasSeen';
        }
        if (group.status === 'resolved') {
            className += ' isResolved';
        }
        var memberList = this.state.memberList;
        var orgId = organization.slug;
        var message = events_1.getMessage(group);
        var searchTermWithoutQuery = omit_1.default(location.query, 'query');
        var eventRouteToObject = {
            pathname: baseUrl + "events/",
            query: searchTermWithoutQuery,
        };
        var disabledTabs = this.getDisabledTabs();
        var disableActions = !!disabledTabs.length;
        return (<div className={className}>
        <div className="row">
          <div className="col-sm-7">
            <TitleWrapper>
              <h3>
                <eventOrGroupTitle_1.default hasGuideAnchor data={group}/>
              </h3>
              {group.inbox && (<InboxReasonWrapper>
                  <inboxReason_1.default inbox={group.inbox} fontSize="md"/>
                </InboxReasonWrapper>)}
            </TitleWrapper>
            <StyledTagAndMessageWrapper>
              {group.level && <errorLevel_1.default level={group.level} size="11px"/>}
              {group.isUnhandled && <unhandledTag_1.default />}
              <eventMessage_1.default message={message} annotations={<React.Fragment>
                    {group.logger && (<EventAnnotationWithSpace>
                        <link_1.default to={{
                        pathname: "/organizations/" + orgId + "/issues/",
                        query: { query: 'logger:' + group.logger },
                    }}>
                          {group.logger}
                        </link_1.default>
                      </EventAnnotationWithSpace>)}
                    {group.annotations.map(function (annotation, i) { return (<EventAnnotationWithSpace key={i} dangerouslySetInnerHTML={{ __html: annotation }}/>); })}
                  </React.Fragment>}/>
            </StyledTagAndMessageWrapper>
          </div>

          <div className="col-sm-5 stats">
            <div className="flex flex-justify-right">
              {group.shortId && (<guideAnchor_1.default target="issue_number" position="bottom">
                  <div className="short-id-box count align-right">
                    <h6 className="nav-header">
                      <tooltip_1.default className="help-link" title={locale_1.t('This identifier is unique across your organization, and can be used to reference an issue in various places, like commit messages.')} position="bottom">
                        <externalLink_1.default href="https://docs.sentry.io/product/integrations/github/#resolve-via-commit-or-pull-request">
                          {locale_1.t('Issue #')}
                        </externalLink_1.default>
                      </tooltip_1.default>
                    </h6>
                    <shortId_1.default shortId={group.shortId} avatar={<StyledProjectBadge project={project} avatarSize={20} hideName/>}/>
                  </div>
                </guideAnchor_1.default>)}
              <div className="count align-right m-l-1">
                <h6 className="nav-header">{locale_1.t('Events')}</h6>
                {disableActions ? (<count_1.default className="count" value={group.count}/>) : (<link_1.default to={eventRouteToObject}>
                    <count_1.default className="count" value={group.count}/>
                  </link_1.default>)}
              </div>
              <div className="count align-right m-l-1">
                <h6 className="nav-header">{locale_1.t('Users')}</h6>
                {userCount !== 0 ? (disableActions ? (<count_1.default className="count" value={userCount}/>) : (<link_1.default to={baseUrl + "tags/user/" + location.search}>
                      <count_1.default className="count" value={userCount}/>
                    </link_1.default>)) : (<span>0</span>)}
              </div>
              <div className="assigned-to m-l-1">
                <h6 className="nav-header">{locale_1.t('Assignee')}</h6>
                <assigneeSelector_1.default id={group.id} memberList={memberList} disabled={disableActions}/>
              </div>
            </div>
          </div>
        </div>
        <seenByList_1.default seenBy={group.seenBy} iconTooltip={locale_1.t('People who have viewed this issue')}/>
        <actions_1.default group={group} project={project} disabled={disableActions} event={event}/>
        <navTabs_1.default>
          <listLink_1.default to={"" + baseUrl + location.search} isActive={function () { return currentTab === TAB.DETAILS; }} disabled={disabledTabs.includes(TAB.DETAILS)}>
            {locale_1.t('Details')}
          </listLink_1.default>
          <StyledListLink to={baseUrl + "activity/" + location.search} isActive={function () { return currentTab === TAB.ACTIVITY; }} disabled={disabledTabs.includes(TAB.ACTIVITY)}>
            {locale_1.t('Activity')}
            <badge_1.default>
              {group.numComments}
              <icons_1.IconChat size="xs"/>
            </badge_1.default>
          </StyledListLink>
          <StyledListLink to={baseUrl + "feedback/" + location.search} isActive={function () { return currentTab === TAB.USER_FEEDBACK; }} disabled={disabledTabs.includes(TAB.USER_FEEDBACK)}>
            {locale_1.t('User Feedback')} <badge_1.default text={group.userReportCount}/>
          </StyledListLink>
          {hasEventAttachments && (<listLink_1.default to={baseUrl + "attachments/" + location.search} isActive={function () { return currentTab === TAB.ATTACHMENTS; }} disabled={disabledTabs.includes(TAB.ATTACHMENTS)}>
              {locale_1.t('Attachments')}
            </listLink_1.default>)}
          <listLink_1.default to={baseUrl + "tags/" + location.search} isActive={function () { return currentTab === TAB.TAGS; }} disabled={disabledTabs.includes(TAB.TAGS)}>
            {locale_1.t('Tags')}
          </listLink_1.default>
          <listLink_1.default to={eventRouteToObject} isActive={function () { return currentTab === TAB.EVENTS; }} disabled={disabledTabs.includes(TAB.EVENTS)}>
            {locale_1.t('Events')}
          </listLink_1.default>
          <listLink_1.default to={baseUrl + "merged/" + location.search} isActive={function () { return currentTab === TAB.MERGED; }} disabled={disabledTabs.includes(TAB.MERGED)}>
            {locale_1.t('Merged Issues')}
          </listLink_1.default>
          {hasGroupingTreeUI && (<listLink_1.default to={baseUrl + "grouping/" + location.search} isActive={function () { return currentTab === TAB.GROUPING; }} disabled={disabledTabs.includes(TAB.GROUPING)}>
              {locale_1.t('Grouping')}
            </listLink_1.default>)}
          {hasSimilarView && (<listLink_1.default to={baseUrl + "similar/" + location.search} isActive={function () { return currentTab === TAB.SIMILAR_ISSUES; }} disabled={disabledTabs.includes(TAB.SIMILAR_ISSUES)}>
              {locale_1.t('Similar Issues')}
            </listLink_1.default>)}
        </navTabs_1.default>
      </div>);
    };
    return GroupHeader;
}(React.Component));
exports.GroupHeader = GroupHeader;
exports.default = withApi_1.default(react_router_1.withRouter(withOrganization_1.default(GroupHeader)));
var TitleWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  line-height: 24px;\n"], ["\n  display: flex;\n  line-height: 24px;\n"])));
var InboxReasonWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space_1.default(1));
var StyledTagAndMessageWrapper = styled_1.default(unhandledTag_2.TagAndMessageWrapper)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  gap: ", ";\n  justify-content: flex-start;\n  line-height: 1.2;\n\n  @media (max-width: ", ") {\n    margin-bottom: ", ";\n  }\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  gap: ", ";\n  justify-content: flex-start;\n  line-height: 1.2;\n\n  @media (max-width: ", ") {\n    margin-bottom: ", ";\n  }\n"])), space_1.default(1), function (p) { return p.theme.breakpoints[0]; }, space_1.default(2));
var StyledListLink = styled_1.default(listLink_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  svg {\n    margin-left: ", ";\n    margin-bottom: ", ";\n    vertical-align: middle;\n  }\n"], ["\n  svg {\n    margin-left: ", ";\n    margin-bottom: ", ";\n    vertical-align: middle;\n  }\n"])), space_1.default(0.5), space_1.default(0.25));
var StyledProjectBadge = styled_1.default(projectBadge_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  flex-shrink: 0;\n"], ["\n  flex-shrink: 0;\n"])));
var EventAnnotationWithSpace = styled_1.default(eventAnnotation_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space_1.default(1));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=header.jsx.map