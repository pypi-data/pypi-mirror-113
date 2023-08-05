Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
var RecoveryOptionsModal = /** @class */ (function (_super) {
    tslib_1.__extends(RecoveryOptionsModal, _super);
    function RecoveryOptionsModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSkipSms = function () {
            _this.setState({ skipSms: true });
        };
        return _this;
    }
    RecoveryOptionsModal.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { skipSms: false });
    };
    RecoveryOptionsModal.prototype.getEndpoints = function () {
        return [['authenticators', '/users/me/authenticators/']];
    };
    RecoveryOptionsModal.prototype.renderBody = function () {
        var _a = this.props, authenticatorName = _a.authenticatorName, closeModal = _a.closeModal, Body = _a.Body, Header = _a.Header, Footer = _a.Footer;
        var _b = this.state, authenticators = _b.authenticators, skipSms = _b.skipSms;
        var _c = authenticators.reduce(function (obj, item) {
            obj[item.id] = item;
            return obj;
        }, {}), recovery = _c.recovery, sms = _c.sms;
        var recoveryEnrolled = recovery && recovery.isEnrolled;
        var displaySmsPrompt = sms && !sms.isEnrolled && !skipSms;
        return (<react_1.Fragment>
        <Header closeButton>{locale_1.t('Two-Factor Authentication Enabled')}</Header>

        <Body>
          <textBlock_1.default>
            {locale_1.t('Two-factor authentication via %s has been enabled.', authenticatorName)}
          </textBlock_1.default>
          <textBlock_1.default>
            {locale_1.t('You should now set up recovery options to secure your account.')}
          </textBlock_1.default>

          {displaySmsPrompt ? (
            // set up backup phone number
            <alert_1.default type="warning">
              {locale_1.t('We recommend adding a phone number as a backup 2FA method.')}
            </alert_1.default>) : (
            // get recovery codes
            <alert_1.default type="warning">
              {locale_1.t("Recovery codes are the only way to access your account if you lose\n                  your device and cannot receive two-factor authentication codes.")}
            </alert_1.default>)}
        </Body>

        {displaySmsPrompt ? (
            // set up backup phone number
            <Footer>
            <button_1.default onClick={this.handleSkipSms} name="skipStep" autoFocus>
              {locale_1.t('Skip this step')}
            </button_1.default>
            <button_1.default priority="primary" onClick={closeModal} to={"/settings/account/security/mfa/" + sms.id + "/enroll/"} name="addPhone" css={{ marginLeft: space_1.default(1) }} autoFocus>
              {locale_1.t('Add a Phone Number')}
            </button_1.default>
          </Footer>) : (
            // get recovery codes
            <Footer>
            <button_1.default priority="primary" onClick={closeModal} to={recoveryEnrolled
                    ? "/settings/account/security/mfa/" + recovery.authId + "/"
                    : '/settings/account/security/'} name="getCodes" autoFocus>
              {locale_1.t('Get Recovery Codes')}
            </button_1.default>
          </Footer>)}
      </react_1.Fragment>);
    };
    return RecoveryOptionsModal;
}(asyncComponent_1.default));
exports.default = RecoveryOptionsModal;
//# sourceMappingURL=recoveryOptionsModal.jsx.map