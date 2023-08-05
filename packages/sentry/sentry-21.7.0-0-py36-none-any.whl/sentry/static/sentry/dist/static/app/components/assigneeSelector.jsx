Object.defineProperty(exports, "__esModule", { value: true });
exports.putSessionUserFirst = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var group_1 = require("app/actionCreators/group");
var modal_1 = require("app/actionCreators/modal");
var actorAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/actorAvatar"));
var suggestedAvatarStack_1 = tslib_1.__importDefault(require("app/components/avatar/suggestedAvatarStack"));
var teamAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/teamAvatar"));
var userAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/userAvatar"));
var dropdownAutoComplete_1 = tslib_1.__importDefault(require("app/components/dropdownAutoComplete"));
var dropdownBubble_1 = tslib_1.__importDefault(require("app/components/dropdownBubble"));
var highlight_1 = tslib_1.__importDefault(require("app/components/highlight"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var textOverflow_1 = tslib_1.__importDefault(require("app/components/textOverflow"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var groupStore_1 = tslib_1.__importDefault(require("app/stores/groupStore"));
var memberListStore_1 = tslib_1.__importDefault(require("app/stores/memberListStore"));
var projectsStore_1 = tslib_1.__importDefault(require("app/stores/projectsStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var AssigneeSelector = /** @class */ (function (_super) {
    tslib_1.__extends(AssigneeSelector, _super);
    function AssigneeSelector() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getInitialState();
        _this.unlisteners = [
            groupStore_1.default.listen(function (itemIds) { return _this.onGroupChange(itemIds); }, undefined),
            memberListStore_1.default.listen(function (users) {
                _this.handleMemberListUpdate(users);
            }, undefined),
        ];
        _this.handleMemberListUpdate = function (members) {
            if (members === _this.state.memberList) {
                return;
            }
            _this.setState({ memberList: members });
        };
        _this.handleAssign = function (_a, _state, e) {
            var _b = _a.value, type = _b.type, assignee = _b.assignee;
            if (type === 'member') {
                _this.assignToUser(assignee);
            }
            if (type === 'team') {
                _this.assignToTeam(assignee);
            }
            e === null || e === void 0 ? void 0 : e.stopPropagation();
            var onAssign = _this.props.onAssign;
            if (onAssign) {
                var suggestionType_1 = type === 'member' ? 'user' : type;
                var suggestion = _this.getSuggestedAssignees().find(function (actor) { return actor.type === suggestionType_1 && actor.id === assignee.id; });
                onAssign === null || onAssign === void 0 ? void 0 : onAssign(type, assignee, suggestion);
            }
        };
        _this.clearAssignTo = function (e) {
            // clears assignment
            group_1.clearAssignment(_this.props.id);
            _this.setState({ loading: true });
            e.stopPropagation();
        };
        return _this;
    }
    AssigneeSelector.prototype.getInitialState = function () {
        var group = groupStore_1.default.get(this.props.id);
        var memberList = memberListStore_1.default.loaded ? memberListStore_1.default.getAll() : undefined;
        var loading = groupStore_1.default.hasStatus(this.props.id, 'assignTo');
        var suggestedOwners = group === null || group === void 0 ? void 0 : group.owners;
        return {
            assignedTo: group === null || group === void 0 ? void 0 : group.assignedTo,
            memberList: memberList,
            loading: loading,
            suggestedOwners: suggestedOwners,
        };
    };
    AssigneeSelector.prototype.componentWillReceiveProps = function (nextProps) {
        var loading = groupStore_1.default.hasStatus(nextProps.id, 'assignTo');
        if (nextProps.id !== this.props.id || loading !== this.state.loading) {
            var group = groupStore_1.default.get(this.props.id);
            this.setState({
                loading: loading,
                assignedTo: group === null || group === void 0 ? void 0 : group.assignedTo,
                suggestedOwners: group === null || group === void 0 ? void 0 : group.owners,
            });
        }
    };
    AssigneeSelector.prototype.shouldComponentUpdate = function (nextProps, nextState) {
        if (nextState.loading !== this.state.loading) {
            return true;
        }
        // If the memberList in props has changed, re-render as
        // props have updated, and we won't use internal state anyways.
        if (nextProps.memberList &&
            !utils_1.valueIsEqual(this.props.memberList, nextProps.memberList)) {
            return true;
        }
        var currentMembers = this.memberList();
        // XXX(billyvg): this means that once `memberList` is not-null, this component will never update due to `memberList` changes
        // Note: this allows us to show a "loading" state for memberList, but only before `MemberListStore.loadInitialData`
        // is called
        if (currentMembers === undefined && nextState.memberList !== currentMembers) {
            return true;
        }
        return !utils_1.valueIsEqual(nextState.assignedTo, this.state.assignedTo, true);
    };
    AssigneeSelector.prototype.componentWillUnmount = function () {
        this.unlisteners.forEach(function (unlistener) { return unlistener === null || unlistener === void 0 ? void 0 : unlistener(); });
    };
    AssigneeSelector.prototype.memberList = function () {
        return this.props.memberList ? this.props.memberList : this.state.memberList;
    };
    AssigneeSelector.prototype.onGroupChange = function (itemIds) {
        if (!itemIds.has(this.props.id)) {
            return;
        }
        var group = groupStore_1.default.get(this.props.id);
        this.setState({
            assignedTo: group === null || group === void 0 ? void 0 : group.assignedTo,
            suggestedOwners: group === null || group === void 0 ? void 0 : group.owners,
            loading: groupStore_1.default.hasStatus(this.props.id, 'assignTo'),
        });
    };
    AssigneeSelector.prototype.assignableTeams = function () {
        var _a, _b;
        var group = groupStore_1.default.get(this.props.id);
        if (!group) {
            return [];
        }
        var teams = (_b = (_a = projectsStore_1.default.getBySlug(group.project.slug)) === null || _a === void 0 ? void 0 : _a.teams) !== null && _b !== void 0 ? _b : [];
        return teams
            .sort(function (a, b) { return a.slug.localeCompare(b.slug); })
            .map(function (team) { return ({
            id: utils_1.buildTeamId(team.id),
            display: "#" + team.slug,
            email: team.id,
            team: team,
        }); });
    };
    AssigneeSelector.prototype.assignToUser = function (user) {
        group_1.assignToUser({ id: this.props.id, user: user });
        this.setState({ loading: true });
    };
    AssigneeSelector.prototype.assignToTeam = function (team) {
        group_1.assignToActor({ actor: { id: team.id, type: 'team' }, id: this.props.id });
        this.setState({ loading: true });
    };
    AssigneeSelector.prototype.renderMemberNode = function (member, suggestedReason) {
        var _this = this;
        var size = this.props.size;
        return {
            value: { type: 'member', assignee: member },
            searchKey: member.email + " " + member.name,
            label: function (_a) {
                var inputValue = _a.inputValue;
                return (<MenuItemWrapper data-test-id="assignee-option" key={utils_1.buildUserId(member.id)} onSelect={_this.assignToUser.bind(_this, member)}>
          <IconContainer>
            <userAvatar_1.default user={member} size={size}/>
          </IconContainer>
          <Label>
            <highlight_1.default text={inputValue}>{member.name || member.email}</highlight_1.default>
            {suggestedReason && <SuggestedReason>{suggestedReason}</SuggestedReason>}
          </Label>
        </MenuItemWrapper>);
            },
        };
    };
    AssigneeSelector.prototype.renderNewMemberNodes = function () {
        var _this = this;
        var members = putSessionUserFirst(this.memberList());
        return members.map(function (member) { return _this.renderMemberNode(member); });
    };
    AssigneeSelector.prototype.renderTeamNode = function (assignableTeam, suggestedReason) {
        var _this = this;
        var size = this.props.size;
        var id = assignableTeam.id, display = assignableTeam.display, team = assignableTeam.team;
        return {
            value: { type: 'team', assignee: team },
            searchKey: team.slug,
            label: function (_a) {
                var inputValue = _a.inputValue;
                return (<MenuItemWrapper data-test-id="assignee-option" key={id} onSelect={_this.assignToTeam.bind(_this, team)}>
          <IconContainer>
            <teamAvatar_1.default team={team} size={size}/>
          </IconContainer>
          <Label>
            <highlight_1.default text={inputValue}>{display}</highlight_1.default>
            {suggestedReason && <SuggestedReason>{suggestedReason}</SuggestedReason>}
          </Label>
        </MenuItemWrapper>);
            },
        };
    };
    AssigneeSelector.prototype.renderNewTeamNodes = function () {
        var _this = this;
        return this.assignableTeams().map(function (team) { return _this.renderTeamNode(team); });
    };
    AssigneeSelector.prototype.renderSuggestedAssigneeNodes = function () {
        var _this = this;
        var assignedTo = this.state.assignedTo;
        // filter out suggested assignees if a suggestion is already selected
        return this.getSuggestedAssignees()
            .filter(function (_a) {
            var type = _a.type, id = _a.id;
            return !(type === (assignedTo === null || assignedTo === void 0 ? void 0 : assignedTo.type) && id === (assignedTo === null || assignedTo === void 0 ? void 0 : assignedTo.id));
        })
            .filter(function (_a) {
            var type = _a.type;
            return type === 'user' || type === 'team';
        })
            .map(function (_a) {
            var type = _a.type, suggestedReason = _a.suggestedReason, assignee = _a.assignee;
            var reason = suggestedReason === 'suspectCommit'
                ? locale_1.t('(Suspect Commit)')
                : locale_1.t('(Issue Owner)');
            if (type === 'user') {
                return _this.renderMemberNode(assignee, reason);
            }
            return _this.renderTeamNode(assignee, reason);
        });
    };
    AssigneeSelector.prototype.renderDropdownGroupLabel = function (label) {
        return <GroupHeader>{label}</GroupHeader>;
    };
    AssigneeSelector.prototype.renderNewDropdownItems = function () {
        var _a;
        var teams = this.renderNewTeamNodes();
        var members = this.renderNewMemberNodes();
        var suggestedAssignees = (_a = this.renderSuggestedAssigneeNodes()) !== null && _a !== void 0 ? _a : [];
        var assigneeIds = new Set(suggestedAssignees.map(function (assignee) { return assignee.value.type + ":" + assignee.value.assignee.id; }));
        // filter out duplicates of Team/Member if also a Suggested Assignee
        var filteredTeams = teams.filter(function (team) {
            return !assigneeIds.has(team.value.type + ":" + team.value.assignee.id);
        });
        var filteredMembers = members.filter(function (member) {
            return !assigneeIds.has(member.value.type + ":" + member.value.assignee.id);
        });
        var dropdownItems = [
            {
                label: this.renderDropdownGroupLabel(locale_1.t('Teams')),
                id: 'team-header',
                items: filteredTeams,
            },
            {
                label: this.renderDropdownGroupLabel(locale_1.t('People')),
                id: 'members-header',
                items: filteredMembers,
            },
        ];
        if (suggestedAssignees.length) {
            dropdownItems.unshift({
                label: this.renderDropdownGroupLabel(locale_1.t('Suggested')),
                id: 'suggested-header',
                items: suggestedAssignees,
            });
        }
        return dropdownItems;
    };
    AssigneeSelector.prototype.getSuggestedAssignees = function () {
        var _a;
        var suggestedOwners = this.state.suggestedOwners;
        if (!suggestedOwners) {
            return [];
        }
        var assignableTeams = this.assignableTeams();
        var memberList = (_a = this.memberList()) !== null && _a !== void 0 ? _a : [];
        var suggestedAssignees = suggestedOwners.map(function (owner) {
            // converts a backend suggested owner to a suggested assignee
            var _a = tslib_1.__read(owner.owner.split(':'), 2), ownerType = _a[0], id = _a[1];
            if (ownerType === 'user') {
                var member = memberList.find(function (user) { return user.id === id; });
                if (member) {
                    return {
                        type: 'user',
                        id: id,
                        name: member.name,
                        suggestedReason: owner.type,
                        assignee: member,
                    };
                }
            }
            else if (ownerType === 'team') {
                var matchingTeam = assignableTeams.find(function (assignableTeam) { return assignableTeam.id === owner.owner; });
                if (matchingTeam) {
                    return {
                        type: 'team',
                        id: id,
                        name: matchingTeam.team.name,
                        suggestedReason: owner.type,
                        assignee: matchingTeam,
                    };
                }
            }
            return null;
        });
        return suggestedAssignees.filter(function (owner) { return !!owner; });
    };
    AssigneeSelector.prototype.render = function () {
        var disabled = this.props.disabled;
        var _a = this.state, loading = _a.loading, assignedTo = _a.assignedTo;
        var memberList = this.memberList();
        var suggestedActors = this.getSuggestedAssignees();
        var suggestedReasons = {
            suspectCommit: locale_1.tct('Based on [commit:commit data]', {
                commit: (<TooltipSubExternalLink href="https://docs.sentry.io/product/sentry-basics/guides/integrate-frontend/configure-scms/"/>),
            }),
            ownershipRule: locale_1.t('Matching Issue Owners Rule'),
        };
        var assignedToSuggestion = suggestedActors.find(function (actor) { return actor.id === (assignedTo === null || assignedTo === void 0 ? void 0 : assignedTo.id); });
        return (<AssigneeWrapper>
        {loading && (<loadingIndicator_1.default mini style={{ height: '24px', margin: 0, marginRight: 11 }}/>)}
        {!loading && (<dropdownAutoComplete_1.default disabled={disabled} maxHeight={400} onOpen={function (e) {
                    // This can be called multiple times and does not always have `event`
                    e === null || e === void 0 ? void 0 : e.stopPropagation();
                }} busy={memberList === undefined} items={memberList !== undefined ? this.renderNewDropdownItems() : null} alignMenu="right" onSelect={this.handleAssign} itemSize="small" searchPlaceholder={locale_1.t('Filter teams and people')} menuHeader={assignedTo && (<MenuItemWrapper data-test-id="clear-assignee" onClick={this.clearAssignTo} py={0}>
                  <IconContainer>
                    <ClearAssigneeIcon isCircled size="14px"/>
                  </IconContainer>
                  <Label>{locale_1.t('Clear Assignee')}</Label>
                </MenuItemWrapper>)} menuFooter={<InviteMemberLink to="" data-test-id="invite-member" disabled={loading} onClick={function () { return modal_1.openInviteMembersModal({ source: 'assignee_selector' }); }}>
                <MenuItemWrapper>
                  <IconContainer>
                    <InviteMemberIcon isCircled size="14px"/>
                  </IconContainer>
                  <Label>{locale_1.t('Invite Member')}</Label>
                </MenuItemWrapper>
              </InviteMemberLink>} menuWithArrow emptyHidesInput>
            {function (_a) {
                    var getActorProps = _a.getActorProps, isOpen = _a.isOpen;
                    return (<DropdownButton {...getActorProps({})}>
                {assignedTo ? (<actorAvatar_1.default actor={assignedTo} className="avatar" size={24} tooltip={<TooltipWrapper>
                        {locale_1.tct('Assigned to [name]', {
                                    name: assignedTo.type === 'team'
                                        ? "#" + assignedTo.name
                                        : assignedTo.name,
                                })}
                        {assignedToSuggestion && (<TooltipSubtext>
                            {suggestedReasons[assignedToSuggestion.suggestedReason]}
                          </TooltipSubtext>)}
                      </TooltipWrapper>}/>) : suggestedActors && suggestedActors.length > 0 ? (<suggestedAvatarStack_1.default size={24} owners={suggestedActors} tooltipOptions={{ isHoverable: true }} tooltip={<TooltipWrapper>
                        <div>
                          {locale_1.tct('Suggestion: [name]', {
                                    name: suggestedActors[0].type === 'team'
                                        ? "#" + suggestedActors[0].name
                                        : suggestedActors[0].name,
                                })}
                          {suggestedActors.length > 1 &&
                                    locale_1.tn(' + %s other', ' + %s others', suggestedActors.length - 1)}
                        </div>
                        <TooltipSubtext>
                          {suggestedReasons[suggestedActors[0].suggestedReason]}
                        </TooltipSubtext>
                      </TooltipWrapper>}/>) : (<tooltip_1.default isHoverable skipWrapper title={<TooltipWrapper>
                        <div>{locale_1.t('Unassigned')}</div>
                        <TooltipSubtext>
                          {locale_1.tct('You can auto-assign issues by adding [issueOwners:Issue Owner rules].', {
                                    issueOwners: (<TooltipSubExternalLink href="https://docs.sentry.io/product/error-monitoring/issue-owners/"/>),
                                })}
                        </TooltipSubtext>
                      </TooltipWrapper>}>
                    <StyledIconUser size="20px" color="gray400"/>
                  </tooltip_1.default>)}
                <StyledChevron direction={isOpen ? 'up' : 'down'} size="xs"/>
              </DropdownButton>);
                }}
          </dropdownAutoComplete_1.default>)}
      </AssigneeWrapper>);
    };
    AssigneeSelector.defaultProps = {
        size: 20,
    };
    return AssigneeSelector;
}(React.Component));
function putSessionUserFirst(members) {
    // If session user is in the filtered list of members, put them at the top
    if (!members) {
        return [];
    }
    var sessionUser = configStore_1.default.get('user');
    var sessionUserIndex = members.findIndex(function (member) { return member.id === (sessionUser === null || sessionUser === void 0 ? void 0 : sessionUser.id); });
    if (sessionUserIndex === -1) {
        return members;
    }
    var arrangedMembers = [members[sessionUserIndex]];
    arrangedMembers.push.apply(arrangedMembers, tslib_1.__spreadArray([], tslib_1.__read(members.slice(0, sessionUserIndex))));
    arrangedMembers.push.apply(arrangedMembers, tslib_1.__spreadArray([], tslib_1.__read(members.slice(sessionUserIndex + 1))));
    return arrangedMembers;
}
exports.putSessionUserFirst = putSessionUserFirst;
exports.default = AssigneeSelector;
var AssigneeWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n\n  /* manually align menu underneath dropdown caret */\n  ", " {\n    right: -14px;\n  }\n"], ["\n  display: flex;\n  justify-content: flex-end;\n\n  /* manually align menu underneath dropdown caret */\n  ", " {\n    right: -14px;\n  }\n"])), dropdownBubble_1.default);
var StyledIconUser = styled_1.default(icons_1.IconUser)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  /* We need this to center with Avatar */\n  margin-right: 2px;\n"], ["\n  /* We need this to center with Avatar */\n  margin-right: 2px;\n"])));
var IconContainer = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  width: 24px;\n  height: 24px;\n  flex-shrink: 0;\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  width: 24px;\n  height: 24px;\n  flex-shrink: 0;\n"])));
var MenuItemWrapper = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  cursor: ", ";\n  display: flex;\n  align-items: center;\n  font-size: 13px;\n  ", ";\n"], ["\n  cursor: ", ";\n  display: flex;\n  align-items: center;\n  font-size: 13px;\n  ", ";\n"])), function (p) { return (p.disabled ? 'not-allowed' : 'pointer'); }, function (p) {
    return typeof p.py !== 'undefined' &&
        "\n      padding-top: " + p.py + ";\n      padding-bottom: " + p.py + ";\n    ";
});
var InviteMemberLink = styled_1.default(link_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return (p.disabled ? p.theme.disabled : p.theme.textColor); });
var Label = styled_1.default(textOverflow_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  margin-left: 6px;\n"], ["\n  margin-left: 6px;\n"])));
var ClearAssigneeIcon = styled_1.default(icons_1.IconClose)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  opacity: 0.3;\n"], ["\n  opacity: 0.3;\n"])));
var InviteMemberIcon = styled_1.default(icons_1.IconAdd)(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  opacity: 0.3;\n"], ["\n  opacity: 0.3;\n"])));
var StyledChevron = styled_1.default(icons_1.IconChevron)(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space_1.default(1));
var DropdownButton = styled_1.default('div')(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  font-size: 20px;\n"], ["\n  display: flex;\n  align-items: center;\n  font-size: 20px;\n"])));
var GroupHeader = styled_1.default('div')(templateObject_11 || (templateObject_11 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  font-weight: 600;\n  margin: ", " 0;\n  color: ", ";\n  line-height: ", ";\n  text-align: left;\n"], ["\n  font-size: ", ";\n  font-weight: 600;\n  margin: ", " 0;\n  color: ", ";\n  line-height: ", ";\n  text-align: left;\n"])), function (p) { return p.theme.fontSizeSmall; }, space_1.default(1), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeSmall; });
var SuggestedReason = styled_1.default('span')(templateObject_12 || (templateObject_12 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n  color: ", ";\n"], ["\n  margin-left: ", ";\n  color: ", ";\n"])), space_1.default(0.5), function (p) { return p.theme.textColor; });
var TooltipWrapper = styled_1.default('div')(templateObject_13 || (templateObject_13 = tslib_1.__makeTemplateObject(["\n  text-align: left;\n"], ["\n  text-align: left;\n"])));
var TooltipSubtext = styled_1.default('div')(templateObject_14 || (templateObject_14 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.subText; });
var TooltipSubExternalLink = styled_1.default(externalLink_1.default)(templateObject_15 || (templateObject_15 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  text-decoration: underline;\n\n  :hover {\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n  text-decoration: underline;\n\n  :hover {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.subText; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14, templateObject_15;
//# sourceMappingURL=assigneeSelector.jsx.map