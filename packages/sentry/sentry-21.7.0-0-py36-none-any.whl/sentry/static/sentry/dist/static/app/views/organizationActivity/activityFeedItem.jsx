Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var avatar_1 = tslib_1.__importDefault(require("app/components/activity/item/avatar"));
var commitLink_1 = tslib_1.__importDefault(require("app/components/commitLink"));
var duration_1 = tslib_1.__importDefault(require("app/components/duration"));
var issueLink_1 = tslib_1.__importDefault(require("app/components/issueLink"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var pullRequestLink_1 = tslib_1.__importDefault(require("app/components/pullRequestLink"));
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var version_1 = tslib_1.__importDefault(require("app/components/version"));
var versionHoverCard_1 = tslib_1.__importDefault(require("app/components/versionHoverCard"));
var locale_1 = require("app/locale");
var memberListStore_1 = tslib_1.__importDefault(require("app/stores/memberListStore"));
var teamStore_1 = tslib_1.__importDefault(require("app/stores/teamStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var marked_1 = tslib_1.__importDefault(require("app/utils/marked"));
var defaultProps = {
    defaultClipped: false,
    clipHeight: 68,
};
var ActivityItem = /** @class */ (function (_super) {
    tslib_1.__extends(ActivityItem, _super);
    function ActivityItem() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            clipped: _this.props.defaultClipped,
        };
        _this.activityBubbleRef = react_1.createRef();
        _this.formatProjectActivity = function (author, item) {
            var data = item.data;
            var organization = _this.props.organization;
            var orgId = organization.slug;
            var project = item.project;
            var issue = item.issue;
            var basePath = "/organizations/" + orgId + "/issues/";
            var issueLink = issue ? (<issueLink_1.default orgId={orgId} issue={issue} to={"" + basePath + issue.id + "/"} card>
        {issue.shortId}
      </issueLink_1.default>) : null;
            var versionLink = data.version ? (<versionHoverCard_1.default organization={organization} projectSlug={project.slug} releaseVersion={data.version}>
        <version_1.default version={data.version} projectId={project.id}/>
      </versionHoverCard_1.default>) : null;
            switch (item.type) {
                case 'note':
                    return locale_1.tct('[author] commented on [issue]', {
                        author: author,
                        issue: (<issueLink_1.default card orgId={orgId} issue={issue} to={"" + basePath + issue.id + "/activity/#event_" + item.id}>
              {issue.shortId}
            </issueLink_1.default>),
                    });
                case 'set_resolved':
                    return locale_1.tct('[author] marked [issue] as resolved', {
                        author: author,
                        issue: issueLink,
                    });
                case 'set_resolved_by_age':
                    return locale_1.tct('[author] marked [issue] as resolved due to age', {
                        author: author,
                        issue: issueLink,
                    });
                case 'set_resolved_in_release':
                    if (data.version) {
                        return locale_1.tct('[author] marked [issue] as resolved in [version]', {
                            author: author,
                            version: versionLink,
                            issue: issueLink,
                        });
                    }
                    return locale_1.tct('[author] marked [issue] as resolved in the upcoming release', {
                        author: author,
                        issue: issueLink,
                    });
                case 'set_resolved_in_commit':
                    return locale_1.tct('[author] marked [issue] as resolved in [version]', {
                        author: author,
                        version: (<commitLink_1.default inline commitId={data.commit && data.commit.id} repository={data.commit && data.commit.repository}/>),
                        issue: issueLink,
                    });
                case 'set_resolved_in_pull_request':
                    return locale_1.tct('[author] marked [issue] as resolved in [version]', {
                        author: author,
                        version: (<pullRequestLink_1.default inline pullRequest={data.pullRequest} repository={data.pullRequest && data.pullRequest.repository}/>),
                        issue: issueLink,
                    });
                case 'set_unresolved':
                    return locale_1.tct('[author] marked [issue] as unresolved', {
                        author: author,
                        issue: issueLink,
                    });
                case 'set_ignored':
                    if (data.ignoreDuration) {
                        return locale_1.tct('[author] ignored [issue] for [duration]', {
                            author: author,
                            duration: <duration_1.default seconds={data.ignoreDuration * 60}/>,
                            issue: issueLink,
                        });
                    }
                    else if (data.ignoreCount && data.ignoreWindow) {
                        return locale_1.tct('[author] ignored [issue] until it happens [count] time(s) in [duration]', {
                            author: author,
                            count: data.ignoreCount,
                            duration: <duration_1.default seconds={data.ignoreWindow * 60}/>,
                            issue: issueLink,
                        });
                    }
                    else if (data.ignoreCount) {
                        return locale_1.tct('[author] ignored [issue] until it happens [count] time(s)', {
                            author: author,
                            count: data.ignoreCount,
                            issue: issueLink,
                        });
                    }
                    else if (data.ignoreUserCount && data.ignoreUserWindow) {
                        return locale_1.tct('[author] ignored [issue] until it affects [count] user(s) in [duration]', {
                            author: author,
                            count: data.ignoreUserCount,
                            duration: <duration_1.default seconds={data.ignoreUserWindow * 60}/>,
                            issue: issueLink,
                        });
                    }
                    else if (data.ignoreUserCount) {
                        return locale_1.tct('[author] ignored [issue] until it affects [count] user(s)', {
                            author: author,
                            count: data.ignoreUserCount,
                            issue: issueLink,
                        });
                    }
                    return locale_1.tct('[author] ignored [issue]', {
                        author: author,
                        issue: issueLink,
                    });
                case 'set_public':
                    return locale_1.tct('[author] made [issue] public', {
                        author: author,
                        issue: issueLink,
                    });
                case 'set_private':
                    return locale_1.tct('[author] made [issue] private', {
                        author: author,
                        issue: issueLink,
                    });
                case 'set_regression':
                    if (data.version) {
                        return locale_1.tct('[author] marked [issue] as a regression in [version]', {
                            author: author,
                            version: versionLink,
                            issue: issueLink,
                        });
                    }
                    return locale_1.tct('[author] marked [issue] as a regression', {
                        author: author,
                        issue: issueLink,
                    });
                case 'create_issue':
                    return locale_1.tct('[author] linked [issue] on [provider]', {
                        author: author,
                        provider: data.provider,
                        issue: issueLink,
                    });
                case 'unmerge_destination':
                    return locale_1.tn('%2$s migrated %1$s fingerprint from %3$s to %4$s', '%2$s migrated %1$s fingerprints from %3$s to %4$s', data.fingerprints.length, author, data.source ? (<a href={"" + basePath + data.source.id}>{data.source.shortId}</a>) : (locale_1.t('a group')), issueLink);
                case 'first_seen':
                    return locale_1.tct('[author] saw [link:issue]', {
                        author: author,
                        issue: issueLink,
                    });
                case 'assigned':
                    var assignee = void 0;
                    if (data.assigneeType === 'team') {
                        var team = teamStore_1.default.getById(data.assignee);
                        assignee = team ? team.slug : '<unknown-team>';
                        return locale_1.tct('[author] assigned [issue] to #[assignee]', {
                            author: author,
                            issue: issueLink,
                            assignee: assignee,
                        });
                    }
                    if (item.user && data.assignee === item.user.id) {
                        return locale_1.tct('[author] assigned [issue] to themselves', {
                            author: author,
                            issue: issueLink,
                        });
                    }
                    assignee = memberListStore_1.default.getById(data.assignee);
                    if (assignee && assignee.email) {
                        return locale_1.tct('[author] assigned [issue] to [assignee]', {
                            author: author,
                            assignee: <span title={assignee.email}>{assignee.name}</span>,
                            issue: issueLink,
                        });
                    }
                    else if (data.assigneeEmail) {
                        return locale_1.tct('[author] assigned [issue] to [assignee]', {
                            author: author,
                            assignee: data.assigneeEmail,
                            issue: issueLink,
                        });
                    }
                    return locale_1.tct('[author] assigned [issue] to an [help:unknown user]', {
                        author: author,
                        help: <span title={data.assignee}/>,
                        issue: issueLink,
                    });
                case 'unassigned':
                    return locale_1.tct('[author] unassigned [issue]', {
                        author: author,
                        issue: issueLink,
                    });
                case 'merge':
                    return locale_1.tct('[author] merged [count] [link:issues]', {
                        author: author,
                        count: data.issues.length + 1,
                        link: <react_router_1.Link to={"" + basePath + issue.id + "/"}/>,
                    });
                case 'release':
                    return locale_1.tct('[author] released version [version]', {
                        author: author,
                        version: versionLink,
                    });
                case 'deploy':
                    return locale_1.tct('[author] deployed version [version] to [environment].', {
                        author: author,
                        version: versionLink,
                        environment: data.environment || 'Default Environment',
                    });
                case 'mark_reviewed':
                    return locale_1.tct('[author] marked [issue] as reviewed', {
                        author: author,
                        issue: issueLink,
                    });
                default:
                    return ''; // should never hit (?)
            }
        };
        return _this;
    }
    ActivityItem.prototype.componentDidMount = function () {
        if (this.activityBubbleRef.current) {
            var bubbleHeight = this.activityBubbleRef.current.offsetHeight;
            if (bubbleHeight > this.props.clipHeight) {
                // okay if this causes re-render; cannot determine until
                // rendered first anyways
                // eslint-disable-next-line react/no-did-mount-set-state
                this.setState({ clipped: true });
            }
        }
    };
    ActivityItem.prototype.render = function () {
        var _a;
        var _b = this.props, className = _b.className, item = _b.item;
        var avatar = (<avatar_1.default type={!item.user ? 'system' : 'user'} user={(_a = item.user) !== null && _a !== void 0 ? _a : undefined} size={36}/>);
        var author = {
            name: item.user ? item.user.name : 'Sentry',
            avatar: avatar,
        };
        var hasBubble = ['note', 'create_issue'].includes(item.type);
        var bubbleProps = tslib_1.__assign(tslib_1.__assign({}, (item.type === 'note'
            ? { dangerouslySetInnerHTML: { __html: marked_1.default(item.data.text) } }
            : {})), (item.type === 'create_issue'
            ? {
                children: (<externalLink_1.default href={item.data.location}>{item.data.title}</externalLink_1.default>),
            }
            : {}));
        return (<div className={className}>
        {author.avatar}
        <div>
          {this.formatProjectActivity(<span>
              <ActivityAuthor>{author.name}</ActivityAuthor>
            </span>, item)}
          {hasBubble && (<Bubble ref={this.activityBubbleRef} clipped={this.state.clipped} {...bubbleProps}/>)}
          <Meta>
            <Project>{item.project.slug}</Project>
            <StyledTimeSince date={item.dateCreated}/>
          </Meta>
        </div>
      </div>);
    };
    ActivityItem.defaultProps = defaultProps;
    return ActivityItem;
}(react_1.Component));
exports.default = styled_1.default(ActivityItem)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: max-content auto;\n  position: relative;\n  margin: 0;\n  padding: ", ";\n  border-bottom: 1px solid ", ";\n  line-height: 1.4;\n  font-size: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: max-content auto;\n  position: relative;\n  margin: 0;\n  padding: ", ";\n  border-bottom: 1px solid ", ";\n  line-height: 1.4;\n  font-size: ", ";\n"])), space_1.default(1), space_1.default(1), function (p) { return p.theme.innerBorder; }, function (p) { return p.theme.fontSizeMedium; });
var ActivityAuthor = styled_1.default('span')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  font-weight: 600;\n"], ["\n  font-weight: 600;\n"])));
var Meta = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n"], ["\n  color: ", ";\n  font-size: ", ";\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.fontSizeRelativeSmall; });
var Project = styled_1.default('span')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  font-weight: bold;\n"], ["\n  font-weight: bold;\n"])));
var Bubble = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  background: ", ";\n  margin: ", " 0;\n  padding: ", " ", ";\n  border: 1px solid ", ";\n  border-radius: 3px;\n  box-shadow: 0 1px 1px rgba(0, 0, 0, 0.04);\n  position: relative;\n  overflow: hidden;\n\n  a {\n    max-width: 100%;\n    overflow-x: hidden;\n    text-overflow: ellipsis;\n  }\n\n  p {\n    &:last-child {\n      margin-bottom: 0;\n    }\n  }\n\n  ", "\n"], ["\n  background: ", ";\n  margin: ", " 0;\n  padding: ", " ", ";\n  border: 1px solid ", ";\n  border-radius: 3px;\n  box-shadow: 0 1px 1px rgba(0, 0, 0, 0.04);\n  position: relative;\n  overflow: hidden;\n\n  a {\n    max-width: 100%;\n    overflow-x: hidden;\n    text-overflow: ellipsis;\n  }\n\n  p {\n    &:last-child {\n      margin-bottom: 0;\n    }\n  }\n\n  ", "\n"])), function (p) { return p.theme.backgroundSecondary; }, space_1.default(0.5), space_1.default(1), space_1.default(2), function (p) { return p.theme.border; }, function (p) {
    return p.clipped &&
        "\n    max-height: 68px;\n\n    &:after {\n      position: absolute;\n      content: '';\n      display: block;\n      bottom: 0;\n      right: 0;\n      left: 0;\n      height: 36px;\n      background-image: linear-gradient(180deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 1));\n      border-bottom: 6px solid #fff;\n      border-radius: 0 0 3px 3px;\n      pointer-events: none;\n    }\n  ";
});
var StyledTimeSince = styled_1.default(timeSince_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  padding-left: ", ";\n"], ["\n  color: ", ";\n  padding-left: ", ";\n"])), function (p) { return p.theme.gray300; }, space_1.default(1));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=activityFeedItem.jsx.map