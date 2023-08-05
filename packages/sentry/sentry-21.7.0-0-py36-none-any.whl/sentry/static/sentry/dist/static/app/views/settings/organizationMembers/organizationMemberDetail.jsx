Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var account_1 = require("app/actionCreators/account");
var indicator_1 = require("app/actionCreators/indicator");
var members_1 = require("app/actionCreators/members");
var autoSelectText_1 = tslib_1.__importDefault(require("app/components/autoSelectText"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var notFound_1 = tslib_1.__importDefault(require("app/components/errors/notFound"));
var hookOrDefault_1 = tslib_1.__importDefault(require("app/components/hookOrDefault"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var panels_1 = require("app/components/panels");
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var locale_1 = require("app/locale");
var input_1 = require("app/styles/input");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var isMemberDisabledFromLimit_1 = tslib_1.__importDefault(require("app/utils/isMemberDisabledFromLimit"));
var recreateRoute_1 = tslib_1.__importDefault(require("app/utils/recreateRoute"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var withTeams_1 = tslib_1.__importDefault(require("app/utils/withTeams"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var field_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var teamSelect_1 = tslib_1.__importDefault(require("app/views/settings/components/teamSelect"));
var roleSelect_1 = tslib_1.__importDefault(require("./inviteMember/roleSelect"));
var MULTIPLE_ORGS = locale_1.t('Cannot be reset since user is in more than one organization');
var NOT_ENROLLED = locale_1.t('Not enrolled in two-factor authentication');
var NO_PERMISSION = locale_1.t('You do not have permission to perform this action');
var TWO_FACTOR_REQUIRED = locale_1.t('Cannot be reset since two-factor is required for this organization');
var DisabledMemberTooltip = hookOrDefault_1.default({
    hookName: 'component:disabled-member-tooltip',
    defaultComponent: function (_a) {
        var children = _a.children;
        return <react_1.Fragment>{children}</react_1.Fragment>;
    },
});
var OrganizationMemberDetail = /** @class */ (function (_super) {
    tslib_1.__extends(OrganizationMemberDetail, _super);
    function OrganizationMemberDetail() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSave = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, organization, params, resp_1, errorMessage;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, organization = _a.organization, params = _a.params;
                        indicator_1.addLoadingMessage(locale_1.t('Saving...'));
                        this.setState({ busy: true });
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, members_1.updateMember(this.api, {
                                orgId: organization.slug,
                                memberId: params.memberId,
                                data: this.state.member,
                            })];
                    case 2:
                        _b.sent();
                        indicator_1.addSuccessMessage(locale_1.t('Saved'));
                        this.redirectToMemberPage();
                        return [3 /*break*/, 4];
                    case 3:
                        resp_1 = _b.sent();
                        errorMessage = (resp_1 && resp_1.responseJSON && resp_1.responseJSON.detail) || locale_1.t('Could not save...');
                        indicator_1.addErrorMessage(errorMessage);
                        return [3 /*break*/, 4];
                    case 4:
                        this.setState({ busy: false });
                        return [2 /*return*/];
                }
            });
        }); };
        _this.handleInvite = function (regenerate) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, organization, params, data_1, _err_1;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, organization = _a.organization, params = _a.params;
                        indicator_1.addLoadingMessage(locale_1.t('Sending invite...'));
                        this.setState({ busy: true });
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, members_1.resendMemberInvite(this.api, {
                                orgId: organization.slug,
                                memberId: params.memberId,
                                regenerate: regenerate,
                            })];
                    case 2:
                        data_1 = _b.sent();
                        indicator_1.addSuccessMessage(locale_1.t('Sent invite!'));
                        if (regenerate) {
                            this.setState(function (state) { return ({ member: tslib_1.__assign(tslib_1.__assign({}, state.member), data_1) }); });
                        }
                        return [3 /*break*/, 4];
                    case 3:
                        _err_1 = _b.sent();
                        indicator_1.addErrorMessage(locale_1.t('Could not send invite'));
                        return [3 /*break*/, 4];
                    case 4:
                        this.setState({ busy: false });
                        return [2 /*return*/];
                }
            });
        }); };
        _this.handleAddTeam = function (team) {
            var member = _this.state.member;
            if (!member.teams.includes(team.slug)) {
                member.teams.push(team.slug);
            }
            _this.setState({ member: member });
        };
        _this.handleRemoveTeam = function (removedTeam) {
            var member = _this.state.member;
            _this.setState({
                member: tslib_1.__assign(tslib_1.__assign({}, member), { teams: member.teams.filter(function (slug) { return slug !== removedTeam; }) }),
            });
        };
        _this.handle2faReset = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, organization, router, user, requests, err_1;
            var _this = this;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, organization = _a.organization, router = _a.router;
                        user = this.state.member.user;
                        requests = user.authenticators.map(function (auth) {
                            return account_1.removeAuthenticator(_this.api, user.id, auth.id);
                        });
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, Promise.all(requests)];
                    case 2:
                        _b.sent();
                        router.push("/settings/" + organization.slug + "/members/");
                        indicator_1.addSuccessMessage(locale_1.t('All authenticators have been removed'));
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _b.sent();
                        indicator_1.addErrorMessage(locale_1.t('Error removing authenticators'));
                        Sentry.captureException(err_1);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.showResetButton = function () {
            var organization = _this.props.organization;
            var member = _this.state.member;
            var user = member.user;
            if (!user || !user.authenticators || organization.require2FA) {
                return false;
            }
            var hasAuth = user.authenticators.length >= 1;
            return hasAuth && user.canReset2fa;
        };
        _this.getTooltip = function () {
            var organization = _this.props.organization;
            var member = _this.state.member;
            var user = member.user;
            if (!user) {
                return '';
            }
            if (!user.authenticators) {
                return NO_PERMISSION;
            }
            if (!user.authenticators.length) {
                return NOT_ENROLLED;
            }
            if (!user.canReset2fa) {
                return MULTIPLE_ORGS;
            }
            if (organization.require2FA) {
                return TWO_FACTOR_REQUIRED;
            }
            return '';
        };
        return _this;
    }
    OrganizationMemberDetail.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { roleList: [], selectedRole: '', member: null });
    };
    OrganizationMemberDetail.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, params = _a.params;
        return [
            ['member', "/organizations/" + organization.slug + "/members/" + params.memberId + "/"],
        ];
    };
    OrganizationMemberDetail.prototype.redirectToMemberPage = function () {
        var _a = this.props, location = _a.location, params = _a.params, routes = _a.routes;
        var members = recreateRoute_1.default('members/', {
            location: location,
            routes: routes,
            params: params,
            stepBack: -2,
        });
        react_router_1.browserHistory.push(members);
    };
    Object.defineProperty(OrganizationMemberDetail.prototype, "memberDeactivated", {
        get: function () {
            return isMemberDisabledFromLimit_1.default(this.state.member);
        },
        enumerable: false,
        configurable: true
    });
    OrganizationMemberDetail.prototype.renderMemberStatus = function (member) {
        if (this.memberDeactivated) {
            return (<em>
          <DisabledMemberTooltip>{locale_1.t('Deactivated')}</DisabledMemberTooltip>
        </em>);
        }
        if (member.expired) {
            return <em>{locale_1.t('Invitation Expired')}</em>;
        }
        if (member.pending) {
            return <em>{locale_1.t('Invitation Pending')}</em>;
        }
        return locale_1.t('Active');
    };
    OrganizationMemberDetail.prototype.renderBody = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, teams = _a.teams;
        var member = this.state.member;
        if (!member) {
            return <notFound_1.default />;
        }
        var access = organization.access;
        var inviteLink = member.invite_link;
        var canEdit = access.includes('org:write') && !this.memberDeactivated;
        var email = member.email, expired = member.expired, pending = member.pending;
        var canResend = !expired;
        var showAuth = !pending;
        return (<react_1.Fragment>
        <settingsPageHeader_1.default title={<react_1.Fragment>
              <div>{member.name}</div>
              <ExtraHeaderText>{locale_1.t('Member Settings')}</ExtraHeaderText>
            </react_1.Fragment>}/>

        <panels_1.Panel>
          <panels_1.PanelHeader>{locale_1.t('Basics')}</panels_1.PanelHeader>

          <panels_1.PanelBody>
            <panels_1.PanelItem>
              <OverflowWrapper>
                <Details>
                  <div>
                    <DetailLabel>{locale_1.t('Email')}</DetailLabel>
                    <div>
                      <externalLink_1.default href={"mailto:" + email}>{email}</externalLink_1.default>
                    </div>
                  </div>
                  <div>
                    <DetailLabel>{locale_1.t('Status')}</DetailLabel>
                    <div data-test-id="member-status">
                      {this.renderMemberStatus(member)}
                    </div>
                  </div>
                  <div>
                    <DetailLabel>{locale_1.t('Added')}</DetailLabel>
                    <div>
                      <dateTime_1.default dateOnly date={member.dateCreated}/>
                    </div>
                  </div>
                </Details>

                {inviteLink && (<InviteSection>
                    <div>
                      <DetailLabel>{locale_1.t('Invite Link')}</DetailLabel>
                      <autoSelectText_1.default>
                        <CodeInput>{inviteLink}</CodeInput>
                      </autoSelectText_1.default>
                      <p className="help-block">
                        {locale_1.t('This unique invite link may only be used by this member.')}
                      </p>
                    </div>
                    <InviteActions>
                      <button_1.default onClick={function () { return _this.handleInvite(true); }}>
                        {locale_1.t('Generate New Invite')}
                      </button_1.default>
                      {canResend && (<button_1.default data-test-id="resend-invite" onClick={function () { return _this.handleInvite(false); }}>
                          {locale_1.t('Resend Invite')}
                        </button_1.default>)}
                    </InviteActions>
                  </InviteSection>)}
              </OverflowWrapper>
            </panels_1.PanelItem>
          </panels_1.PanelBody>
        </panels_1.Panel>

        {showAuth && (<panels_1.Panel>
            <panels_1.PanelHeader>{locale_1.t('Authentication')}</panels_1.PanelHeader>
            <panels_1.PanelBody>
              <field_1.default alignRight flexibleControlStateSize label={locale_1.t('Reset two-factor authentication')} help={locale_1.t('Resetting two-factor authentication will remove all two-factor authentication methods for this member.')}>
                <tooltip_1.default data-test-id="reset-2fa-tooltip" disabled={this.showResetButton()} title={this.getTooltip()}>
                  <confirm_1.default disabled={!this.showResetButton()} message={locale_1.tct('Are you sure you want to disable all two-factor authentication methods for [name]?', { name: member.name ? member.name : 'this member' })} onConfirm={this.handle2faReset} data-test-id="reset-2fa-confirm">
                    <button_1.default data-test-id="reset-2fa" priority="danger">
                      {locale_1.t('Reset two-factor authentication')}
                    </button_1.default>
                  </confirm_1.default>
                </tooltip_1.default>
              </field_1.default>
            </panels_1.PanelBody>
          </panels_1.Panel>)}

        <roleSelect_1.default enforceAllowed={false} disabled={!canEdit} roleList={member.roles} selectedRole={member.role} setRole={function (slug) { return _this.setState({ member: tslib_1.__assign(tslib_1.__assign({}, member), { role: slug }) }); }}/>

        <teamSelect_1.default organization={organization} selectedTeams={member.teams
                .map(function (teamSlug) { return teams.find(function (team) { return team.slug === teamSlug; }); })
                .filter(function (team) { return team !== undefined; })} disabled={!canEdit} onAddTeam={this.handleAddTeam} onRemoveTeam={this.handleRemoveTeam}/>

        <Footer>
          <button_1.default priority="primary" busy={this.state.busy} onClick={this.handleSave} disabled={!canEdit}>
            {locale_1.t('Save Member')}
          </button_1.default>
        </Footer>
      </react_1.Fragment>);
    };
    return OrganizationMemberDetail;
}(asyncView_1.default));
exports.default = withTeams_1.default(withOrganization_1.default(OrganizationMemberDetail));
var ExtraHeaderText = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-weight: normal;\n  font-size: ", ";\n"], ["\n  color: ", ";\n  font-weight: normal;\n  font-size: ", ";\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeLarge; });
var Details = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-template-columns: 2fr 1fr 1fr;\n  grid-gap: ", ";\n  width: 100%;\n\n  @media (max-width: ", ") {\n    grid-auto-flow: row;\n    grid-template-columns: auto;\n  }\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-template-columns: 2fr 1fr 1fr;\n  grid-gap: ", ";\n  width: 100%;\n\n  @media (max-width: ", ") {\n    grid-auto-flow: row;\n    grid-template-columns: auto;\n  }\n"])), space_1.default(2), function (p) { return p.theme.breakpoints[0]; });
var DetailLabel = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  font-weight: bold;\n  margin-bottom: ", ";\n  color: ", ";\n"], ["\n  font-weight: bold;\n  margin-bottom: ", ";\n  color: ", ";\n"])), space_1.default(0.5), function (p) { return p.theme.textColor; });
var OverflowWrapper = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  overflow: hidden;\n  flex: 1;\n"], ["\n  overflow: hidden;\n  flex: 1;\n"])));
var InviteSection = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  border-top: 1px solid ", ";\n  margin-top: ", ";\n  padding-top: ", ";\n"], ["\n  border-top: 1px solid ", ";\n  margin-top: ", ";\n  padding-top: ", ";\n"])), function (p) { return p.theme.border; }, space_1.default(2), space_1.default(2));
var CodeInput = styled_1.default('code')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  ", "; /* Have to do this for typescript :( */\n"], ["\n  ", "; /* Have to do this for typescript :( */\n"])), function (p) { return input_1.inputStyles(p); });
var InviteActions = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-auto-flow: column;\n  justify-content: flex-end;\n  margin-top: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-auto-flow: column;\n  justify-content: flex-end;\n  margin-top: ", ";\n"])), space_1.default(1), space_1.default(2));
var Footer = styled_1.default('div')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n"], ["\n  display: flex;\n  justify-content: flex-end;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=organizationMemberDetail.jsx.map