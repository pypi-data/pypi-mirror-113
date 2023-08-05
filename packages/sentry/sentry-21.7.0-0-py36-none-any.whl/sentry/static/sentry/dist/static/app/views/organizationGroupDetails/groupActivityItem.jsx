Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var commitLink_1 = tslib_1.__importDefault(require("app/components/commitLink"));
var duration_1 = tslib_1.__importDefault(require("app/components/duration"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var pullRequestLink_1 = tslib_1.__importDefault(require("app/components/pullRequestLink"));
var version_1 = tslib_1.__importDefault(require("app/components/version"));
var locale_1 = require("app/locale");
var memberListStore_1 = tslib_1.__importDefault(require("app/stores/memberListStore"));
var teamStore_1 = tslib_1.__importDefault(require("app/stores/teamStore"));
var types_1 = require("app/types");
function GroupActivityItem(_a) {
    var activity = _a.activity, orgSlug = _a.orgSlug, projectId = _a.projectId, author = _a.author;
    var issuesLink = "/organizations/" + orgSlug + "/issues/";
    function getIgnoredMessage(data) {
        if (data.ignoreDuration) {
            return locale_1.tct('[author] ignored this issue for [duration]', {
                author: author,
                duration: <duration_1.default seconds={data.ignoreDuration * 60}/>,
            });
        }
        if (data.ignoreCount && data.ignoreWindow) {
            return locale_1.tct('[author] ignored this issue until it happens [count] time(s) in [duration]', {
                author: author,
                count: data.ignoreCount,
                duration: <duration_1.default seconds={data.ignoreWindow * 60}/>,
            });
        }
        if (data.ignoreCount) {
            return locale_1.tct('[author] ignored this issue until it happens [count] time(s)', {
                author: author,
                count: data.ignoreCount,
            });
        }
        if (data.ignoreUserCount && data.ignoreUserWindow) {
            return locale_1.tct('[author] ignored this issue until it affects [count] user(s) in [duration]', {
                author: author,
                count: data.ignoreUserCount,
                duration: <duration_1.default seconds={data.ignoreUserWindow * 60}/>,
            });
        }
        if (data.ignoreUserCount) {
            return locale_1.tct('[author] ignored this issue until it affects [count] user(s)', {
                author: author,
                count: data.ignoreUserCount,
            });
        }
        return locale_1.tct('[author] ignored this issue', { author: author });
    }
    function getAssignedMessage(data) {
        var assignee = undefined;
        if (data.assigneeType === 'team') {
            var team = teamStore_1.default.getById(data.assignee);
            assignee = team ? team.slug : '<unknown-team>';
            return locale_1.tct('[author] assigned this issue to #[assignee]', {
                author: author,
                assignee: assignee,
            });
        }
        if (activity.user && activity.assignee === activity.user.id) {
            return locale_1.tct('[author] assigned this issue to themselves', { author: author });
        }
        assignee = memberListStore_1.default.getById(data.assignee);
        if (typeof assignee === 'object' && (assignee === null || assignee === void 0 ? void 0 : assignee.email)) {
            return locale_1.tct('[author] assigned this issue to [assignee]', {
                author: author,
                assignee: assignee.email,
            });
        }
        return locale_1.tct('[author] assigned this issue to an unknown user', { author: author });
    }
    function renderContent() {
        var _a;
        switch (activity.type) {
            case types_1.GroupActivityType.NOTE:
                return locale_1.tct('[author] left a comment', { author: author });
            case types_1.GroupActivityType.SET_RESOLVED:
                return locale_1.tct('[author] marked this issue as resolved', { author: author });
            case types_1.GroupActivityType.SET_RESOLVED_BY_AGE:
                return locale_1.tct('[author] marked this issue as resolved due to inactivity', {
                    author: author,
                });
            case types_1.GroupActivityType.SET_RESOLVED_IN_RELEASE:
                return activity.data.version
                    ? locale_1.tct('[author] marked this issue as resolved in [version]', {
                        author: author,
                        version: (<version_1.default version={activity.data.version} projectId={projectId} tooltipRawVersion/>),
                    })
                    : locale_1.tct('[author] marked this issue as resolved in the upcoming release', {
                        author: author,
                    });
            case types_1.GroupActivityType.SET_RESOLVED_IN_COMMIT:
                return locale_1.tct('[author] marked this issue as resolved in [version]', {
                    author: author,
                    version: (<commitLink_1.default inline commitId={activity.data.commit.id} repository={activity.data.commit.repository}/>),
                });
            case types_1.GroupActivityType.SET_RESOLVED_IN_PULL_REQUEST: {
                var data = activity.data;
                var pullRequest = data.pullRequest;
                return locale_1.tct('[author] marked this issue as resolved in [version]', {
                    author: author,
                    version: (<pullRequestLink_1.default inline pullRequest={pullRequest} repository={pullRequest.repository}/>),
                });
            }
            case types_1.GroupActivityType.SET_UNRESOLVED:
                return locale_1.tct('[author] marked this issue as unresolved', { author: author });
            case types_1.GroupActivityType.SET_IGNORED: {
                var data = activity.data;
                return getIgnoredMessage(data);
            }
            case types_1.GroupActivityType.SET_PUBLIC:
                return locale_1.tct('[author] made this issue public', { author: author });
            case types_1.GroupActivityType.SET_PRIVATE:
                return locale_1.tct('[author] made this issue private', { author: author });
            case types_1.GroupActivityType.SET_REGRESSION: {
                var data = activity.data;
                return data.version
                    ? locale_1.tct('[author] marked this issue as a regression in [version]', {
                        author: author,
                        version: (<version_1.default version={data.version} projectId={projectId} tooltipRawVersion/>),
                    })
                    : locale_1.tct('[author] marked this issue as a regression', { author: author });
            }
            case types_1.GroupActivityType.CREATE_ISSUE: {
                var data = activity.data;
                return locale_1.tct('[author] created an issue on [provider] titled [title]', {
                    author: author,
                    provider: data.provider,
                    title: <externalLink_1.default href={data.location}>{data.title}</externalLink_1.default>,
                });
            }
            case types_1.GroupActivityType.UNMERGE_SOURCE: {
                var data = activity.data;
                var destination = data.destination, fingerprints = data.fingerprints;
                return locale_1.tn('%2$s migrated %1$s fingerprint to %3$s', '%2$s migrated %1$s fingerprints to %3$s', fingerprints.length, author, destination ? (<link_1.default to={"" + issuesLink + destination.id}>{destination.shortId}</link_1.default>) : (locale_1.t('a group')));
            }
            case types_1.GroupActivityType.UNMERGE_DESTINATION: {
                var data = activity.data;
                var source = data.source, fingerprints = data.fingerprints;
                return locale_1.tn('%2$s migrated %1$s fingerprint from %3$s', '%2$s migrated %1$s fingerprints from %3$s', fingerprints.length, author, source ? (<link_1.default to={"" + issuesLink + source.id}>{source.shortId}</link_1.default>) : (locale_1.t('a group')));
            }
            case types_1.GroupActivityType.FIRST_SEEN:
                return locale_1.tct('[author] first saw this issue', { author: author });
            case types_1.GroupActivityType.ASSIGNED: {
                var data = activity.data;
                return getAssignedMessage(data);
            }
            case types_1.GroupActivityType.UNASSIGNED:
                return locale_1.tct('[author] unassigned this issue', { author: author });
            case types_1.GroupActivityType.MERGE:
                return locale_1.tn('%2$s merged %1$s issue into this issue', '%2$s merged %1$s issues into this issue', activity.data.issues.length, author);
            case types_1.GroupActivityType.REPROCESS: {
                var data = activity.data;
                var oldGroupId = data.oldGroupId, eventCount = data.eventCount;
                return locale_1.tct('[author] reprocessed the events in this issue. [new-events]', (_a = {
                        author: author
                    },
                    _a['new-events'] = (<link_1.default to={"/organizations/" + orgSlug + "/issues/?query=reprocessing.original_issue_id:" + oldGroupId}>
              {locale_1.tn('See %s new event', 'See %s new events', eventCount)}
            </link_1.default>),
                    _a));
            }
            case types_1.GroupActivityType.MARK_REVIEWED: {
                return locale_1.tct('[author] marked this issue as reviewed', {
                    author: author,
                });
            }
            default:
                return ''; // should never hit (?)
        }
    }
    return <React.Fragment>{renderContent()}</React.Fragment>;
}
exports.default = GroupActivityItem;
//# sourceMappingURL=groupActivityItem.jsx.map