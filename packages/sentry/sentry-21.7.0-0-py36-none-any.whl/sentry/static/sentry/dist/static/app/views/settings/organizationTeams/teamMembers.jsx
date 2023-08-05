Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var debounce_1 = tslib_1.__importDefault(require("lodash/debounce"));
var indicator_1 = require("app/actionCreators/indicator");
var modal_1 = require("app/actionCreators/modal");
var teams_1 = require("app/actionCreators/teams");
var userAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/userAvatar"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var dropdownAutoComplete_1 = tslib_1.__importDefault(require("app/components/dropdownAutoComplete"));
var dropdownButton_1 = tslib_1.__importDefault(require("app/components/dropdownButton"));
var idBadge_1 = tslib_1.__importDefault(require("app/components/idBadge"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var panels_1 = require("app/components/panels");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withConfig_1 = tslib_1.__importDefault(require("app/utils/withConfig"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var TeamMembers = /** @class */ (function (_super) {
    tslib_1.__extends(TeamMembers, _super);
    function TeamMembers() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: true,
            error: false,
            dropdownBusy: false,
            teamMemberList: [],
            orgMemberList: [],
        };
        _this.debouncedFetchMembersRequest = debounce_1.default(function (query) {
            return _this.setState({ dropdownBusy: true }, function () { return _this.fetchMembersRequest(query); });
        }, 200);
        _this.fetchMembersRequest = function (query) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, params, api, orgId, data, _err_1;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, params = _a.params, api = _a.api;
                        orgId = params.orgId;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/organizations/" + orgId + "/members/", {
                                query: { query: query },
                            })];
                    case 2:
                        data = _b.sent();
                        this.setState({
                            orgMemberList: data,
                            dropdownBusy: false,
                        });
                        return [3 /*break*/, 4];
                    case 3:
                        _err_1 = _b.sent();
                        indicator_1.addErrorMessage(locale_1.t('Unable to load organization members.'), {
                            duration: 2000,
                        });
                        this.setState({
                            dropdownBusy: false,
                        });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.fetchData = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, api, params, data, err_1;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, params = _a.params;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/teams/" + params.orgId + "/" + params.teamId + "/members/")];
                    case 2:
                        data = _b.sent();
                        this.setState({
                            teamMemberList: data,
                            loading: false,
                            error: false,
                        });
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _b.sent();
                        this.setState({
                            loading: false,
                            error: true,
                        });
                        return [3 /*break*/, 4];
                    case 4:
                        this.fetchMembersRequest('');
                        return [2 /*return*/];
                }
            });
        }); };
        _this.addTeamMember = function (selection) {
            var params = _this.props.params;
            _this.setState({ loading: true });
            // Reset members list after adding member to team
            _this.debouncedFetchMembersRequest('');
            teams_1.joinTeam(_this.props.api, {
                orgId: params.orgId,
                teamId: params.teamId,
                memberId: selection.value,
            }, {
                success: function () {
                    var orgMember = _this.state.orgMemberList.find(function (member) { return member.id === selection.value; });
                    if (orgMember === undefined) {
                        return;
                    }
                    _this.setState({
                        loading: false,
                        error: false,
                        teamMemberList: _this.state.teamMemberList.concat([orgMember]),
                    });
                    indicator_1.addSuccessMessage(locale_1.t('Successfully added member to team.'));
                },
                error: function () {
                    _this.setState({
                        loading: false,
                    });
                    indicator_1.addErrorMessage(locale_1.t('Unable to add team member.'));
                },
            });
        };
        /**
         * We perform an API request to support orgs with > 100 members (since that's the max API returns)
         *
         * @param {Event} e React Event when member filter input changes
         */
        _this.handleMemberFilterChange = function (e) {
            _this.setState({ dropdownBusy: true });
            _this.debouncedFetchMembersRequest(e.target.value);
        };
        return _this;
    }
    TeamMembers.prototype.componentDidMount = function () {
        this.fetchData();
    };
    TeamMembers.prototype.UNSAFE_componentWillReceiveProps = function (nextProps) {
        var params = this.props.params;
        if (nextProps.params.teamId !== params.teamId ||
            nextProps.params.orgId !== params.orgId) {
            this.setState({
                loading: true,
                error: false,
            }, this.fetchData);
        }
    };
    TeamMembers.prototype.removeMember = function (member) {
        var _this = this;
        var params = this.props.params;
        teams_1.leaveTeam(this.props.api, {
            orgId: params.orgId,
            teamId: params.teamId,
            memberId: member.id,
        }, {
            success: function () {
                _this.setState({
                    teamMemberList: _this.state.teamMemberList.filter(function (m) { return m.id !== member.id; }),
                });
                indicator_1.addSuccessMessage(locale_1.t('Successfully removed member from team.'));
            },
            error: function () {
                return indicator_1.addErrorMessage(locale_1.t('There was an error while trying to remove a member from the team.'));
            },
        });
    };
    TeamMembers.prototype.renderDropdown = function (hasWriteAccess) {
        var _this = this;
        var _a = this.props, organization = _a.organization, params = _a.params;
        var existingMembers = new Set(this.state.teamMemberList.map(function (member) { return member.id; }));
        // members can add other members to a team if the `Open Membership` setting is enabled
        // otherwise, `org:write` or `team:admin` permissions are required
        var hasOpenMembership = !!(organization === null || organization === void 0 ? void 0 : organization.openMembership);
        var canAddMembers = hasOpenMembership || hasWriteAccess;
        var items = (this.state.orgMemberList || [])
            .filter(function (m) { return !existingMembers.has(m.id); })
            .map(function (m) { return ({
            searchKey: m.name + " " + m.email,
            value: m.id,
            label: (<StyledUserListElement>
            <StyledAvatar user={m} size={24} className="avatar"/>
            <StyledNameOrEmail>{m.name || m.email}</StyledNameOrEmail>
          </StyledUserListElement>),
        }); });
        var menuHeader = (<StyledMembersLabel>
        {locale_1.t('Members')}
        <StyledCreateMemberLink to="" onClick={function () { return modal_1.openInviteMembersModal({ source: 'teams' }); }} data-test-id="invite-member">
          {locale_1.t('Invite Member')}
        </StyledCreateMemberLink>
      </StyledMembersLabel>);
        return (<dropdownAutoComplete_1.default items={items} alignMenu="right" onSelect={canAddMembers
                ? this.addTeamMember
                : function (selection) {
                    return modal_1.openTeamAccessRequestModal({
                        teamId: params.teamId,
                        orgId: params.orgId,
                        memberId: selection.value,
                    });
                }} menuHeader={menuHeader} emptyMessage={locale_1.t('No members')} onChange={this.handleMemberFilterChange} busy={this.state.dropdownBusy} onClose={function () { return _this.debouncedFetchMembersRequest(''); }}>
        {function (_a) {
                var isOpen = _a.isOpen;
                return (<dropdownButton_1.default isOpen={isOpen} size="xsmall" data-test-id="add-member">
            {locale_1.t('Add Member')}
          </dropdownButton_1.default>);
            }}
      </dropdownAutoComplete_1.default>);
    };
    TeamMembers.prototype.removeButton = function (member) {
        var _this = this;
        return (<button_1.default size="small" icon={<icons_1.IconSubtract size="xs" isCircled/>} onClick={function () { return _this.removeMember(member); }} label={locale_1.t('Remove')}>
        {locale_1.t('Remove')}
      </button_1.default>);
    };
    TeamMembers.prototype.render = function () {
        var _this = this;
        if (this.state.loading) {
            return <loadingIndicator_1.default />;
        }
        if (this.state.error) {
            return <loadingError_1.default onRetry={this.fetchData}/>;
        }
        var _a = this.props, params = _a.params, organization = _a.organization, config = _a.config;
        var access = organization.access;
        var hasWriteAccess = access.includes('org:write') || access.includes('team:admin');
        return (<panels_1.Panel>
        <panels_1.PanelHeader hasButtons>
          <div>{locale_1.t('Members')}</div>
          <div style={{ textTransform: 'none' }}>{this.renderDropdown(hasWriteAccess)}</div>
        </panels_1.PanelHeader>
        {this.state.teamMemberList.length ? (this.state.teamMemberList.map(function (member) {
                var isSelf = member.email === config.user.email;
                var canRemoveMember = hasWriteAccess || isSelf;
                return (<StyledMemberContainer key={member.id}>
                <idBadge_1.default avatarSize={36} member={member} useLink orgId={params.orgId}/>
                {canRemoveMember && _this.removeButton(member)}
              </StyledMemberContainer>);
            })) : (<emptyMessage_1.default icon={<icons_1.IconUser size="xl"/>} size="large">
            {locale_1.t('This team has no members')}
          </emptyMessage_1.default>)}
      </panels_1.Panel>);
    };
    return TeamMembers;
}(React.Component));
var StyledMemberContainer = styled_1.default(panels_1.PanelItem)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  justify-content: space-between;\n  align-items: center;\n"], ["\n  justify-content: space-between;\n  align-items: center;\n"])));
var StyledUserListElement = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n"])), space_1.default(0.5));
var StyledNameOrEmail = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  ", ";\n"], ["\n  font-size: ", ";\n  ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, overflowEllipsis_1.default);
var StyledAvatar = styled_1.default(function (props) { return <userAvatar_1.default {...props}/>; })(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  min-width: 1.75em;\n  min-height: 1.75em;\n  width: 1.5em;\n  height: 1.5em;\n"], ["\n  min-width: 1.75em;\n  min-height: 1.75em;\n  width: 1.5em;\n  height: 1.5em;\n"])));
var StyledMembersLabel = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  padding: ", " 0;\n  font-size: ", ";\n  text-transform: uppercase;\n"], ["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  padding: ", " 0;\n  font-size: ", ";\n  text-transform: uppercase;\n"])), space_1.default(1), function (p) { return p.theme.fontSizeExtraSmall; });
var StyledCreateMemberLink = styled_1.default(link_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  text-transform: none;\n"], ["\n  text-transform: none;\n"])));
exports.default = withConfig_1.default(withApi_1.default(withOrganization_1.default(TeamMembers)));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=teamMembers.jsx.map