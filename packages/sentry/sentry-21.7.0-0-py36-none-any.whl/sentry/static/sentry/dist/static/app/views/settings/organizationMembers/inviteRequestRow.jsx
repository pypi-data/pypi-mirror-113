Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var multiSelectControl_1 = tslib_1.__importDefault(require("app/components/forms/multiSelectControl"));
var hookOrDefault_1 = tslib_1.__importDefault(require("app/components/hookOrDefault"));
var panels_1 = require("app/components/panels");
var roleSelectControl_1 = tslib_1.__importDefault(require("app/components/roleSelectControl"));
var tag_1 = tslib_1.__importDefault(require("app/components/tag"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var InviteModalHook = hookOrDefault_1.default({
    hookName: 'member-invite-modal:customization',
    defaultComponent: function (_a) {
        var onSendInvites = _a.onSendInvites, children = _a.children;
        return children({ sendInvites: onSendInvites, canSend: true });
    },
});
var InviteRequestRow = function (_a) {
    var inviteRequest = _a.inviteRequest, inviteRequestBusy = _a.inviteRequestBusy, organization = _a.organization, onApprove = _a.onApprove, onDeny = _a.onDeny, onUpdate = _a.onUpdate, allTeams = _a.allTeams, allRoles = _a.allRoles;
    var role = allRoles.find(function (r) { return r.id === inviteRequest.role; });
    var roleDisallowed = !(role && role.allowed);
    // eslint-disable-next-line react/prop-types
    var hookRenderer = function (_a) {
        var sendInvites = _a.sendInvites, canSend = _a.canSend, headerInfo = _a.headerInfo;
        return (<StyledPanelItem>
      <div>
        <h5 style={{ marginBottom: space_1.default(0.5) }}>
          <UserName>{inviteRequest.email}</UserName>
        </h5>
        {inviteRequest.inviteStatus === 'requested_to_be_invited' ? (inviteRequest.inviterName && (<Description>
              <tooltip_1.default title={locale_1.t('An existing member has asked to invite this user to your organization')}>
                {locale_1.tct('Requested by [inviterName]', {
                    inviterName: inviteRequest.inviterName,
                })}
              </tooltip_1.default>
            </Description>)) : (<JoinRequestIndicator tooltipText={locale_1.t('This user has asked to join your organization.')}>
            {locale_1.t('Join request')}
          </JoinRequestIndicator>)}
      </div>

      <StyledRoleSelectControl name="role" disableUnallowed onChange={function (r) { return onUpdate({ role: r.value }); }} value={inviteRequest.role} roles={allRoles}/>

      <TeamSelectControl name="teams" placeholder={locale_1.t('Add to teams\u2026')} onChange={function (teams) {
                return onUpdate({ teams: (teams || []).map(function (team) { return team.value; }) });
            }} value={inviteRequest.teams} options={allTeams.map(function (_a) {
                var slug = _a.slug;
                return ({
                    value: slug,
                    label: "#" + slug,
                });
            })} clearable/>

      <ButtonGroup>
        <confirm_1.default onConfirm={sendInvites} disableConfirmButton={!canSend} disabled={roleDisallowed} message={<React.Fragment>
              {locale_1.tct('Are you sure you want to invite [email] to your organization?', {
                    email: inviteRequest.email,
                })}
              {headerInfo}
            </React.Fragment>}>
          <button_1.default priority="primary" size="small" busy={inviteRequestBusy[inviteRequest.id]} title={roleDisallowed
                ? locale_1.t("You do not have permission to approve a user of this role.\n                     Select a different role to approve this user.")
                : undefined}>
            {locale_1.t('Approve')}
          </button_1.default>
        </confirm_1.default>
        <button_1.default size="small" busy={inviteRequestBusy[inviteRequest.id]} onClick={function () { return onDeny(inviteRequest); }}>
          {locale_1.t('Deny')}
        </button_1.default>
      </ButtonGroup>
    </StyledPanelItem>);
    };
    return (<InviteModalHook willInvite organization={organization} onSendInvites={function () { return onApprove(inviteRequest); }}>
      {hookRenderer}
    </InviteModalHook>);
};
var JoinRequestIndicator = styled_1.default(tag_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  text-transform: uppercase;\n"], ["\n  text-transform: uppercase;\n"])));
var StyledPanelItem = styled_1.default(panels_1.PanelItem)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: minmax(150px, auto) minmax(100px, 140px) 220px max-content;\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  display: grid;\n  grid-template-columns: minmax(150px, auto) minmax(100px, 140px) 220px max-content;\n  grid-gap: ", ";\n  align-items: center;\n"])), space_1.default(2));
var UserName = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  overflow: hidden;\n  text-overflow: ellipsis;\n"], ["\n  font-size: ", ";\n  overflow: hidden;\n  text-overflow: ellipsis;\n"])), function (p) { return p.theme.fontSizeLarge; });
var Description = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: block;\n  color: ", ";\n  font-size: 14px;\n  overflow: hidden;\n  text-overflow: ellipsis;\n"], ["\n  display: block;\n  color: ", ";\n  font-size: 14px;\n  overflow: hidden;\n  text-overflow: ellipsis;\n"])), function (p) { return p.theme.subText; });
var StyledRoleSelectControl = styled_1.default(roleSelectControl_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  max-width: 140px;\n"], ["\n  max-width: 140px;\n"])));
var TeamSelectControl = styled_1.default(multiSelectControl_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  max-width: 220px;\n  .Select-value-label {\n    max-width: 150px;\n    word-break: break-all;\n  }\n"], ["\n  max-width: 220px;\n  .Select-value-label {\n    max-width: 150px;\n    word-break: break-all;\n  }\n"])));
var ButtonGroup = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  display: inline-grid;\n  grid-template-columns: repeat(2, max-content);\n  grid-gap: ", ";\n"], ["\n  display: inline-grid;\n  grid-template-columns: repeat(2, max-content);\n  grid-gap: ", ";\n"])), space_1.default(1));
exports.default = InviteRequestRow;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=inviteRequestRow.jsx.map