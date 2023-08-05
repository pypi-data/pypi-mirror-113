Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var indicator_1 = require("app/actionCreators/indicator");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var locale_1 = require("app/locale");
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var AdminMail = /** @class */ (function (_super) {
    tslib_1.__extends(AdminMail, _super);
    function AdminMail() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.sendTestEmail = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var testMailEmail, error_1;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        testMailEmail = this.state.data.testMailEmail;
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise('/internal/mail/', { method: 'POST' })];
                    case 2:
                        _a.sent();
                        indicator_1.addSuccessMessage(locale_1.t('A test email has been sent to %s', testMailEmail));
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _a.sent();
                        indicator_1.addErrorMessage(error_1.responseJSON
                            ? error_1.responseJSON.error
                            : locale_1.t('Unable to send test email. Check your server logs'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    AdminMail.prototype.getEndpoints = function () {
        return [['data', '/internal/mail/']];
    };
    AdminMail.prototype.renderBody = function () {
        var data = this.state.data;
        var mailHost = data.mailHost, mailPassword = data.mailPassword, mailUsername = data.mailUsername, mailPort = data.mailPort, mailUseTls = data.mailUseTls, mailUseSsl = data.mailUseSsl, mailFrom = data.mailFrom, mailListNamespace = data.mailListNamespace, testMailEmail = data.testMailEmail;
        return (<div>
        <h3>{locale_1.t('SMTP Settings')}</h3>

        <dl className="vars">
          <dt>{locale_1.t('From Address')}</dt>
          <dd>
            <pre className="val">{mailFrom}</pre>
          </dd>

          <dt>{locale_1.t('Host')}</dt>
          <dd>
            <pre className="val">
              {mailHost}:{mailPort}
            </pre>
          </dd>

          <dt>{locale_1.t('Username')}</dt>
          <dd>
            <pre className="val">{mailUsername || <em>{locale_1.t('not set')}</em>}</pre>
          </dd>

          <dt>{locale_1.t('Password')}</dt>
          <dd>
            <pre className="val">
              {mailPassword ? '********' : <em>{locale_1.t('not set')}</em>}
            </pre>
          </dd>

          <dt>{locale_1.t('STARTTLS?')}</dt>
          <dd>
            <pre className="val">{mailUseTls ? locale_1.t('Yes') : locale_1.t('No')}</pre>
          </dd>

          <dt>{locale_1.t('SSL?')}</dt>
          <dd>
            <pre className="val">{mailUseSsl ? locale_1.t('Yes') : locale_1.t('No')}</pre>
          </dd>

          <dt>{locale_1.t('Mailing List Namespace')}</dt>
          <dd>
            <pre className="val">{mailListNamespace}</pre>
          </dd>
        </dl>

        <h3>{locale_1.t('Test Settings')}</h3>

        <p>
          {locale_1.t("Send an email to your account's email address to confirm that everything is configured correctly.")}
        </p>

        <button_1.default onClick={this.sendTestEmail}>
          {locale_1.t('Send a test email to %s', testMailEmail)}
        </button_1.default>
      </div>);
    };
    return AdminMail;
}(asyncView_1.default));
exports.default = AdminMail;
//# sourceMappingURL=adminMail.jsx.map