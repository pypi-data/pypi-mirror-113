Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var forms_1 = require("app/components/forms");
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var narrowLayout_1 = tslib_1.__importDefault(require("app/components/narrowLayout"));
var locale_1 = require("app/locale");
var NewsletterConsent = /** @class */ (function (_super) {
    tslib_1.__extends(NewsletterConsent, _super);
    function NewsletterConsent() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    NewsletterConsent.prototype.componentDidMount = function () {
        document.body.classList.add('auth');
    };
    NewsletterConsent.prototype.componentWillUnmount = function () {
        document.body.classList.remove('auth');
    };
    // NOTE: the text here is duplicated within ``RegisterForm`` on the backend
    NewsletterConsent.prototype.render = function () {
        var _this = this;
        return (<narrowLayout_1.default>
        <p>
          {locale_1.t('Pardon the interruption, we just need to get a quick answer from you.')}
        </p>

        <forms_1.ApiForm apiMethod="POST" apiEndpoint="/users/me/subscriptions/" onSubmitSuccess={function () { var _a, _b; return (_b = (_a = _this.props).onSubmitSuccess) === null || _b === void 0 ? void 0 : _b.call(_a); }} submitLabel={locale_1.t('Continue')}>
          <forms_1.RadioBooleanField key="subscribed" name="subscribed" label={locale_1.t('Email Updates')} help={<span>
                {locale_1.tct("We'd love to keep you updated via email with product and feature\n                   announcements, promotions, educational materials, and events. Our updates\n                   focus on relevant information, and we'll never sell your data to third\n                   parties. See our [link:Privacy Policy] for more details.\n                   ", { link: <externalLink_1.default href="https://sentry.io/privacy/"/> })}
              </span>} yesLabel={locale_1.t('Yes, I would like to receive updates via email')} noLabel={locale_1.t("No, I'd prefer not to receive these updates")} required/>
        </forms_1.ApiForm>
      </narrowLayout_1.default>);
    };
    return NewsletterConsent;
}(react_1.Component));
exports.default = NewsletterConsent;
//# sourceMappingURL=newsletterConsent.jsx.map