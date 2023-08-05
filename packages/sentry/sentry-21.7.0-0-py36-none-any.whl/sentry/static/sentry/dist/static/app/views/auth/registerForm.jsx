Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var react_2 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var form_1 = tslib_1.__importDefault(require("app/components/forms/form"));
var passwordField_1 = tslib_1.__importDefault(require("app/components/forms/passwordField"));
var radioBooleanField_1 = tslib_1.__importDefault(require("app/components/forms/radioBooleanField"));
var textField_1 = tslib_1.__importDefault(require("app/components/forms/textField"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var locale_1 = require("app/locale");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var login_1 = require("app/views/auth/login");
var SubscribeField = function () { return (<radioBooleanField_1.default name="subscribe" yesLabel={locale_1.t('Yes, I would like to receive updates via email')} noLabel={locale_1.t("No, I'd prefer not to receive these updates")} help={locale_1.tct("We'd love to keep you updated via email with product and feature\n           announcements, promotions, educational materials, and events. Our\n           updates focus on relevant information, and we'll never sell your data\n           to third parties. See our [link] for more details.", {
        link: <a href="https://sentry.io/privacy/">Privacy Policy</a>,
    })}/>); };
var RegisterForm = /** @class */ (function (_super) {
    tslib_1.__extends(RegisterForm, _super);
    function RegisterForm() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            errorMessage: null,
            errors: {},
        };
        _this.handleSubmit = function (data, onSuccess, onError) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var api, response, e_1, message;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        api = this.props.api;
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise('/auth/register/', {
                                method: 'POST',
                                data: data,
                            })];
                    case 2:
                        response = _a.sent();
                        onSuccess(data);
                        // TODO(epurkhiser): There is more we need to do to setup the user. but
                        // definitely primarily we need to init our user.
                        configStore_1.default.set('user', response.user);
                        react_router_1.browserHistory.push({ pathname: response.nextUri });
                        return [3 /*break*/, 4];
                    case 3:
                        e_1 = _a.sent();
                        if (!e_1.responseJSON || !e_1.responseJSON.errors) {
                            onError(e_1);
                            return [2 /*return*/];
                        }
                        message = e_1.responseJSON.detail;
                        if (e_1.responseJSON.errors.__all__) {
                            message = e_1.responseJSON.errors.__all__;
                        }
                        this.setState({
                            errorMessage: message,
                            errors: e_1.responseJSON.errors || {},
                        });
                        onError(e_1);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    RegisterForm.prototype.render = function () {
        var _this = this;
        var hasNewsletter = this.props.authConfig.hasNewsletter;
        var _a = this.state, errorMessage = _a.errorMessage, errors = _a.errors;
        return (<react_2.ClassNames>
        {function (_a) {
                var css = _a.css;
                return (<form_1.default initialData={{ subscribe: true }} submitLabel={locale_1.t('Continue')} onSubmit={_this.handleSubmit} footerClass={css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n              ", "\n            "], ["\n              ", "\n            "])), login_1.formFooterClass)} errorMessage={errorMessage} extraButton={<PrivacyPolicyLink href="https://sentry.io/privacy/">
                {locale_1.t('Privacy Policy')}
              </PrivacyPolicyLink>}>
            <textField_1.default name="name" placeholder={locale_1.t('Jane Bloggs')} label={locale_1.t('Name')} error={errors.name} required/>
            <textField_1.default name="username" placeholder={locale_1.t('you@example.com')} label={locale_1.t('Email')} error={errors.username} required/>
            <passwordField_1.default name="password" placeholder={locale_1.t('something super secret')} label={locale_1.t('Password')} error={errors.password} required/>
            {hasNewsletter && <SubscribeField />}
          </form_1.default>);
            }}
      </react_2.ClassNames>);
    };
    return RegisterForm;
}(react_1.Component));
var PrivacyPolicyLink = styled_1.default(externalLink_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n\n  &:hover {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.textColor; });
exports.default = RegisterForm;
var templateObject_1, templateObject_2;
//# sourceMappingURL=registerForm.jsx.map