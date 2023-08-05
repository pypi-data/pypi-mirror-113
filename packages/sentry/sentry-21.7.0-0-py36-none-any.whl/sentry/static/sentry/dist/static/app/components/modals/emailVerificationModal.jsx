Object.defineProperty(exports, "__esModule", { value: true });
exports.EmailVerificationModal = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var locale_1 = require("app/locale");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var accountEmails_1 = require("app/views/settings/account/accountEmails");
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
function EmailVerificationModal(_a) {
    var Header = _a.Header, Body = _a.Body, _b = _a.actionMessage, actionMessage = _b === void 0 ? 'taking this action' : _b;
    return (<React.Fragment>
      <Header closeButton>{locale_1.t('Action Required')}</Header>
      <Body>
        <textBlock_1.default>
          {locale_1.tct('Please verify your email before [actionMessage], or [link].', {
            actionMessage: actionMessage,
            link: (<link_1.default to="/settings/account/emails/" data-test-id="email-settings-link">
                {locale_1.t('go to your email settings')}
              </link_1.default>),
        })}
        </textBlock_1.default>
        <accountEmails_1.EmailAddresses />
      </Body>
    </React.Fragment>);
}
exports.EmailVerificationModal = EmailVerificationModal;
exports.default = react_router_1.withRouter(withApi_1.default(EmailVerificationModal));
//# sourceMappingURL=emailVerificationModal.jsx.map