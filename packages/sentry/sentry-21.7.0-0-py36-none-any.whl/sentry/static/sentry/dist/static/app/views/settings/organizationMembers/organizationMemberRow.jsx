Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var userAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/userAvatar"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var hookOrDefault_1 = tslib_1.__importDefault(require("app/components/hookOrDefault"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var panels_1 = require("app/components/panels");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var isMemberDisabledFromLimit_1 = tslib_1.__importDefault(require("app/utils/isMemberDisabledFromLimit"));
var recreateRoute_1 = tslib_1.__importDefault(require("app/utils/recreateRoute"));
var DisabledMemberTooltip = hookOrDefault_1.default({
    hookName: 'component:disabled-member-tooltip',
    defaultComponent: function (_a) {
        var children = _a.children;
        return <react_1.Fragment>{children}</react_1.Fragment>;
    },
});
var OrganizationMemberRow = /** @class */ (function (_super) {
    tslib_1.__extends(OrganizationMemberRow, _super);
    function OrganizationMemberRow() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            busy: false,
        };
        _this.handleRemove = function () {
            var onRemove = _this.props.onRemove;
            if (typeof onRemove !== 'function') {
                return;
            }
            _this.setState({ busy: true });
            onRemove(_this.props.member);
        };
        _this.handleLeave = function () {
            var onLeave = _this.props.onLeave;
            if (typeof onLeave !== 'function') {
                return;
            }
            _this.setState({ busy: true });
            onLeave(_this.props.member);
        };
        _this.handleSendInvite = function () {
            var _a = _this.props, onSendInvite = _a.onSendInvite, member = _a.member;
            if (typeof onSendInvite !== 'function') {
                return;
            }
            onSendInvite(member);
        };
        return _this;
    }
    OrganizationMemberRow.prototype.renderMemberRole = function () {
        var member = this.props.member;
        var roleName = member.roleName, pending = member.pending, expired = member.expired;
        if (isMemberDisabledFromLimit_1.default(member)) {
            return <DisabledMemberTooltip>{locale_1.t('Deactivated')}</DisabledMemberTooltip>;
        }
        if (pending) {
            return (<InvitedRole>
          <icons_1.IconMail size="md"/>
          {expired ? locale_1.t('Expired Invite') : locale_1.tct('Invited [roleName]', { roleName: roleName })}
        </InvitedRole>);
        }
        return roleName;
    };
    OrganizationMemberRow.prototype.render = function () {
        var _a = this.props, params = _a.params, routes = _a.routes, member = _a.member, orgName = _a.orgName, status = _a.status, requireLink = _a.requireLink, memberCanLeave = _a.memberCanLeave, currentUser = _a.currentUser, canRemoveMembers = _a.canRemoveMembers, canAddMembers = _a.canAddMembers;
        var id = member.id, flags = member.flags, email = member.email, name = member.name, pending = member.pending, user = member.user;
        // if member is not the only owner, they can leave
        var needsSso = !flags['sso:linked'] && requireLink;
        var isCurrentUser = currentUser.email === email;
        var showRemoveButton = !isCurrentUser;
        var showLeaveButton = isCurrentUser;
        var canRemoveMember = canRemoveMembers && !isCurrentUser;
        // member has a `user` property if they are registered with sentry
        // i.e. has accepted an invite to join org
        var has2fa = user && user.has2fa;
        var detailsUrl = recreateRoute_1.default(id, { routes: routes, params: params });
        var isInviteSuccessful = status === 'success';
        var isInviting = status === 'loading';
        var showResendButton = pending || needsSso;
        return (<StyledPanelItem data-test-id={email}>
        <MemberHeading>
          <userAvatar_1.default size={32} user={user !== null && user !== void 0 ? user : { id: email, email: email }}/>
          <MemberDescription to={detailsUrl}>
            <h5 style={{ margin: '0 0 3px' }}>
              <UserName>{name}</UserName>
            </h5>
            <Email>{email}</Email>
          </MemberDescription>
        </MemberHeading>

        <div data-test-id="member-role">{this.renderMemberRole()}</div>

        <div data-test-id="member-status">
          {showResendButton ? (<react_1.Fragment>
              {isInviting && (<LoadingContainer>
                  <loadingIndicator_1.default mini/>
                </LoadingContainer>)}
              {isInviteSuccessful && <span>{locale_1.t('Sent!')}</span>}
              {!isInviting && !isInviteSuccessful && (<button_1.default disabled={!canAddMembers} priority="primary" size="small" onClick={this.handleSendInvite}>
                  {pending ? locale_1.t('Resend invite') : locale_1.t('Resend SSO link')}
                </button_1.default>)}
            </react_1.Fragment>) : (<AuthStatus>
              {has2fa ? (<icons_1.IconCheckmark isCircled color="success"/>) : (<icons_1.IconFlag color="error"/>)}
              {has2fa ? locale_1.t('2FA Enabled') : locale_1.t('2FA Not Enabled')}
            </AuthStatus>)}
        </div>

        {showRemoveButton || showLeaveButton ? (<div>
            {showRemoveButton && canRemoveMember && (<confirm_1.default message={locale_1.tct('Are you sure you want to remove [name] from [orgName]?', {
                        name: name,
                        orgName: orgName,
                    })} onConfirm={this.handleRemove}>
                <button_1.default data-test-id="remove" icon={<icons_1.IconSubtract isCircled size="xs"/>} size="small" busy={this.state.busy}>
                  {locale_1.t('Remove')}
                </button_1.default>
              </confirm_1.default>)}

            {showRemoveButton && !canRemoveMember && (<button_1.default disabled size="small" title={locale_1.t('You do not have access to remove members')} icon={<icons_1.IconSubtract isCircled size="xs"/>}>
                {locale_1.t('Remove')}
              </button_1.default>)}

            {showLeaveButton && memberCanLeave && (<confirm_1.default message={locale_1.tct('Are you sure you want to leave [orgName]?', {
                        orgName: orgName,
                    })} onConfirm={this.handleLeave}>
                <button_1.default priority="danger" size="small" icon={<icons_1.IconClose size="xs"/>}>
                  {locale_1.t('Leave')}
                </button_1.default>
              </confirm_1.default>)}

            {showLeaveButton && !memberCanLeave && (<button_1.default size="small" icon={<icons_1.IconClose size="xs"/>} disabled title={locale_1.t('You cannot leave this organization as you are the only organization owner.')}>
                {locale_1.t('Leave')}
              </button_1.default>)}
          </div>) : null}
      </StyledPanelItem>);
    };
    return OrganizationMemberRow;
}(react_1.PureComponent));
exports.default = OrganizationMemberRow;
var StyledPanelItem = styled_1.default(panels_1.PanelItem)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: minmax(150px, 2fr) minmax(90px, 1fr) minmax(120px, 1fr) 90px;\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  display: grid;\n  grid-template-columns: minmax(150px, 2fr) minmax(90px, 1fr) minmax(120px, 1fr) 90px;\n  grid-gap: ", ";\n  align-items: center;\n"])), space_1.default(2));
var Section = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: inline-grid;\n  grid-template-columns: max-content auto;\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  display: inline-grid;\n  grid-template-columns: max-content auto;\n  grid-gap: ", ";\n  align-items: center;\n"])), space_1.default(1));
var MemberHeading = styled_1.default(Section)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject([""], [""])));
var MemberDescription = styled_1.default(link_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  overflow: hidden;\n"], ["\n  overflow: hidden;\n"])));
var UserName = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: block;\n  font-size: ", ";\n  overflow: hidden;\n  text-overflow: ellipsis;\n"], ["\n  display: block;\n  font-size: ", ";\n  overflow: hidden;\n  text-overflow: ellipsis;\n"])), function (p) { return p.theme.fontSizeLarge; });
var Email = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  overflow: hidden;\n  text-overflow: ellipsis;\n"], ["\n  color: ", ";\n  font-size: ", ";\n  overflow: hidden;\n  text-overflow: ellipsis;\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.fontSizeMedium; });
var InvitedRole = styled_1.default(Section)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject([""], [""])));
var LoadingContainer = styled_1.default('div')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  margin-top: 0;\n  margin-bottom: ", ";\n"], ["\n  margin-top: 0;\n  margin-bottom: ", ";\n"])), space_1.default(1.5));
var AuthStatus = styled_1.default(Section)(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject([""], [""])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=organizationMemberRow.jsx.map