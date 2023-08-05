Object.defineProperty(exports, "__esModule", { value: true });
exports.CompactIssue = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var group_1 = require("app/actionCreators/group");
var indicator_1 = require("app/actionCreators/indicator");
var eventOrGroupTitle_1 = tslib_1.__importDefault(require("app/components/eventOrGroupTitle"));
var errorLevel_1 = tslib_1.__importDefault(require("app/components/events/errorLevel"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var panels_1 = require("app/components/panels");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var groupStore_1 = tslib_1.__importDefault(require("app/stores/groupStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var events_1 = require("app/utils/events");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var CompactIssueHeader = /** @class */ (function (_super) {
    tslib_1.__extends(CompactIssueHeader, _super);
    function CompactIssueHeader() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    CompactIssueHeader.prototype.render = function () {
        var _a = this.props, data = _a.data, organization = _a.organization, projectId = _a.projectId, eventId = _a.eventId;
        var basePath = "/organizations/" + organization.slug + "/issues/";
        var issueLink = eventId
            ? "/organizations/" + organization.slug + "/projects/" + projectId + "/events/" + eventId + "/"
            : "" + basePath + data.id + "/";
        var commentColor = data.subscriptionDetails && data.subscriptionDetails.reason === 'mentioned'
            ? 'success'
            : 'textColor';
        return (<react_1.Fragment>
        <IssueHeaderMetaWrapper>
          <StyledErrorLevel size="12px" level={data.level} title={data.level}/>
          <h3 className="truncate">
            <IconLink to={issueLink || ''}>
              {data.status === 'ignored' && <icons_1.IconMute size="xs"/>}
              {data.isBookmarked && <icons_1.IconStar isSolid size="xs"/>}
              <eventOrGroupTitle_1.default data={data}/>
            </IconLink>
          </h3>
        </IssueHeaderMetaWrapper>
        <div className="event-extra">
          <span className="project-name">
            <strong>{data.project.slug}</strong>
          </span>
          {data.numComments !== 0 && (<span>
              <IconLink to={"" + basePath + data.id + "/activity/"} className="comments">
                <icons_1.IconChat size="xs" color={commentColor}/>
                <span className="tag-count">{data.numComments}</span>
              </IconLink>
            </span>)}
          <span className="culprit">{events_1.getMessage(data)}</span>
        </div>
      </react_1.Fragment>);
    };
    return CompactIssueHeader;
}(react_1.Component));
/**
 * Type assertion to disambiguate GroupTypes
 *
 * The GroupCollapseRelease type isn't compatible with BaseGroup
 */
function isGroup(maybe) {
    return maybe.status !== undefined;
}
var CompactIssue = /** @class */ (function (_super) {
    tslib_1.__extends(CompactIssue, _super);
    function CompactIssue() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            issue: _this.props.data || groupStore_1.default.get(_this.props.id),
        };
        _this.listener = groupStore_1.default.listen(function (itemIds) { return _this.onGroupChange(itemIds); }, undefined);
        return _this;
    }
    CompactIssue.prototype.componentWillReceiveProps = function (nextProps) {
        if (nextProps.id !== this.props.id) {
            this.setState({
                issue: groupStore_1.default.get(this.props.id),
            });
        }
    };
    CompactIssue.prototype.componentWillUnmount = function () {
        this.listener();
    };
    CompactIssue.prototype.onGroupChange = function (itemIds) {
        if (!itemIds.has(this.props.id)) {
            return;
        }
        var id = this.props.id;
        var issue = groupStore_1.default.get(id);
        this.setState({
            issue: issue,
        });
    };
    CompactIssue.prototype.onUpdate = function (data) {
        var issue = this.state.issue;
        if (!issue) {
            return;
        }
        indicator_1.addLoadingMessage(locale_1.t('Saving changes\u2026'));
        group_1.bulkUpdate(this.props.api, {
            orgId: this.props.organization.slug,
            projectId: issue.project.slug,
            itemIds: [issue.id],
            data: data,
        }, {
            complete: function () {
                indicator_1.clearIndicators();
            },
        });
    };
    CompactIssue.prototype.render = function () {
        var issue = this.state.issue;
        var organization = this.props.organization;
        if (!isGroup(issue)) {
            return null;
        }
        var className = 'issue';
        if (issue.isBookmarked) {
            className += ' isBookmarked';
        }
        if (issue.hasSeen) {
            className += ' hasSeen';
        }
        if (issue.status === 'resolved') {
            className += ' isResolved';
        }
        if (issue.status === 'ignored') {
            className += ' isIgnored';
        }
        return (<IssueRow className={className}>
        <CompactIssueHeader data={issue} organization={organization} projectId={issue.project.slug} eventId={this.props.eventId}/>
        {this.props.children}
      </IssueRow>);
    };
    return CompactIssue;
}(react_1.Component));
exports.CompactIssue = CompactIssue;
exports.default = withApi_1.default(withOrganization_1.default(CompactIssue));
var IssueHeaderMetaWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var StyledErrorLevel = styled_1.default(errorLevel_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: block;\n  margin-right: ", ";\n"], ["\n  display: block;\n  margin-right: ", ";\n"])), space_1.default(1));
var IconLink = styled_1.default(link_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  & > svg {\n    margin-right: ", ";\n  }\n"], ["\n  & > svg {\n    margin-right: ", ";\n  }\n"])), space_1.default(0.5));
var IssueRow = styled_1.default(panels_1.PanelItem)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  padding-top: ", ";\n  padding-bottom: ", ";\n  flex-direction: column;\n"], ["\n  padding-top: ", ";\n  padding-bottom: ", ";\n  flex-direction: column;\n"])), space_1.default(1.5), space_1.default(0.75));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=compactIssue.jsx.map