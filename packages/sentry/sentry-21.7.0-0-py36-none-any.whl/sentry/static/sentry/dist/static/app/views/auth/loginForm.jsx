Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var react_2 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var form_1 = tslib_1.__importDefault(require("app/components/forms/form"));
var passwordField_1 = tslib_1.__importDefault(require("app/components/forms/passwordField"));
var textField_1 = tslib_1.__importDefault(require("app/components/forms/textField"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var login_1 = require("app/views/auth/login");
// TODO(epurkhiser): The abstraction here would be much nicer if we just
// exposed a configuration object telling us what auth providers there are.
var LoginProviders = function (_a) {
    var vstsLoginLink = _a.vstsLoginLink, githubLoginLink = _a.githubLoginLink, googleLoginLink = _a.googleLoginLink;
    return (<ProviderWrapper>
    <ProviderHeading>{locale_1.t('External Account Login')}</ProviderHeading>
    {googleLoginLink && (<button_1.default align="left" size="small" icon={<icons_1.IconGoogle size="xs"/>} href={googleLoginLink}>
        {locale_1.t('Sign in with Google')}
      </button_1.default>)}
    {githubLoginLink && (<button_1.default align="left" size="small" icon={<icons_1.IconGithub size="xs"/>} href={githubLoginLink}>
        {locale_1.t('Sign in with GitHub')}
      </button_1.default>)}
    {vstsLoginLink && (<button_1.default align="left" size="small" icon={<icons_1.IconVsts size="xs"/>} href={vstsLoginLink}>
        {locale_1.t('Sign in with Azure DevOps')}
      </button_1.default>)}
  </ProviderWrapper>);
};
var LoginForm = /** @class */ (function (_super) {
    tslib_1.__extends(LoginForm, _super);
    function LoginForm() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            errorMessage: null,
            errors: {},
        };
        _this.handleSubmit = function (data, onSuccess, onError) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var response, e_1, message;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        _a.trys.push([0, 2, , 3]);
                        return [4 /*yield*/, this.props.api.requestPromise('/auth/login/', {
                                method: 'POST',
                                data: data,
                            })];
                    case 1:
                        response = _a.sent();
                        onSuccess(data);
                        // TODO(epurkhiser): There is likely more that needs to happen to update
                        // the application state after user login.
                        configStore_1.default.set('user', response.user);
                        // TODO(epurkhiser): Reconfigure sentry SDK identity
                        react_router_1.browserHistory.push({ pathname: response.nextUri });
                        return [3 /*break*/, 3];
                    case 2:
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
                        return [3 /*break*/, 3];
                    case 3: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    LoginForm.prototype.render = function () {
        var _this = this;
        var _a = this.state, errorMessage = _a.errorMessage, errors = _a.errors;
        var _b = this.props.authConfig, githubLoginLink = _b.githubLoginLink, vstsLoginLink = _b.vstsLoginLink;
        var hasLoginProvider = !!(githubLoginLink || vstsLoginLink);
        return (<react_2.ClassNames>
        {function (_a) {
                var css = _a.css;
                return (<FormWrapper hasLoginProvider={hasLoginProvider}>
            <form_1.default submitLabel={locale_1.t('Continue')} onSubmit={_this.handleSubmit} footerClass={css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n                ", "\n              "], ["\n                ", "\n              "])), login_1.formFooterClass)} errorMessage={errorMessage} extraButton={<LostPasswordLink to="/account/recover/">
                  {locale_1.t('Lost your password?')}
                </LostPasswordLink>}>
              <textField_1.default name="username" placeholder={locale_1.t('username or email')} label={locale_1.t('Account')} error={errors.username} required/>
              <passwordField_1.default name="password" placeholder={locale_1.t('password')} label={locale_1.t('Password')} error={errors.password} required/>
            </form_1.default>
            {hasLoginProvider && <LoginProviders {...{ vstsLoginLink: vstsLoginLink, githubLoginLink: githubLoginLink }}/>}
          </FormWrapper>);
            }}
      </react_2.ClassNames>);
    };
    return LoginForm;
}(react_1.Component));
var FormWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: 60px;\n  grid-template-columns: ", ";\n"], ["\n  display: grid;\n  grid-gap: 60px;\n  grid-template-columns: ", ";\n"])), function (p) { return (p.hasLoginProvider ? '1fr 0.8fr' : '1fr'); });
var ProviderHeading = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin: 0;\n  font-size: 15px;\n  font-weight: bold;\n  line-height: 24px;\n"], ["\n  margin: 0;\n  font-size: 15px;\n  font-weight: bold;\n  line-height: 24px;\n"])));
var ProviderWrapper = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  display: grid;\n  grid-auto-rows: max-content;\n  grid-gap: ", ";\n\n  &:before {\n    position: absolute;\n    display: block;\n    content: '';\n    top: 0;\n    bottom: 0;\n    left: -30px;\n    border-left: 1px solid ", ";\n  }\n"], ["\n  position: relative;\n  display: grid;\n  grid-auto-rows: max-content;\n  grid-gap: ", ";\n\n  &:before {\n    position: absolute;\n    display: block;\n    content: '';\n    top: 0;\n    bottom: 0;\n    left: -30px;\n    border-left: 1px solid ", ";\n  }\n"])), space_1.default(1.5), function (p) { return p.theme.border; });
var LostPasswordLink = styled_1.default(link_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n\n  &:hover {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.textColor; });
exports.default = LoginForm;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=loginForm.jsx.map