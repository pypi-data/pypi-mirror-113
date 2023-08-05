Object.defineProperty(exports, "__esModule", { value: true });
exports.Actions = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var group_1 = require("app/actionCreators/group");
var indicator_1 = require("app/actionCreators/indicator");
var modal_1 = require("app/actionCreators/modal");
var groupActions_1 = tslib_1.__importDefault(require("app/actions/groupActions"));
var button_1 = tslib_1.__importDefault(require("app/components/actions/button"));
var ignore_1 = tslib_1.__importDefault(require("app/components/actions/ignore"));
var resolve_1 = tslib_1.__importDefault(require("app/components/actions/resolve"));
var guideAnchor_1 = tslib_1.__importDefault(require("app/components/assistant/guideAnchor"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var iconRefresh_1 = require("app/icons/iconRefresh");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var eventView_1 = tslib_1.__importDefault(require("app/utils/discover/eventView"));
var displayReprocessEventAction_1 = require("app/utils/displayReprocessEventAction");
var guid_1 = require("app/utils/guid");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var reviewAction_1 = tslib_1.__importDefault(require("app/views/issueList/actions/reviewAction"));
var shareIssue_1 = tslib_1.__importDefault(require("app/views/organizationGroupDetails/actions/shareIssue"));
var deleteAction_1 = tslib_1.__importDefault(require("./deleteAction"));
var subscribeAction_1 = tslib_1.__importDefault(require("./subscribeAction"));
var Actions = /** @class */ (function (_super) {
    tslib_1.__extends(Actions, _super);
    function Actions() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            shareBusy: false,
        };
        _this.onDelete = function () {
            var _a = _this.props, group = _a.group, project = _a.project, organization = _a.organization, api = _a.api;
            indicator_1.addLoadingMessage(locale_1.t('Delete event\u2026'));
            group_1.bulkDelete(api, {
                orgId: organization.slug,
                projectId: project.slug,
                itemIds: [group.id],
            }, {
                complete: function () {
                    indicator_1.clearIndicators();
                    react_router_1.browserHistory.push("/" + organization.slug + "/" + project.slug + "/");
                },
            });
        };
        _this.onUpdate = function (data) {
            var _a = _this.props, group = _a.group, project = _a.project, organization = _a.organization, api = _a.api;
            indicator_1.addLoadingMessage(locale_1.t('Saving changes\u2026'));
            group_1.bulkUpdate(api, {
                orgId: organization.slug,
                projectId: project.slug,
                itemIds: [group.id],
                data: data,
            }, {
                complete: indicator_1.clearIndicators,
            });
        };
        _this.onReprocessEvent = function () {
            var _a = _this.props, group = _a.group, organization = _a.organization;
            modal_1.openReprocessEventModal({ organization: organization, groupId: group.id });
        };
        _this.onToggleShare = function () {
            _this.onShare(!_this.props.group.isPublic);
        };
        _this.onToggleBookmark = function () {
            _this.onUpdate({ isBookmarked: !_this.props.group.isBookmarked });
        };
        _this.onToggleSubscribe = function () {
            _this.onUpdate({ isSubscribed: !_this.props.group.isSubscribed });
        };
        _this.onDiscard = function () {
            var _a = _this.props, group = _a.group, project = _a.project, organization = _a.organization, api = _a.api;
            var id = guid_1.uniqueId();
            indicator_1.addLoadingMessage(locale_1.t('Discarding event\u2026'));
            groupActions_1.default.discard(id, group.id);
            api.request("/issues/" + group.id + "/", {
                method: 'PUT',
                data: { discard: true },
                success: function (response) {
                    groupActions_1.default.discardSuccess(id, group.id, response);
                    react_router_1.browserHistory.push("/" + organization.slug + "/" + project.slug + "/");
                },
                error: function (error) {
                    groupActions_1.default.discardError(id, group.id, error);
                },
                complete: indicator_1.clearIndicators,
            });
        };
        return _this;
    }
    Actions.prototype.componentWillReceiveProps = function (nextProps) {
        if (this.state.shareBusy && nextProps.group.shareId !== this.props.group.shareId) {
            this.setState({ shareBusy: false });
        }
    };
    Actions.prototype.getShareUrl = function (shareId) {
        if (!shareId) {
            return '';
        }
        var path = "/share/issue/" + shareId + "/";
        var _a = window.location, host = _a.host, protocol = _a.protocol;
        return protocol + "//" + host + path;
    };
    Actions.prototype.getDiscoverUrl = function () {
        var _a = this.props, group = _a.group, project = _a.project, organization = _a.organization;
        var title = group.title, id = group.id, type = group.type;
        var discoverQuery = {
            id: undefined,
            name: title || type,
            fields: ['title', 'release', 'environment', 'user.display', 'timestamp'],
            orderby: '-timestamp',
            query: "issue.id:" + id,
            projects: [Number(project.id)],
            version: 2,
            range: '90d',
        };
        var discoverView = eventView_1.default.fromSavedQuery(discoverQuery);
        return discoverView.getResultsViewUrlTarget(organization.slug);
    };
    Actions.prototype.onShare = function (shared) {
        var _a = this.props, group = _a.group, project = _a.project, organization = _a.organization, api = _a.api;
        this.setState({ shareBusy: true });
        // not sure why this is a bulkUpdate
        group_1.bulkUpdate(api, {
            orgId: organization.slug,
            projectId: project.slug,
            itemIds: [group.id],
            data: {
                isPublic: shared,
            },
        }, {
            error: function () {
                indicator_1.addErrorMessage(locale_1.t('Error sharing'));
            },
            complete: function () {
                // shareBusy marked false in componentWillReceiveProps to sync
                // busy state update with shareId update
            },
        });
    };
    Actions.prototype.handleClick = function (disabled, onClick) {
        return function (event) {
            if (disabled) {
                event.preventDefault();
                event.stopPropagation();
                return;
            }
            onClick(event);
        };
    };
    Actions.prototype.render = function () {
        var _this = this;
        var _a;
        var _b = this.props, group = _b.group, project = _b.project, organization = _b.organization, disabled = _b.disabled, event = _b.event;
        var status = group.status, isBookmarked = group.isBookmarked;
        var orgFeatures = new Set(organization.features);
        var bookmarkTitle = isBookmarked ? locale_1.t('Remove bookmark') : locale_1.t('Bookmark');
        var hasRelease = !!((_a = project.features) === null || _a === void 0 ? void 0 : _a.includes('releases'));
        var isResolved = status === 'resolved';
        var isIgnored = status === 'ignored';
        return (<Wrapper>
        <guideAnchor_1.default target="resolve" position="bottom" offset={space_1.default(3)}>
          <resolve_1.default disabled={disabled} disableDropdown={disabled} hasRelease={hasRelease} latestRelease={project.latestRelease} onUpdate={this.onUpdate} orgSlug={organization.slug} projectSlug={project.slug} isResolved={isResolved} isAutoResolved={group.status === 'resolved' ? group.statusDetails.autoResolved : undefined}/>
        </guideAnchor_1.default>
        <guideAnchor_1.default target="ignore_delete_discard" position="bottom" offset={space_1.default(3)}>
          <ignore_1.default isIgnored={isIgnored} onUpdate={this.onUpdate} disabled={disabled}/>
        </guideAnchor_1.default>
        <tooltip_1.default disabled={!!group.inbox || disabled} title={locale_1.t('Issue has been reviewed')}>
          <reviewAction_1.default onUpdate={this.onUpdate} disabled={!group.inbox || disabled}/>
        </tooltip_1.default>
        <deleteAction_1.default disabled={disabled} organization={organization} project={project} onDelete={this.onDelete} onDiscard={this.onDiscard}/>
        {orgFeatures.has('shared-issues') && (<shareIssue_1.default disabled={disabled} loading={this.state.shareBusy} isShared={group.isPublic} shareUrl={this.getShareUrl(group.shareId)} onToggle={this.onToggleShare} onReshare={function () { return _this.onShare(true); }}/>)}

        {orgFeatures.has('discover-basic') && (<button_1.default disabled={disabled} to={disabled ? '' : this.getDiscoverUrl()}>
            <guideAnchor_1.default target="open_in_discover">{locale_1.t('Open in Discover')}</guideAnchor_1.default>
          </button_1.default>)}

        <BookmarkButton disabled={disabled} isActive={group.isBookmarked} title={bookmarkTitle} label={bookmarkTitle} onClick={this.handleClick(disabled, this.onToggleBookmark)} icon={<icons_1.IconStar isSolid size="xs"/>}/>

        <subscribeAction_1.default disabled={disabled} group={group} onClick={this.handleClick(disabled, this.onToggleSubscribe)}/>

        {displayReprocessEventAction_1.displayReprocessEventAction(organization.features, event) && (<ReprocessAction disabled={disabled} icon={<iconRefresh_1.IconRefresh size="xs"/>} title={locale_1.t('Reprocess this issue')} label={locale_1.t('Reprocess this issue')} onClick={this.handleClick(disabled, this.onReprocessEvent)}/>)}
      </Wrapper>);
    };
    return Actions;
}(React.Component));
exports.Actions = Actions;
var ReprocessAction = styled_1.default(button_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject([""], [""])));
var BookmarkButton = styled_1.default(button_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), function (p) {
    return p.isActive &&
        "\n   && {\n background: " + p.theme.yellow100 + ";\n color: " + p.theme.yellow300 + ";\n border-color: " + p.theme.yellow300 + ";\n text-shadow: 0 1px 0 rgba(0, 0, 0, 0.15);\n}\n  ";
});
var Wrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  justify-content: flex-start;\n  align-items: center;\n  grid-auto-flow: column;\n  gap: ", ";\n  margin-top: ", ";\n  white-space: nowrap;\n"], ["\n  display: grid;\n  justify-content: flex-start;\n  align-items: center;\n  grid-auto-flow: column;\n  gap: ", ";\n  margin-top: ", ";\n  white-space: nowrap;\n"])), space_1.default(0.5), space_1.default(2));
exports.default = withApi_1.default(withOrganization_1.default(Actions));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=index.jsx.map