Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var utils_1 = require("@sentry/utils");
var account_1 = require("app/actionCreators/account");
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var narrowLayout_1 = tslib_1.__importDefault(require("app/components/narrowLayout"));
var locale_1 = require("app/locale");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var AcceptOrganizationInvite = /** @class */ (function (_super) {
    tslib_1.__extends(AcceptOrganizationInvite, _super);
    function AcceptOrganizationInvite() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleLogout = function (e) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        e.preventDefault();
                        return [4 /*yield*/, account_1.logout(this.api)];
                    case 1:
                        _a.sent();
                        window.location.replace(this.makeNextUrl('/auth/login/'));
                        return [2 /*return*/];
                }
            });
        }); };
        _this.handleAcceptInvite = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, memberId, token, _b;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props.params, memberId = _a.memberId, token = _a.token;
                        this.setState({ accepting: true });
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/accept-invite/" + memberId + "/" + token + "/", {
                                method: 'POST',
                            })];
                    case 2:
                        _c.sent();
                        react_router_1.browserHistory.replace("/" + this.state.inviteDetails.orgSlug + "/");
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        this.setState({ acceptError: true });
                        return [3 /*break*/, 4];
                    case 4:
                        this.setState({ accepting: false });
                        return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    AcceptOrganizationInvite.prototype.getEndpoints = function () {
        var _a = this.props.params, memberId = _a.memberId, token = _a.token;
        return [['inviteDetails', "/accept-invite/" + memberId + "/" + token + "/"]];
    };
    AcceptOrganizationInvite.prototype.getTitle = function () {
        return locale_1.t('Accept Organization Invite');
    };
    AcceptOrganizationInvite.prototype.makeNextUrl = function (path) {
        return path + "?" + utils_1.urlEncode({ next: window.location.pathname });
    };
    Object.defineProperty(AcceptOrganizationInvite.prototype, "existingMemberAlert", {
        get: function () {
            var user = configStore_1.default.get('user');
            return (<alert_1.default type="warning" data-test-id="existing-member">
        {locale_1.tct('Your account ([email]) is already a member of this organization. [switchLink:Switch accounts]?', {
                    email: user.email,
                    switchLink: (<link_1.default to="" data-test-id="existing-member-link" onClick={this.handleLogout}/>),
                })}
      </alert_1.default>);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(AcceptOrganizationInvite.prototype, "authenticationActions", {
        get: function () {
            var inviteDetails = this.state.inviteDetails;
            return (<react_1.Fragment>
        {!inviteDetails.requireSso && (<p data-test-id="action-info-general">
            {locale_1.t("To continue, you must either create a new account, or login to an\n              existing Sentry account.")}
          </p>)}

        {inviteDetails.needsSso && (<p data-test-id="action-info-sso">
            {inviteDetails.requireSso
                        ? locale_1.tct("Note that [orgSlug] has required Single Sign-On (SSO) using\n               [authProvider]. You may create an account by authenticating with\n               the organization's SSO provider.", {
                            orgSlug: <strong>{inviteDetails.orgSlug}</strong>,
                            authProvider: inviteDetails.ssoProvider,
                        })
                        : locale_1.tct("Note that [orgSlug] has enabled Single Sign-On (SSO) using\n               [authProvider]. You may create an account by authenticating with\n               the organization's SSO provider.", {
                            orgSlug: <strong>{inviteDetails.orgSlug}</strong>,
                            authProvider: inviteDetails.ssoProvider,
                        })}
          </p>)}

        <Actions>
          <ActionsLeft>
            {inviteDetails.needsSso && (<button_1.default label="sso-login" priority="primary" href={this.makeNextUrl("/auth/login/" + inviteDetails.orgSlug + "/")}>
                {locale_1.t('Join with %s', inviteDetails.ssoProvider)}
              </button_1.default>)}
            {!inviteDetails.requireSso && (<button_1.default label="create-account" priority="primary" href={this.makeNextUrl('/auth/register/')}>
                {locale_1.t('Create a new account')}
              </button_1.default>)}
          </ActionsLeft>
          {!inviteDetails.requireSso && (<externalLink_1.default href={this.makeNextUrl('/auth/login/')} openInNewTab={false} data-test-id="link-with-existing">
              {locale_1.t('Login using an existing account')}
            </externalLink_1.default>)}
        </Actions>
      </react_1.Fragment>);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(AcceptOrganizationInvite.prototype, "warning2fa", {
        get: function () {
            var inviteDetails = this.state.inviteDetails;
            return (<react_1.Fragment>
        <p data-test-id="2fa-warning">
          {locale_1.tct('To continue, [orgSlug] requires all members to configure two-factor authentication.', { orgSlug: inviteDetails.orgSlug })}
        </p>
        <Actions>
          <button_1.default priority="primary" to="/settings/account/security/">
            {locale_1.t('Configure Two-Factor Auth')}
          </button_1.default>
        </Actions>
      </react_1.Fragment>);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(AcceptOrganizationInvite.prototype, "warningEmailVerification", {
        get: function () {
            var inviteDetails = this.state.inviteDetails;
            return (<react_1.Fragment>
        <p data-test-id="email-verification-warning">
          {locale_1.tct('To continue, [orgSlug] requires all members to verify their email address.', { orgSlug: inviteDetails.orgSlug })}
        </p>
        <Actions>
          <button_1.default priority="primary" to="/settings/account/emails/">
            {locale_1.t('Verify Email Address')}
          </button_1.default>
        </Actions>
      </react_1.Fragment>);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(AcceptOrganizationInvite.prototype, "acceptActions", {
        get: function () {
            var _a = this.state, inviteDetails = _a.inviteDetails, accepting = _a.accepting;
            return (<Actions>
        <button_1.default label="join-organization" priority="primary" disabled={accepting} onClick={this.handleAcceptInvite}>
          {locale_1.t('Join the %s organization', inviteDetails.orgSlug)}
        </button_1.default>
      </Actions>);
        },
        enumerable: false,
        configurable: true
    });
    AcceptOrganizationInvite.prototype.renderError = function () {
        return (<narrowLayout_1.default>
        <alert_1.default type="warning">
          {locale_1.t('This organization invite link is no longer valid.')}
        </alert_1.default>
      </narrowLayout_1.default>);
    };
    AcceptOrganizationInvite.prototype.renderBody = function () {
        var _a = this.state, inviteDetails = _a.inviteDetails, acceptError = _a.acceptError;
        return (<narrowLayout_1.default>
        <settingsPageHeader_1.default title={locale_1.t('Accept organization invite')}/>
        {acceptError && (<alert_1.default type="error">
            {locale_1.t('Failed to join this organization. Please try again')}
          </alert_1.default>)}
        <InviteDescription data-test-id="accept-invite">
          {locale_1.tct('[orgSlug] is using Sentry to track and debug errors.', {
                orgSlug: <strong>{inviteDetails.orgSlug}</strong>,
            })}
        </InviteDescription>
        {inviteDetails.needsAuthentication
                ? this.authenticationActions
                : inviteDetails.existingMember
                    ? this.existingMemberAlert
                    : inviteDetails.needs2fa
                        ? this.warning2fa
                        : inviteDetails.needsEmailVerification
                            ? this.warningEmailVerification
                            : this.acceptActions}
      </narrowLayout_1.default>);
    };
    return AcceptOrganizationInvite;
}(asyncView_1.default));
var Actions = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n"])), space_1.default(3));
var ActionsLeft = styled_1.default('span')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  > a {\n    margin-right: ", ";\n  }\n"], ["\n  > a {\n    margin-right: ", ";\n  }\n"])), space_1.default(1));
var InviteDescription = styled_1.default('p')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  font-size: 1.2em;\n"], ["\n  font-size: 1.2em;\n"])));
exports.default = AcceptOrganizationInvite;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=acceptOrganizationInvite.jsx.map