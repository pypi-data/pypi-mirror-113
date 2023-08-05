Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
/**
 * AccountSecurityDetails is only displayed when user is enrolled in the 2fa method.
 * It displays created + last used time of the 2fa method.
 *
 * Also displays 2fa method specific details.
 */
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var circleIndicator_1 = tslib_1.__importDefault(require("app/components/circleIndicator"));
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var recoveryCodes_1 = tslib_1.__importDefault(require("app/views/settings/account/accountSecurity/components/recoveryCodes"));
var removeConfirm_1 = tslib_1.__importDefault(require("app/views/settings/account/accountSecurity/components/removeConfirm"));
var u2fEnrolledDetails_1 = tslib_1.__importDefault(require("app/views/settings/account/accountSecurity/components/u2fEnrolledDetails"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
var ENDPOINT = '/users/me/authenticators/';
function AuthenticatorDate(_a) {
    var label = _a.label, date = _a.date;
    return (<react_1.Fragment>
      <DateLabel>{label}</DateLabel>
      <div>{date ? <dateTime_1.default date={date}/> : locale_1.t('never')}</div>
    </react_1.Fragment>);
}
var AccountSecurityDetails = /** @class */ (function (_super) {
    tslib_1.__extends(AccountSecurityDetails, _super);
    function AccountSecurityDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleRemove = function (device) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var authenticator, deviceId, deviceName, _a;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        authenticator = this.state.authenticator;
                        if (!authenticator || !authenticator.authId) {
                            return [2 /*return*/];
                        }
                        deviceId = device ? device.key_handle + "/" : '';
                        deviceName = device ? device.name : locale_1.t('Authenticator');
                        this.setState({ loading: true });
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("" + ENDPOINT + authenticator.authId + "/" + deviceId, {
                                method: 'DELETE',
                            })];
                    case 2:
                        _b.sent();
                        this.props.router.push('/settings/account/security');
                        indicator_1.addSuccessMessage(locale_1.t('%s has been removed', deviceName));
                        return [3 /*break*/, 4];
                    case 3:
                        _a = _b.sent();
                        // Error deleting authenticator
                        this.setState({ loading: false });
                        indicator_1.addErrorMessage(locale_1.t('Error removing %s', deviceName));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    AccountSecurityDetails.prototype.getTitle = function () {
        return locale_1.t('Security');
    };
    AccountSecurityDetails.prototype.getEndpoints = function () {
        var params = this.props.params;
        var authId = params.authId;
        return [['authenticator', "" + ENDPOINT + authId + "/"]];
    };
    AccountSecurityDetails.prototype.renderBody = function () {
        var authenticator = this.state.authenticator;
        if (!authenticator) {
            return null;
        }
        var _a = this.props, deleteDisabled = _a.deleteDisabled, onRegenerateBackupCodes = _a.onRegenerateBackupCodes;
        return (<react_1.Fragment>
        <settingsPageHeader_1.default title={<react_1.Fragment>
              <span>{authenticator.name}</span>
              <AuthenticatorStatus enabled={authenticator.isEnrolled}/>
            </react_1.Fragment>} action={authenticator.isEnrolled &&
                authenticator.removeButton && (<tooltip_1.default title={locale_1.t("Two-factor authentication is required for at least one organization you're a member of.")} disabled={!deleteDisabled}>
                <removeConfirm_1.default onConfirm={this.handleRemove} disabled={deleteDisabled}>
                  <button_1.default priority="danger">{authenticator.removeButton}</button_1.default>
                </removeConfirm_1.default>
              </tooltip_1.default>)}/>

        <textBlock_1.default>{authenticator.description}</textBlock_1.default>

        <AuthenticatorDates>
          <AuthenticatorDate label={locale_1.t('Created at')} date={authenticator.createdAt}/>
          <AuthenticatorDate label={locale_1.t('Last used')} date={authenticator.lastUsedAt}/>
        </AuthenticatorDates>

        <u2fEnrolledDetails_1.default isEnrolled={authenticator.isEnrolled} id={authenticator.id} devices={authenticator.devices} onRemoveU2fDevice={this.handleRemove}/>

        {authenticator.isEnrolled && authenticator.phone && (<PhoneWrapper>
            {locale_1.t('Confirmation codes are sent to the following phone number')}:
            <Phone>{authenticator.phone}</Phone>
          </PhoneWrapper>)}

        <recoveryCodes_1.default onRegenerateBackupCodes={onRegenerateBackupCodes} isEnrolled={authenticator.isEnrolled} codes={authenticator.codes}/>
      </react_1.Fragment>);
    };
    return AccountSecurityDetails;
}(asyncView_1.default));
exports.default = AccountSecurityDetails;
var AuthenticatorStatus = styled_1.default(circleIndicator_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space_1.default(1));
var AuthenticatorDates = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: max-content auto;\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: max-content auto;\n"])), space_1.default(2));
var DateLabel = styled_1.default('span')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  font-weight: bold;\n"], ["\n  font-weight: bold;\n"])));
var PhoneWrapper = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space_1.default(4));
var Phone = styled_1.default('span')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  font-weight: bold;\n  margin-left: ", ";\n"], ["\n  font-weight: bold;\n  margin-left: ", ";\n"])), space_1.default(1));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=accountSecurityDetails.jsx.map