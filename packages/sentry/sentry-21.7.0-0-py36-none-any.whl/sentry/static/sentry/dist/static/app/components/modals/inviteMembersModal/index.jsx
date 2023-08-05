Object.defineProperty(exports, "__esModule", { value: true });
exports.modalCss = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var hookOrDefault_1 = tslib_1.__importDefault(require("app/components/hookOrDefault"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var constants_1 = require("app/constants");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var guid_1 = require("app/utils/guid");
var withLatestContext_1 = tslib_1.__importDefault(require("app/utils/withLatestContext"));
var withTeams_1 = tslib_1.__importDefault(require("app/utils/withTeams"));
var inviteRowControl_1 = tslib_1.__importDefault(require("./inviteRowControl"));
var DEFAULT_ROLE = 'member';
var InviteModalHook = hookOrDefault_1.default({
    hookName: 'member-invite-modal:customization',
    defaultComponent: function (_a) {
        var onSendInvites = _a.onSendInvites, children = _a.children;
        return children({ sendInvites: onSendInvites, canSend: true });
    },
});
var InviteMembersModal = /** @class */ (function (_super) {
    tslib_1.__extends(InviteMembersModal, _super);
    function InviteMembersModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * Used for analytics tracking of the modals usage.
         */
        _this.sessionId = '';
        _this.reset = function () {
            _this.setState({
                pendingInvites: [_this.inviteTemplate],
                inviteStatus: {},
                complete: false,
                sendingInvites: false,
            });
            analytics_1.trackAnalyticsEvent({
                eventKey: 'invite_modal.add_more',
                eventName: 'Invite Modal: Add More',
                organization_id: _this.props.organization.id,
                modal_session: _this.sessionId,
            });
        };
        _this.sendInvite = function (invite) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var slug, data, endpoint, err_1, errorResponse, emailError, error_1;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        slug = this.props.organization.slug;
                        data = {
                            email: invite.email,
                            teams: tslib_1.__spreadArray([], tslib_1.__read(invite.teams)),
                            role: invite.role,
                        };
                        this.setState(function (state) {
                            var _a;
                            return ({
                                inviteStatus: tslib_1.__assign(tslib_1.__assign({}, state.inviteStatus), (_a = {}, _a[invite.email] = { sent: false }, _a)),
                            });
                        });
                        endpoint = this.willInvite
                            ? "/organizations/" + slug + "/members/"
                            : "/organizations/" + slug + "/invite-requests/";
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise(endpoint, { method: 'POST', data: data })];
                    case 2:
                        _a.sent();
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _a.sent();
                        errorResponse = err_1.responseJSON;
                        emailError = !errorResponse || !errorResponse.email
                            ? false
                            : Array.isArray(errorResponse.email)
                                ? errorResponse.email[0]
                                : errorResponse.email;
                        error_1 = emailError || locale_1.t('Could not invite user');
                        this.setState(function (state) {
                            var _a;
                            return ({
                                inviteStatus: tslib_1.__assign(tslib_1.__assign({}, state.inviteStatus), (_a = {}, _a[invite.email] = { sent: false, error: error_1 }, _a)),
                            });
                        });
                        return [2 /*return*/];
                    case 4:
                        this.setState(function (state) {
                            var _a;
                            return ({
                                inviteStatus: tslib_1.__assign(tslib_1.__assign({}, state.inviteStatus), (_a = {}, _a[invite.email] = { sent: true }, _a)),
                            });
                        });
                        return [2 /*return*/];
                }
            });
        }); };
        _this.sendInvites = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        this.setState({ sendingInvites: true });
                        return [4 /*yield*/, Promise.all(this.invites.map(this.sendInvite))];
                    case 1:
                        _a.sent();
                        this.setState({ sendingInvites: false, complete: true });
                        analytics_1.trackAnalyticsEvent({
                            eventKey: this.willInvite
                                ? 'invite_modal.invites_sent'
                                : 'invite_modal.requests_sent',
                            eventName: this.willInvite
                                ? 'Invite Modal: Invites Sent'
                                : 'Invite Modal: Requests Sent',
                            organization_id: this.props.organization.id,
                            modal_session: this.sessionId,
                        });
                        return [2 /*return*/];
                }
            });
        }); };
        _this.addInviteRow = function () {
            return _this.setState(function (state) { return ({
                pendingInvites: tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(state.pendingInvites)), [_this.inviteTemplate]),
            }); });
        };
        return _this;
    }
    Object.defineProperty(InviteMembersModal.prototype, "inviteTemplate", {
        get: function () {
            return {
                emails: new Set(),
                teams: new Set(),
                role: DEFAULT_ROLE,
            };
        },
        enumerable: false,
        configurable: true
    });
    InviteMembersModal.prototype.componentDidMount = function () {
        this.sessionId = guid_1.uniqueId();
        var _a = this.props, organization = _a.organization, source = _a.source;
        analytics_1.trackAnalyticsEvent({
            eventKey: 'invite_modal.opened',
            eventName: 'Invite Modal: Opened',
            organization_id: organization.id,
            modal_session: this.sessionId,
            can_invite: this.willInvite,
            source: source,
        });
    };
    InviteMembersModal.prototype.getEndpoints = function () {
        var orgId = this.props.organization.slug;
        return [['member', "/organizations/" + orgId + "/members/me/"]];
    };
    InviteMembersModal.prototype.getDefaultState = function () {
        var _this = this;
        var state = _super.prototype.getDefaultState.call(this);
        var initialData = this.props.initialData;
        var pendingInvites = initialData
            ? initialData.map(function (initial) { return (tslib_1.__assign(tslib_1.__assign({}, _this.inviteTemplate), initial)); })
            : [this.inviteTemplate];
        return tslib_1.__assign(tslib_1.__assign({}, state), { pendingInvites: pendingInvites, inviteStatus: {}, complete: false, sendingInvites: false });
    };
    InviteMembersModal.prototype.setEmails = function (emails, index) {
        this.setState(function (state) {
            var pendingInvites = tslib_1.__spreadArray([], tslib_1.__read(state.pendingInvites));
            pendingInvites[index] = tslib_1.__assign(tslib_1.__assign({}, pendingInvites[index]), { emails: new Set(emails) });
            return { pendingInvites: pendingInvites };
        });
    };
    InviteMembersModal.prototype.setTeams = function (teams, index) {
        this.setState(function (state) {
            var pendingInvites = tslib_1.__spreadArray([], tslib_1.__read(state.pendingInvites));
            pendingInvites[index] = tslib_1.__assign(tslib_1.__assign({}, pendingInvites[index]), { teams: new Set(teams) });
            return { pendingInvites: pendingInvites };
        });
    };
    InviteMembersModal.prototype.setRole = function (role, index) {
        this.setState(function (state) {
            var pendingInvites = tslib_1.__spreadArray([], tslib_1.__read(state.pendingInvites));
            pendingInvites[index] = tslib_1.__assign(tslib_1.__assign({}, pendingInvites[index]), { role: role });
            return { pendingInvites: pendingInvites };
        });
    };
    InviteMembersModal.prototype.removeInviteRow = function (index) {
        this.setState(function (state) {
            var pendingInvites = tslib_1.__spreadArray([], tslib_1.__read(state.pendingInvites));
            pendingInvites.splice(index, 1);
            return { pendingInvites: pendingInvites };
        });
    };
    Object.defineProperty(InviteMembersModal.prototype, "invites", {
        get: function () {
            return this.state.pendingInvites.reduce(function (acc, row) { return tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(acc)), tslib_1.__read(tslib_1.__spreadArray([], tslib_1.__read(row.emails)).map(function (email) { return ({ email: email, teams: row.teams, role: row.role }); }))); }, []);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(InviteMembersModal.prototype, "hasDuplicateEmails", {
        get: function () {
            var emails = this.invites.map(function (inv) { return inv.email; });
            return emails.length !== new Set(emails).size;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(InviteMembersModal.prototype, "isValidInvites", {
        get: function () {
            return this.invites.length > 0 && !this.hasDuplicateEmails;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(InviteMembersModal.prototype, "statusMessage", {
        get: function () {
            var _a = this.state, sendingInvites = _a.sendingInvites, complete = _a.complete, inviteStatus = _a.inviteStatus;
            if (sendingInvites) {
                return (<StatusMessage>
          <loadingIndicator_1.default mini relative hideMessage size={16}/>
          {this.willInvite
                        ? locale_1.t('Sending organization invitations...')
                        : locale_1.t('Sending invite requests...')}
        </StatusMessage>);
            }
            if (complete) {
                var statuses = Object.values(inviteStatus);
                var sentCount = statuses.filter(function (i) { return i.sent; }).length;
                var errorCount = statuses.filter(function (i) { return i.error; }).length;
                var invites = <strong>{locale_1.tn('%s invite', '%s invites', sentCount)}</strong>;
                var tctComponents = {
                    invites: invites,
                    failed: errorCount,
                };
                return (<StatusMessage status="success">
          <icons_1.IconCheckmark size="sm"/>
          {errorCount > 0
                        ? locale_1.tct('Sent [invites], [failed] failed to send.', tctComponents)
                        : locale_1.tct('Sent [invites]', tctComponents)}
        </StatusMessage>);
            }
            if (this.hasDuplicateEmails) {
                return (<StatusMessage status="error">
          <icons_1.IconWarning size="sm"/>
          {locale_1.t('Duplicate emails between invite rows.')}
        </StatusMessage>);
            }
            return null;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(InviteMembersModal.prototype, "willInvite", {
        get: function () {
            var _a;
            return (_a = this.props.organization.access) === null || _a === void 0 ? void 0 : _a.includes('member:write');
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(InviteMembersModal.prototype, "inviteButtonLabel", {
        get: function () {
            if (this.invites.length > 0) {
                var numberInvites = this.invites.length;
                // Note we use `t()` here because `tn()` expects the same # of string formatters
                var inviteText = numberInvites === 1 ? locale_1.t('Send invite') : locale_1.t('Send invites (%s)', numberInvites);
                var requestText = numberInvites === 1
                    ? locale_1.t('Send invite request')
                    : locale_1.t('Send invite requests (%s)', numberInvites);
                return this.willInvite ? inviteText : requestText;
            }
            return this.willInvite ? locale_1.t('Send invite') : locale_1.t('Send invite request');
        },
        enumerable: false,
        configurable: true
    });
    InviteMembersModal.prototype.render = function () {
        var _this = this;
        var _a = this.props, Footer = _a.Footer, closeModal = _a.closeModal, organization = _a.organization, allTeams = _a.teams;
        var _b = this.state, pendingInvites = _b.pendingInvites, sendingInvites = _b.sendingInvites, complete = _b.complete, inviteStatus = _b.inviteStatus, member = _b.member;
        var disableInputs = sendingInvites || complete;
        // eslint-disable-next-line react/prop-types
        var hookRenderer = function (_a) {
            var sendInvites = _a.sendInvites, canSend = _a.canSend, headerInfo = _a.headerInfo;
            return (<React.Fragment>
        <Heading>
          {locale_1.t('Invite New Members')}
          {!_this.willInvite && (<questionTooltip_1.default title={locale_1.t("You do not have permission to directly invite members. Email\n                 addresses entered here will be forwarded to organization\n                 managers and owners; they will be prompted to approve the\n                 invitation.")} size="sm" position="bottom"/>)}
        </Heading>
        <Subtext>
          {_this.willInvite
                    ? locale_1.t('Invite new members by email to join your organization.')
                    : locale_1.t("You don\u2019t have permission to directly invite users, but we'll send a request to your organization owner and manager for review.")}
        </Subtext>

        {headerInfo}

        <InviteeHeadings>
          <div>{locale_1.t('Email addresses')}</div>
          <div>{locale_1.t('Role')}</div>
          <div>{locale_1.t('Add to team')}</div>
        </InviteeHeadings>

        {pendingInvites.map(function (_a, i) {
                    var emails = _a.emails, role = _a.role, teams = _a.teams;
                    return (<StyledInviteRow key={i} disabled={disableInputs} emails={tslib_1.__spreadArray([], tslib_1.__read(emails))} role={role} teams={tslib_1.__spreadArray([], tslib_1.__read(teams))} roleOptions={member ? member.roles : constants_1.MEMBER_ROLES} roleDisabledUnallowed={_this.willInvite} teamOptions={allTeams} inviteStatus={inviteStatus} onRemove={function () { return _this.removeInviteRow(i); }} onChangeEmails={function (opts) { var _a; return _this.setEmails((_a = opts === null || opts === void 0 ? void 0 : opts.map(function (v) { return v.value; })) !== null && _a !== void 0 ? _a : [], i); }} onChangeRole={function (value) { return _this.setRole(value === null || value === void 0 ? void 0 : value.value, i); }} onChangeTeams={function (opts) { return _this.setTeams(opts ? opts.map(function (v) { return v.value; }) : [], i); }} disableRemove={disableInputs || pendingInvites.length === 1}/>);
                })}

        <AddButton disabled={disableInputs} priority="link" onClick={_this.addInviteRow} icon={<icons_1.IconAdd size="xs" isCircled/>}>
          {locale_1.t('Add another')}
        </AddButton>

        <Footer>
          <FooterContent>
            <div>{_this.statusMessage}</div>

            {complete ? (<React.Fragment>
                <button_1.default data-test-id="send-more" size="small" onClick={_this.reset}>
                  {locale_1.t('Send more invites')}
                </button_1.default>
                <button_1.default data-test-id="close" priority="primary" size="small" onClick={function () {
                        analytics_1.trackAnalyticsEvent({
                            eventKey: 'invite_modal.closed',
                            eventName: 'Invite Modal: Closed',
                            organization_id: _this.props.organization.id,
                            modal_session: _this.sessionId,
                        });
                        closeModal();
                    }}>
                  {locale_1.t('Close')}
                </button_1.default>
              </React.Fragment>) : (<React.Fragment>
                <button_1.default data-test-id="cancel" size="small" onClick={closeModal} disabled={disableInputs}>
                  {locale_1.t('Cancel')}
                </button_1.default>
                <button_1.default size="small" data-test-id="send-invites" priority="primary" disabled={!canSend || !_this.isValidInvites || disableInputs} onClick={sendInvites}>
                  {_this.inviteButtonLabel}
                </button_1.default>
              </React.Fragment>)}
          </FooterContent>
        </Footer>
      </React.Fragment>);
        };
        return (<InviteModalHook organization={organization} willInvite={this.willInvite} onSendInvites={this.sendInvites}>
        {hookRenderer}
      </InviteModalHook>);
    };
    return InviteMembersModal;
}(asyncComponent_1.default));
var Heading = styled_1.default('h1')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: inline-grid;\n  grid-gap: ", ";\n  grid-auto-flow: column;\n  align-items: center;\n  font-weight: 400;\n  font-size: ", ";\n  margin-top: 0;\n  margin-bottom: ", ";\n"], ["\n  display: inline-grid;\n  grid-gap: ", ";\n  grid-auto-flow: column;\n  align-items: center;\n  font-weight: 400;\n  font-size: ", ";\n  margin-top: 0;\n  margin-bottom: ", ";\n"])), space_1.default(1.5), function (p) { return p.theme.headerFontSize; }, space_1.default(0.75));
var Subtext = styled_1.default('p')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  margin-bottom: ", ";\n"], ["\n  color: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.subText; }, space_1.default(3));
var inviteRowGrid = react_1.css(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: 3fr 180px 2fr max-content;\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: 3fr 180px 2fr max-content;\n"])), space_1.default(1.5));
var InviteeHeadings = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  ", ";\n\n  margin-bottom: ", ";\n  font-weight: 600;\n  text-transform: uppercase;\n  font-size: ", ";\n"], ["\n  ", ";\n\n  margin-bottom: ", ";\n  font-weight: 600;\n  text-transform: uppercase;\n  font-size: ", ";\n"])), inviteRowGrid, space_1.default(1), function (p) { return p.theme.fontSizeSmall; });
var StyledInviteRow = styled_1.default(inviteRowControl_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  ", ";\n  margin-bottom: ", ";\n"], ["\n  ", ";\n  margin-bottom: ", ";\n"])), inviteRowGrid, space_1.default(1.5));
var AddButton = styled_1.default(button_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space_1.default(3));
var FooterContent = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  width: 100%;\n  display: grid;\n  grid-template-columns: 1fr max-content max-content;\n  grid-gap: ", ";\n"], ["\n  width: 100%;\n  display: grid;\n  grid-template-columns: 1fr max-content max-content;\n  grid-gap: ", ";\n"])), space_1.default(1));
var StatusMessage = styled_1.default('div')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content max-content;\n  grid-gap: ", ";\n  align-items: center;\n  font-size: ", ";\n  color: ", ";\n\n  > :first-child {\n    ", ";\n  }\n"], ["\n  display: grid;\n  grid-template-columns: max-content max-content;\n  grid-gap: ", ";\n  align-items: center;\n  font-size: ", ";\n  color: ", ";\n\n  > :first-child {\n    ", ";\n  }\n"])), space_1.default(1), function (p) { return p.theme.fontSizeMedium; }, function (p) { return (p.status === 'error' ? p.theme.red300 : p.theme.gray400); }, function (p) { return p.status === 'success' && "color: " + p.theme.green300; });
exports.modalCss = react_1.css(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  width: 100%;\n  max-width: 800px;\n  margin: 50px auto;\n"], ["\n  width: 100%;\n  max-width: 800px;\n  margin: 50px auto;\n"])));
exports.default = withLatestContext_1.default(withTeams_1.default(InviteMembersModal));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=index.jsx.map