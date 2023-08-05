Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var modal_1 = require("app/actionCreators/modal");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var circleIndicator_1 = tslib_1.__importDefault(require("app/components/circleIndicator"));
var listLink_1 = tslib_1.__importDefault(require("app/components/links/listLink"));
var navTabs_1 = tslib_1.__importDefault(require("app/components/navTabs"));
var panels_1 = require("app/components/panels");
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var recreateRoute_1 = tslib_1.__importDefault(require("app/utils/recreateRoute"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var removeConfirm_1 = tslib_1.__importDefault(require("app/views/settings/account/accountSecurity/components/removeConfirm"));
var twoFactorRequired_1 = tslib_1.__importDefault(require("app/views/settings/account/accountSecurity/components/twoFactorRequired"));
var passwordForm_1 = tslib_1.__importDefault(require("app/views/settings/account/passwordForm"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var field_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
/**
 * Lists 2fa devices + password change form
 */
var AccountSecurity = /** @class */ (function (_super) {
    tslib_1.__extends(AccountSecurity, _super);
    function AccountSecurity() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSessionClose = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var err_1;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        _a.trys.push([0, 2, , 3]);
                        return [4 /*yield*/, this.api.requestPromise('/auth/', {
                                method: 'DELETE',
                                data: { all: true },
                            })];
                    case 1:
                        _a.sent();
                        window.location.assign('/auth/login/');
                        return [3 /*break*/, 3];
                    case 2:
                        err_1 = _a.sent();
                        indicator_1.addErrorMessage(locale_1.t('There was a problem closing all sessions'));
                        throw err_1;
                    case 3: return [2 /*return*/];
                }
            });
        }); };
        _this.formatOrgSlugs = function () {
            var orgsRequire2fa = _this.props.orgsRequire2fa;
            var slugs = orgsRequire2fa.map(function (_a) {
                var slug = _a.slug;
                return slug;
            });
            return [slugs.slice(0, -1).join(', '), slugs.slice(-1)[0]].join(slugs.length > 1 ? ' and ' : '');
        };
        _this.handleAdd2FAClicked = function () {
            var handleRefresh = _this.props.handleRefresh;
            modal_1.openEmailVerification({
                onClose: function () {
                    handleRefresh();
                },
                actionMessage: 'enrolling a 2FA device',
            });
        };
        return _this;
    }
    AccountSecurity.prototype.getTitle = function () {
        return locale_1.t('Security');
    };
    AccountSecurity.prototype.getEndpoints = function () {
        return [];
    };
    AccountSecurity.prototype.renderBody = function () {
        var _this = this;
        var _a = this.props, authenticators = _a.authenticators, countEnrolled = _a.countEnrolled, deleteDisabled = _a.deleteDisabled, onDisable = _a.onDisable, hasVerifiedEmail = _a.hasVerifiedEmail;
        var isEmpty = !(authenticators === null || authenticators === void 0 ? void 0 : authenticators.length);
        return (<div>
        <settingsPageHeader_1.default title={locale_1.t('Security')} tabs={<navTabs_1.default underlined>
              <listLink_1.default to={recreateRoute_1.default('', this.props)} index>
                {locale_1.t('Settings')}
              </listLink_1.default>
              <listLink_1.default to={recreateRoute_1.default('session-history/', this.props)}>
                {locale_1.t('Session History')}
              </listLink_1.default>
            </navTabs_1.default>}/>

        {!isEmpty && countEnrolled === 0 && <twoFactorRequired_1.default />}

        <passwordForm_1.default />

        <panels_1.Panel>
          <panels_1.PanelHeader>{locale_1.t('Sessions')}</panels_1.PanelHeader>
          <panels_1.PanelBody>
            <field_1.default alignRight flexibleControlStateSize label={locale_1.t('Sign out of all devices')} help={locale_1.t('Signing out of all devices will sign you out of this device as well.')}>
              <button_1.default data-test-id="signoutAll" onClick={this.handleSessionClose}>
                {locale_1.t('Sign out of all devices')}
              </button_1.default>
            </field_1.default>
          </panels_1.PanelBody>
        </panels_1.Panel>

        <panels_1.Panel>
          <panels_1.PanelHeader>{locale_1.t('Two-Factor Authentication')}</panels_1.PanelHeader>

          {isEmpty && (<emptyMessage_1.default>{locale_1.t('No available authenticators to add')}</emptyMessage_1.default>)}

          <panels_1.PanelBody>
            {!isEmpty &&
                (authenticators === null || authenticators === void 0 ? void 0 : authenticators.map(function (auth) {
                    var id = auth.id, authId = auth.authId, description = auth.description, isBackupInterface = auth.isBackupInterface, isEnrolled = auth.isEnrolled, configureButton = auth.configureButton, name = auth.name;
                    return (<AuthenticatorPanelItem key={id}>
                    <AuthenticatorHeader>
                      <AuthenticatorTitle>
                        <AuthenticatorStatus enabled={isEnrolled}/>
                        <AuthenticatorName>{name}</AuthenticatorName>
                      </AuthenticatorTitle>

                      <Actions>
                        {!isBackupInterface && !isEnrolled && hasVerifiedEmail && (<button_1.default to={"/settings/account/security/mfa/" + id + "/enroll/"} size="small" priority="primary" className="enroll-button">
                            {locale_1.t('Add')}
                          </button_1.default>)}
                        {!isBackupInterface && !isEnrolled && !hasVerifiedEmail && (<button_1.default onClick={_this.handleAdd2FAClicked} size="small" priority="primary" className="enroll-button">
                            {locale_1.t('Add')}
                          </button_1.default>)}

                        {isEnrolled && authId && (<button_1.default to={"/settings/account/security/mfa/" + authId + "/"} size="small" className="details-button">
                            {configureButton}
                          </button_1.default>)}

                        {!isBackupInterface && isEnrolled && (<tooltip_1.default title={locale_1.t("Two-factor authentication is required for organization(s): " + _this.formatOrgSlugs() + ".")} disabled={!deleteDisabled}>
                            <removeConfirm_1.default onConfirm={function () { return onDisable(auth); }} disabled={deleteDisabled}>
                              <button_1.default size="small" label={locale_1.t('delete')} icon={<icons_1.IconDelete />}/>
                            </removeConfirm_1.default>
                          </tooltip_1.default>)}
                      </Actions>

                      {isBackupInterface && !isEnrolled ? locale_1.t('requires 2FA') : null}
                    </AuthenticatorHeader>

                    <Description>{description}</Description>
                  </AuthenticatorPanelItem>);
                }))}
          </panels_1.PanelBody>
        </panels_1.Panel>
      </div>);
    };
    return AccountSecurity;
}(asyncView_1.default));
var AuthenticatorName = styled_1.default('span')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-size: 1.2em;\n"], ["\n  font-size: 1.2em;\n"])));
var AuthenticatorPanelItem = styled_1.default(panels_1.PanelItem)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  flex-direction: column;\n"], ["\n  flex-direction: column;\n"])));
var AuthenticatorHeader = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  align-items: center;\n"], ["\n  display: flex;\n  flex: 1;\n  align-items: center;\n"])));
var AuthenticatorTitle = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var Actions = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n"])), space_1.default(1));
var AuthenticatorStatus = styled_1.default(circleIndicator_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(1));
var Description = styled_1.default(textBlock_1.default)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n  margin-bottom: 0;\n"], ["\n  margin-top: ", ";\n  margin-bottom: 0;\n"])), space_1.default(2));
exports.default = AccountSecurity;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=index.jsx.map